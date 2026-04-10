import asyncio
from app.database import get_db
from app.models import User
from sqlalchemy import select

async def test():
    async for db in get_db():
        result = await db.execute(
            select(User).where(User.phone == '+919876543210')
        )
        user = result.scalar_one_or_none()
        if user:
            print(f'✅ User found:')
            print(f'  ID: {user.id}')
            print(f'  Name: {user.name}')
            print(f'  Phone: {user.phone}')
            print(f'  Crop: {user.crop_type}')
        else:
            print('❌ User not found')
        break

asyncio.run(test())
