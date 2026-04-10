import asyncio
import sys
sys.path.insert(0, '.')

from httpx import AsyncClient, ASGITransport
from app.main import app

async def test_otp():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        try:
            response = await client.post(
                "/api/auth/send-otp",
                json={"phone": "9876543210"}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 500:
                print("\nFull response:")
                print(response.json())
        except Exception as e:
            print(f"Exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_otp())
