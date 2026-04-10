import asyncio
from app.database import get_db
from app.models import User
from sqlalchemy import select

async def update():
    async for db in get_db():
        result = await db.execute(
            select(User).where(User.phone == '+919876543210')
        )
        user = result.scalar_one_or_none()
        user.location_lat = 19.0760  # Mumbai
        user.location_lng = 72.8777  # Mumbai
        await db.commit()
        print('✅ Updated location to Mumbai (19.0760, 72.8777)')
        break

asyncio.run(update())
