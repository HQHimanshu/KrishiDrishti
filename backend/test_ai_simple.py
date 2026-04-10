import requests
import json

# Login
r1 = requests.post("http://localhost:8000/api/auth/send-otp", json={"phone": "+919876543210"})
r2 = requests.post("http://localhost:8000/api/auth/verify-otp", json={"phone": "+919876543210", "otp_code": "123456"})
token = r2.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

print("Testing AI advice with simplified prompt...")
try:
    r = requests.post("http://localhost:8000/api/advice", 
                      json={"question": "Should I irrigate my wheat crop?"}, 
                      headers=headers, 
                      timeout=120)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"Recommendation: {data.get('recommendation')}")
        print(f"Reason: {data.get('reason', '')[:100]}")
        print(f"Action: {data.get('action', '')[:100]}")
    else:
        print(f"Error: {r.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")
