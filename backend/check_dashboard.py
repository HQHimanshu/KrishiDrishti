"""Check what's happening with dashboard endpoint"""
import requests
import json
import time

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1OTAzMDg2fQ.jGtjygkWjnq5pjSxcP_b-rdg_pGBjdm-_mmNax7ZUyk"
BASE = "http://localhost:8000"

print("🔍 Testing Dashboard Endpoint...")
print("="*60)

# Test with timeout
try:
    print("\n⏱️  Calling /api/dashboard/metrics/...")
    start = time.time()
    response = requests.get(
        f"{BASE}/api/dashboard/metrics/",
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=15
    )
    elapsed = time.time() - start
    
    print(f"   Response time: {elapsed:.2f}s")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Dashboard Data:")
        print(f"   Sensor: {data.get('current_sensor_data')}")
        print(f"   Weather: {data.get('weather')}")
        print(f"   Resources: {data.get('resource_summary')}")
        print(f"   Alerts: {len(data.get('recent_alerts', []))}")
    else:
        print(f"   Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print(f"   ❌ TIMEOUT after 15s")
    print(f"   💡 Weather API is hanging the request")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test sensor data directly
print("\n" + "="*60)
print("📊 Latest Sensor Reading...")
try:
    response = requests.get(
        f"{BASE}/api/sensors/latest",
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Data: {json.dumps(data, indent=6)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test Ollama
print("\n" + "="*60)
print("🤖 Testing Ollama...")
try:
    import httpx
    import asyncio
    
    async def test_ollama():
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "qwen2.5vl:3b",
                        "prompt": "Hello",
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    return "✅ RUNNING", response.json().get("response", "")[:50]
                else:
                    return "❌ NOT RUNNING", f"Status: {response.status_code}"
            except:
                return "❌ NOT RUNNING", "Connection refused"
    
    status, msg = asyncio.run(test_ollama())
    print(f"   Status: {status}")
    print(f"   Details: {msg}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
