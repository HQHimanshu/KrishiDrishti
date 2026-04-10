"""
Comprehensive Diagnostic Tool
Checks Database, Ollama, and Backend API
"""
import asyncio
import requests
import sqlite3
import httpx
import json

print("🔍 Starting KrishiDrishti Diagnostic...")
print("="*60)

# 1. Check Database
print("\n1️⃣  CHECKING DATABASE...")
try:
    conn = sqlite3.connect('krishidrishti.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    count = cursor.fetchone()[0]
    print(f"   📊 Total readings: {count}")
    
    if count > 0:
        cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        print(f"   ✅ Latest: ID={row[0]}, Temp={row[3]}, Hum={row[4]}, Soil={row[6]}")
    else:
        print("   ❌ NO DATA IN DATABASE! Check Arduino connection.")
    conn.close()
except Exception as e:
    print(f"   ❌ DB Error: {e}")

# 2. Check Ollama
print("\n2️⃣  CHECKING OLLAMA...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    models = response.json().get('models', [])
    print(f"   🤖 Models loaded:")
    for m in models:
        print(f"      - {m['name']}")
    
    # Test generation
    print("   🧪 Testing generation...")
    test_resp = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5:1.5b",
        "prompt": "Say OK",
        "stream": False
    }, timeout=30)
    
    if test_resp.status_code == 200:
        print("   ✅ Ollama is responding!")
    else:
        print(f"   ❌ Ollama generation failed: {test_resp.status_code}")
except Exception as e:
    print(f"   ❌ Ollama Error: {e}")
    print("   💡 Is 'ollama serve' running?")

# 3. Check Backend API
print("\n3️⃣  CHECKING BACKEND API...")
BASE = "http://localhost:8000"

# Login first
try:
    print("   🔑 Logging in...")
    r1 = requests.post(f"{BASE}/api/auth/send-otp", json={"phone": "+919876543210"})
    r2 = requests.post(f"{BASE}/api/auth/verify-otp", json={"phone": "+919876543210", "otp_code": "123456"})
    token = r2.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print(f"   ✅ Logged in. Token: {token[:20]}...")
    
    # Check Dashboard
    print("   📊 Fetching dashboard metrics...")
    r3 = requests.get(f"{BASE}/api/dashboard/metrics", headers=headers, timeout=10)
    if r3.status_code == 200:
        data = r3.json()
        sensor = data.get('current_sensor_data')
        if sensor and sensor.get('temperature'):
            print(f"   ✅ Dashboard working! Temp: {sensor['temperature']}°C")
        else:
            print(f"   ⚠️  Dashboard returned no sensor data. Response keys: {list(data.keys())}")
    else:
        print(f"   ❌ Dashboard failed: {r3.status_code} {r3.text}")

    # Check Analytics
    print("   📈 Fetching analytics trends...")
    r4 = requests.get(f"{BASE}/api/dashboard/trends?days=7", headers=headers, timeout=10)
    if r4.status_code == 200:
        t_data = r4.json()
        trends = t_data.get('sensor_trend', [])
        print(f"   ✅ Analytics working! Found {len(trends)} trend points.")
    else:
        print(f"   ❌ Analytics failed: {r4.status_code}")
        
    # Check AI Advice
    print("   💬 Testing AI advice...")
    r5 = requests.post(f"{BASE}/api/advice", json={"question": "Test"}, headers=headers, timeout=60)
    if r5.status_code == 200:
        print(f"   ✅ AI advice working! Resp: {r5.json().get('recommendation')}")
    else:
        print(f"   ❌ AI advice failed: {r5.status_code} {r5.text[:100]}")

except Exception as e:
    print(f"   ❌ API Error: {e}")
    print("   💡 Is the backend running? Run: python run.py")

print("\n" + "="*60)
print("✅ Diagnostic Complete!")
