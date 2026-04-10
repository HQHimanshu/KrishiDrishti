from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SensorReading
import httpx
from app.config import settings


async def store_offline_reading(
    db: AsyncSession,
    user_id: int,
    sensor_data: dict
) -> SensorReading:
    """Store sensor reading with offline flag for later sync"""
    
    reading = SensorReading(
        user_id=user_id,
        **sensor_data,
        is_synced=False
    )
    
    db.add(reading)
    await db.commit()
    await db.refresh(reading)
    
    return reading


async def sync_pending_readings(db: AsyncSession) -> dict:
    """Sync all unsynced readings when internet connection is restored"""
    
    # Get all unsynced readings
    result = await db.execute(
        select(SensorReading).where(SensorReading.is_synced == False)
    )
    unsynced = result.scalars().all()
    
    if not unsynced:
        return {"synced": 0, "failed": 0, "details": []}
    
    synced_count = 0
    failed_count = 0
    details = []
    
    for reading in unsynced:
        try:
            # Try to push to cloud API
            success = await push_to_cloud_api(reading)
            
            if success:
                # Mark as synced
                await db.execute(
                    update(SensorReading)
                    .where(SensorReading.id == reading.id)
                    .values(is_synced=True)
                )
                synced_count += 1
                details.append({"id": reading.id, "status": "SYNCED"})
            else:
                failed_count += 1
                details.append({"id": reading.id, "status": "FAILED"})
        
        except Exception as e:
            failed_count += 1
            details.append({"id": reading.id, "status": "ERROR", "error": str(e)})
    
    await db.commit()
    
    return {
        "synced": synced_count,
        "failed": failed_count,
        "total": len(unsynced),
        "details": details
    }


async def push_to_cloud_api(reading: SensorReading) -> bool:
    """Push a single reading to cloud API"""
    try:
        # In production, this would call your cloud API endpoint
        # For now, we just mark it as synced
        return True
        
        # Example implementation:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{settings.CLOUD_API_URL}/api/sensors",
        #         json={
        #             "user_id": reading.user_id,
        #             "temperature": reading.temperature,
        #             "humidity": reading.humidity,
        #             # ... other fields
        #         },
        #         headers={"Authorization": f"Bearer {settings.API_TOKEN}"}
        #     )
        #     return response.status_code == 200
    
    except Exception as e:
        print(f"[WARNING] Failed to sync reading {reading.id}: {e}")
        return False


async def get_offline_status(db: AsyncSession, user_id: int) -> dict:
    """Get count of pending offline readings"""
    
    result = await db.execute(
        select(SensorReading).where(
            SensorReading.user_id == user_id,
            SensorReading.is_synced == False
        )
    )
    pending = result.scalars().all()
    
    return {
        "pending_sync": len(pending),
        "readings": [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "temperature": r.temperature
            }
            for r in pending[:10]  # Return last 10
        ]
    }
