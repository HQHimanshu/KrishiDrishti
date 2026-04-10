"""
Quick test to verify the complete pipeline
Run: python test_usb_pipeline.py
"""
import requests
import json

print("🧪 Testing KrishiDrishti Pipeline...")
print("="*60)

# Step 1: Login
print("\n1️⃣  Testing login...")
try:
    # Send OTP
    response = requests.post(
        "http://localhost:8000/api/auth/send-otp",
        json={"phone": "+919876543210"}
    )
    print(f"   ✅ OTP sent: {response.status_code}")
    
    # Verify OTP
    response = requests.post(
        "http://localhost:8000/api/auth/verify-otp",
        json={"phone": "+919876543210", "otp_code": "123456"}
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"   ✅ Login successful!")
        print(f"   📱 User: {response.json()['user']['name']}")
        print(f"   🔑 Token: {token[:30]}...")
    else:
        print(f"   ❌ Login failed: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"   ❌ Login error: {e}")
    print("   💡 Is backend running? (python -m uvicorn app.main:app --reload)")
    exit(1)

# Step 2: Send test sensor data
print("\n2️⃣  Testing sensor data submission...")
try:
    test_data = {
        "temperature": 32.5,
        "humidity": 68.2,
        "soil_moisture_surface": 520,
        "soil_moisture_root": 580,
        "ph_level": 6.8,
        "rain_detected": False,
        "water_tank_level": 75.0
    }
    
    response = requests.post(
        "http://localhost:8000/api/sensors/",
        headers={"Authorization": f"Bearer {token}"},
        json=test_data
    )
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"   ✅ Sensor data saved (ID: {result['id']})")
        print(f"   🌡️  Temperature: {result['temperature']}°C")
        print(f"   💧 Humidity: {result['humidity']}%")
        print(f"   🌱 Soil Moisture: {result['soil_moisture_root']} ADC")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ❌ Sensor error: {e}")

# Step 3: Get dashboard metrics
print("\n3️⃣  Testing dashboard metrics...")
try:
    response = requests.get(
        "http://localhost:8000/api/dashboard/metrics/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Dashboard data retrieved!")
        if data.get('current_sensor_data'):
            sensor = data['current_sensor_data']
            print(f"   🌡️  Latest temperature: {sensor.get('temperature', 'N/A')}°C")
            print(f"   💧 Latest humidity: {sensor.get('humidity', 'N/A')}%")
        else:
            print("   ⚠️  No sensor data yet")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ Dashboard error: {e}")

# Step 4: Check Ollama
print("\n4️⃣  Testing Ollama AI model...")
try:
    import httpx
    import asyncio
    
    async def test_ollama():
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5vl:3b",
                    "prompt": "Say hello in one word",
                    "stream": False
                }
            )
            return response.status_code == 200
    
    result = asyncio.run(test_ollama())
    if result:
        print(f"   ✅ Ollama is running with qwen2.5vl:3b")
    else:
        print(f"   ⚠️  Ollama not responding")
        print(f"   💡 Run: ollama serve")
        
except Exception as e:
    print(f"   ⚠️  Ollama test failed: {e}")
    print(f"   💡 Make sure Ollama is running: ollama serve")

# Summary
print("\n" + "="*60)
print("✅ PIPELINE TEST COMPLETE!")
print("="*60)
print("\n🎯 Next Steps:")
print("1. Upload your Arduino code")
print("2. Close Arduino Serial Monitor")
print("3. Run: run_usb_bridge.bat")
print("4. Watch data flow to dashboard!")
print("\n📱 Your Token (copy this):")
print(token)
print("="*60)
