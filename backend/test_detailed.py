import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            'http://localhost:8000/api/auth/send-otp', 
            json={'phone': '+919876543210'},
            timeout=10.0
        )
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        if resp.status_code == 500:
            print("\n=== FULL ERROR ===")
            print(resp.json())

asyncio.run(test())
