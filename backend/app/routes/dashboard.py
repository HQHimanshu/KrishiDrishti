from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.database import get_db
from app.models import User, SensorReading, Alert, AdviceLog, ResourceLog
from app.schemas import DashboardMetrics, SensorResponse, AlertResponse, WeatherResponse, ResourceSummary
from app.security import verify_token
from app.services import weather_service, resource_service
from datetime import date, timedelta, datetime
import asyncio

router = APIRouter()


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get aggregated metrics for dashboard"""

    # Get user
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get latest sensor reading
    sensor_result = await db.execute(
        select(SensorReading)
        .where(SensorReading.user_id == user_id)
        .order_by(desc(SensorReading.timestamp))
        .limit(1)
    )
    latest_sensor = sensor_result.scalar_one_or_none()

    # Run weather and resource fetch in parallel
    # Use Mumbai coordinates if user has no location set
    lat = user.location_lat or 19.0760  # Mumbai latitude
    lng = user.location_lng or 72.8777  # Mumbai longitude
    
    weather_data, resource_summary = await asyncio.gather(
        weather_service.get_weather_data(lat, lng),
        resource_service.get_resource_summary(user_id, db, 30),
        return_exceptions=True
    )
    
    # Handle exceptions gracefully
    if isinstance(weather_data, Exception):
        print(f"[WARNING] Weather error: {weather_data}")
        weather_data = None

    if isinstance(resource_summary, Exception):
        print(f"[WARNING] Resource error: {resource_summary}")
        resource_summary = {
            "total_water_used_liters": 0,
            "total_water_saved_liters": 0,
            "total_fertilizer_used_grams": 0,
            "total_cost_rupees": 0,
            "total_energy_kwh": 0,
            "water_budget_liters": 50000,
            "water_usage_percentage": 0,
            "status": "OK",
            "message": "No data yet"
        }
    
    # Get recent alerts (last 5)
    alerts_result = await db.execute(
        select(Alert)
        .where(Alert.user_id == user_id)
        .order_by(desc(Alert.timestamp))
        .limit(5)
    )
    recent_alerts = alerts_result.scalars().all()
    
    # Get latest advice
    advice_result = await db.execute(
        select(AdviceLog)
        .where(AdviceLog.user_id == user_id)
        .order_by(desc(AdviceLog.timestamp))
        .limit(1)
    )
    latest_advice = advice_result.scalar_one_or_none()
    
    return DashboardMetrics(
        current_sensor_data=SensorResponse.from_orm(latest_sensor) if latest_sensor else None,
        weather=WeatherResponse(**weather_data) if weather_data else None,
        resource_summary=ResourceSummary(**resource_summary),
        recent_alerts=[AlertResponse.from_orm(a) for a in recent_alerts],
        latest_advice=None
    )


@router.get("/trends", response_model=dict)
async def get_dashboard_trends(
    days: int = 7,
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get trend data for charts"""

    cutoff = datetime.utcnow() - timedelta(days=days)

    # Get sensor readings trend (sampled to avoid too many points)
    sensor_result = await db.execute(
        select(SensorReading)
        .where(
            SensorReading.user_id == user_id,
            SensorReading.timestamp >= cutoff
        )
        .order_by(SensorReading.timestamp)
    )
    sensors = sensor_result.scalars().all()

    # Sample data for charts (max 100 points)
    step = max(1, len(sensors) // 100)
    sampled = sensors[::step]

    sensor_trend = [
        {
            "timestamp": s.timestamp.isoformat(),
            "temperature": round(s.temperature or 0, 1),
            "humidity": round(s.humidity or 0, 1),
            "soil_moisture": round(s.soil_moisture_root or 0, 1)
        }
        for s in sampled
    ]

    # Get resource usage trend
    resource_result = await db.execute(
        select(ResourceLog)
        .where(
            ResourceLog.user_id == user_id,
            ResourceLog.date >= cutoff.date()
        )
        .order_by(ResourceLog.date)
    )
    resources = resource_result.scalars().all()

    resource_trend = [
        {
            "date": r.date.isoformat(),
            "water_used": round(r.water_used_liters or 0, 1),
            "water_saved": round(r.water_saved_liters or 0, 1),
            "fertilizer_used": round(r.fertilizer_used_grams or 0, 1)
        }
        for r in resources
    ]

    return {
        "sensor_trend": sensor_trend,
        "resource_trend": resource_trend,
        "period_days": days,
        "total_readings": len(sensors)
    }
