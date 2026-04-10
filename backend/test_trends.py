import requests
import json

# Login
r1 = requests.post("http://localhost:8000/api/auth/send-otp", json={"phone": "+919876543210"})
r2 = requests.post("http://localhost:8000/api/auth/verify-otp", json={"phone": "+919876543210", "otp_code": "123456"})
token = r2.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

print("Testing trends endpoint...")
r = requests.get("http://localhost:8000/api/dashboard/trends?days=7", headers=headers)
print(f"Status: {r.status_code}")
data = r.json()
print(f"Total readings: {data.get('total_readings', 0)}")
print(f"Trend points: {len(data.get('sensor_trend', []))}")

if data.get('sensor_trend'):
    print(f"First point: {data['sensor_trend'][0]}")
else:
    print("No data returned!")
