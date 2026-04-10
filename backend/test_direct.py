import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("Testing /api/auth/send-otp endpoint...")
response = client.post(
    "/api/auth/send-otp",
    json={"phone": "+919876543210"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code != 200:
    print("\n=== ERROR DETAILS ===")
    try:
        print(response.json())
    except:
        print(response.text)
