"""
Test Dashboard API Endpoints
Simulates exactly what the frontend does
"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_dashboard_endpoints():
    print("=" * 60)
    print("  KrishiDrishti - Dashboard API Test")
    print("=" * 60)
    print()
    
    # Step 1: Get authentication token
    print("[1/4] Getting authentication token...")
    res1 = requests.post(
        f"{BACKEND_URL}/api/auth/send-otp",
        json={"phone": "8626081052"}
    )
    
    if res1.status_code != 200:
        print(f"  ❌ Failed to get OTP: {res1.text}")
        return
    
    otp = res1.json().get("mock_otp", "123456")
    print(f"  ✅ OTP received: {otp}")
    
    res2 = requests.post(
        f"{BACKEND_URL}/api/auth/verify-otp",
        json={"phone": "8626081052", "otp_code": otp}
    )
    
    if res2.status_code != 200:
        print(f"  ❌ Failed to verify OTP: {res2.text}")
        return
    
    token = res2.json()["access_token"]
    print(f"  ✅ Token obtained")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Test Dashboard Metrics
    print(f"\n[2/4] Testing GET /api/dashboard/metrics...")
    res3 = requests.get(f"{BACKEND_URL}/api/dashboard/metrics", headers=headers)
    
    print(f"  Status: {res3.status_code}")
    
    if res3.status_code == 200:
        data = res3.json()
        sensor = data.get("current_sensor_data")
        
        if sensor:
            print(f"  ✅ Sensor data found!")
            print(f"     - Temperature: {sensor.get('temperature')}°C")
            print(f"     - Humidity: {sensor.get('humidity')}%")
            print(f"     - Soil Moisture: {sensor.get('soil_moisture_root')} ADC")
            print(f"     - pH Level: {sensor.get('ph_level')}")
            print(f"     - Rain: {sensor.get('rain_detected')}")
            print(f"     - Water Tank: {sensor.get('water_tank_level')}%")
        else:
            print(f"  ❌ No sensor data in response")
            print(f"  Full response: {json.dumps(data, indent=2)}")
    else:
        print(f"  ❌ Failed: {res3.text[:200]}")
    
    # Step 3: Test Dashboard Trends
    print(f"\n[3/4] Testing GET /api/dashboard/trends?days=1...")
    res4 = requests.get(
        f"{BACKEND_URL}/api/dashboard/trends",
        headers=headers,
        params={"days": 1}
    )
    
    print(f"  Status: {res4.status_code}")
    
    if res4.status_code == 200:
        data = res4.json()
        trend = data.get("sensor_trend", [])
        total = data.get("total_readings", 0)
        
        if len(trend) > 0:
            print(f"  ✅ Trends data found!")
            print(f"     - Total readings: {total}")
            print(f"     - Trend points: {len(trend)}")
            print(f"     - First: {trend[0]['timestamp']}")
            print(f"     - Last: {trend[-1]['timestamp']}")
        else:
            print(f"  ⚠️  No trend data (total_readings: {total})")
    else:
        print(f"  ❌ Failed: {res4.text[:200]}")
    
    # Step 4: Test Latest Sensor
    print(f"\n[4/4] Testing GET /api/sensors/latest...")
    res5 = requests.get(f"{BACKEND_URL}/api/sensors/latest", headers=headers)
    
    print(f"  Status: {res5.status_code}")
    
    if res5.status_code == 200:
        data = res5.json()
        print(f"  ✅ Latest sensor reading:")
        print(f"     - ID: {data.get('id')}")
        print(f"     - Time: {data.get('timestamp')}")
        print(f"     - Temperature: {data.get('temperature')}°C")
        print(f"     - Humidity: {data.get('humidity')}%")
    else:
        print(f"  ❌ Failed: {res5.text[:200]}")
    
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    
    if res3.status_code == 200 and res5.status_code == 200:
        print("  ✅ ALL ENDPOINTS WORKING")
        print("\n  Your token (copy this to browser console):")
        print(f"  {token}")
        print(f"\n  Command to run in browser console (F12):")
        print(f'  localStorage.setItem("token", "{token}")')
    else:
        print("  ❌ SOME ENDPOINTS FAILED - check backend logs")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_dashboard_endpoints()
