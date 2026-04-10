from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import SensorReading, User
from app.schemas import SensorDataCreate, SensorResponse, SensorHistoryResponse
from app.security import verify_token
from app.services import notification_service
from app.utils.helpers import calculate_moisture_percentage

router = APIRouter()


@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    sensor_data: SensorDataCreate,
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Receive sensor data from Arduino or mobile app"""
    
    # Verify user exists
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create sensor reading
    reading = SensorReading(
        user_id=user_id,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        soil_moisture_surface=sensor_data.soil_moisture_surface,
        soil_moisture_root=sensor_data.soil_moisture_root,
        ph_level=sensor_data.ph_level,
        rain_detected=sensor_data.rain_detected,
        water_tank_level=sensor_data.water_tank_level
    )
    
    db.add(reading)
    await db.commit()
    await db.refresh(reading)
    
    # Check for critical conditions and send alerts
    await check_sensor_alerts(user, reading, db)
    
    return SensorResponse.from_orm(reading)


@router.get("/latest", response_model=SensorResponse)
async def get_latest_reading(
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get latest sensor reading for user"""
    
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.user_id == user_id)
        .order_by(desc(SensorReading.timestamp))
        .limit(1)
    )
    reading = result.scalar_one_or_none()
    
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sensor readings found"
        )
    
    return SensorResponse.from_orm(reading)


@router.get("/history", response_model=SensorHistoryResponse)
async def get_sensor_history(
    hours: int = Query(default=24, ge=1, le=168),  # Max 7 days
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get sensor history for specified time period"""
    
    # Calculate start time
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    result = await db.execute(
        select(SensorReading)
        .where(
            SensorReading.user_id == user_id,
            SensorReading.timestamp >= start_time
        )
        .order_by(SensorReading.timestamp)
    )
    readings = result.scalars().all()
    
    return SensorHistoryResponse(
        readings=[SensorResponse.from_orm(r) for r in readings],
        total=len(readings)
    )


async def check_sensor_alerts(user: User, reading: SensorReading, db: AsyncSession):
    """Check sensor data and send alerts if needed"""
    
    alerts_to_send = []
    
    # Check soil moisture (ADC value: 0=wet, 1023=dry)
    if reading.soil_moisture_root and reading.soil_moisture_root > 700:
        alerts_to_send.append("irrigate_now")
    
    # Check rain detected
    if reading.rain_detected:
        alerts_to_send.append("rain_detected")
    
    # Check high temperature
    if reading.temperature and reading.temperature > 40:
        alerts_to_send.append("high_temperature")
    
    # Check pH level
    if reading.ph_level:
        if reading.ph_level < 5.5:
            alerts_to_send.append("low_ph")
        elif reading.ph_level > 8.5:
            alerts_to_send.append("high_ph")
    
    # Send alerts
    for alert_key in alerts_to_send:
        try:
            await notification_service.send_alert(user, alert_key)
        except Exception as e:
            print(f"[WARNING] Failed to send alert {alert_key}: {e}")
