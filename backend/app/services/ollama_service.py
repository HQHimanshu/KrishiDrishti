import json
import httpx
from typing import Dict, Optional, List
from app.config import settings


async def get_farming_advice(
    user_id: int,
    question: str,
    sensor_data: Dict,
    crop_type: Optional[str] = None,
    language: str = "en",
    weather_data: Optional[Dict] = None,
    crop_health_history: Optional[Dict] = None,
    advice_history: Optional[List[Dict]] = None
) -> Dict:
    """Get advice from Qwen - simple and works for ANY question"""

    # Build context if farming-related
    context = ""
    
    farming_keywords = ['crop', 'farm', 'irrigat', 'fertiliz', 'pest', 'soil', 'harvest', 
                       'plant', 'seed', 'weather', 'rain', 'water', 'agriculture', 'kisan',
                       'wheat', 'rice', 'vegetable', 'grow']
    is_farming = any(kw in question.lower() for kw in farming_keywords)
    
    if is_farming:
        sensor_parts = []
        if sensor_data:
            if sensor_data.get("temperature") is not None:
                sensor_parts.append(f"Temperature: {sensor_data['temperature']}°C")
            if sensor_data.get("humidity") is not None:
                sensor_parts.append(f"Humidity: {sensor_data['humidity']}%")
            if sensor_data.get("soil_moisture_root") is not None:
                sensor_parts.append(f"Soil Moisture: {sensor_data['soil_moisture_root']} ADC")
            if sensor_data.get("ph_level") is not None:
                sensor_parts.append(f"pH: {sensor_data['ph_level']}")
            if sensor_data.get("rain_detected"):
                sensor_parts.append("Rain detected")
        
        sensor_text = ", ".join(sensor_parts) if sensor_parts else "No sensor data"
        
        weather_text = ""
        if weather_data:
            weather_text = f"Weather: {weather_data.get('temperature', '?')}°C, {weather_data.get('description', 'unknown')}"
        
        context = f"""Current conditions:
- Crop: {crop_type or 'Unknown'}
- Sensors: {sensor_text}
- {weather_text}

"""

    # Simple direct prompt
    prompt = f"""{context}Question: {question}

Answer the question helpfully. Return JSON:
{{"answer": "your response", "optimization_tips": "tips or null", "estimated_impact": "impact or null"}}"""

    # Call Ollama
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 2048
                }
            )

            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                # Try to extract JSON
                try:
                    text_clean = text.replace("```json", "").replace("```", "").strip()
                    start = text_clean.find('{')
                    end = text_clean.rfind('}') + 1
                    
                    if start >= 0 and end > start:
                        data = json.loads(text_clean[start:end])
                        return {
                            "recommendation": "Advice",
                            "reason": data.get("answer", text[:300]),
                            "action": data.get("answer", text[:300]),
                            "risk": None,
                            "confidence_score": 70,
                            "optimization_tips": data.get("optimization_tips"),
                            "estimated_impact": data.get("estimated_impact"),
                            "language": language
                        }
                except Exception as e:
                    print(f"[WARNING] JSON parse error: {e}")
                
                # Fallback: use text directly
                return {
                    "recommendation": "Response",
                    "reason": text[:400] if text else "No response",
                    "action": text[:400] if text else "No response",
                    "risk": None,
                    "confidence_score": 60,
                    "optimization_tips": None,
                    "estimated_impact": None,
                    "language": language
                }
            else:
                raise Exception(f"Ollama error: {response.status_code}")

    except httpx.ConnectError:
        raise Exception("Cannot connect to Ollama. Run: ollama serve")
    except httpx.ReadTimeout:
        raise Exception("Request timed out. Try a simpler question.")
    except Exception as e:
        raise Exception(f"AI error: {str(e)}")
