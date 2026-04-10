import httpx
from typing import Optional, Dict
from app.config import settings
import time


# Cache for weather data (avoid frequent API calls)
_weather_cache = {}
CACHE_DURATION = 1800  # 30 minutes


async def get_weather_data(lat: float, lng: float) -> Optional[Dict]:
    """Fetch current weather data from OpenWeatherMap"""

    # Return mock data if no API key
    if not settings.OPENWEATHER_API_KEY:
        return get_mock_weather()

    cache_key = f"{lat:.2f},{lng:.2f}"
    current_time = time.time()

    # Check cache (30 minutes)
    if cache_key in _weather_cache:
        cached_data, cached_time = _weather_cache[cache_key]
        if current_time - cached_time < CACHE_DURATION:
            return cached_data

    # Fetch from API
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lng,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 200:
                data = response.json()

                weather = {
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"],
                    "forecast": None,
                    "alert": None
                }

                # Cache the result
                _weather_cache[cache_key] = (weather, current_time)

                print(f"[OK] Weather fetched: {weather['temperature']}°C, {weather['description']}")
                return weather
            else:
                print(f"[WARNING] Weather API returned {response.status_code}")
                return get_mock_weather()

    except Exception as e:
        print(f"[WARNING] Weather fetch error: {e}")
        return get_mock_weather()


async def get_forecast_data(lat: float, lng: float) -> Optional[Dict]:
    """Get 5-day forecast (simplified)"""
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lng,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "cnt": 8  # 24 hours (3-hour intervals)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                
                forecast = []
                for item in data.get("list", [])[:8]:
                    forecast.append({
                        "datetime": item.get("dt_txt"),
                        "temperature": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "rain_probability": item.get("pop", 0) * 100
                    })
                
                return forecast
            else:
                return None
    
    except Exception as e:
        print(f"[WARNING] Forecast fetch error: {e}")
        return None


def check_weather_alerts(weather: Dict) -> Optional[str]:
    """Check for critical weather conditions"""
    alerts = []
    
    if weather.get("temperature", 0) > 40:
        alerts.append("अत्यधिक तापमान चेतावनी - अधिक सिंचाई की आवश्यकता हो सकती है")
    
    if weather.get("wind_speed", 0) > 50:
        alerts.append("तेज हवा की चेतावनी - फसल को नुकसान हो सकता है")
    
    if weather.get("humidity", 0) > 90:
        alerts.append("उच्च आर्द्रता - फंगल रोग का खतरा")
    
    return " | ".join(alerts) if alerts else None


def get_mock_weather() -> Dict:
    """Return mock weather data for development/demo"""
    from datetime import datetime, timedelta
    
    now = datetime.now()
    forecast = []
    for i in range(4):
        forecast_time = now + timedelta(hours=i*3)
        forecast.append({
            "datetime": forecast_time.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": 33.0 - i*2,
            "description": ["sunny", "partly cloudy", "cloudy", "light rain"][i],
            "rain_probability": 10 + i*15
        })
    
    return {
        "temperature": 32.5,
        "feels_like": 35.0,
        "humidity": 65.0,
        "description": "partly cloudy",
        "wind_speed": 12.5,
        "pressure": 1012,
        "forecast": forecast,
        "alert": None
    }
