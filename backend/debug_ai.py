"""Debug AI Advice 500 Error"""
import requests
import json

# Login
r1 = requests.post("http://localhost:8000/api/auth/send-otp", json={"phone": "+919876543210"})
r2 = requests.post("http://localhost:8000/api/auth/verify-otp", json={"phone": "+919876543210", "otp_code": "123456"})
token = r2.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# Test AI
print("Testing AI advice with question: 'Should I water my crops?'")
try:
    r = requests.post("http://localhost:8000/api/advice", 
                      json={"question": "Should I water my crops?"}, 
                      headers=headers, 
                      timeout=120)
    print("Status:", r.status_code)
    print("Raw Response:", r.text[:1000])
except Exception as e:
    print("Request failed:", e)
