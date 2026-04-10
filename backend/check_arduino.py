"""Check Arduino data in database"""
import asyncio
from app.database import get_db
from app.models import SensorReading
from sqlalchemy import select, desc

async def check():
    async for db in get_db():
        result = await db.execute(
            select(SensorReading)
            .order_by(desc(SensorReading.timestamp))
            .limit(5)
        )
        readings = result.scalars().all()
        print(f"\n📊 Last {len(readings)} sensor readings:")
        for i, r in enumerate(readings):
            print(f"\n{'='*60}")
            print(f"#{i+1} ID:{r.id} | User:{r.user_id}")
            print(f"⏰ {r.timestamp}")
            print(f"🌡️  Temp: {r.temperature}°C")
            print(f"💧 Humidity: {r.humidity}%")
            print(f"🌱 Soil: {r.soil_moisture_root} ADC")
            print(f"🌧️  Rain: {r.rain_detected}")
            print(f"💧 Tank: {r.water_tank_level}%")
        break

asyncio.run(check())
