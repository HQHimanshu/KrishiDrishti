from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models import User, AdviceLog
from app.schemas import AdviceRequest, AdviceResponse, AdviceHistoryItem
from app.security import verify_token
from app.services import ollama_service, weather_service

router = APIRouter()


@router.post("/", response_model=AdviceResponse)
async def get_advice(
    request: AdviceRequest,
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered farming advice using RAG + Qwen with full context"""

    # Get user data
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Use provided sensor_data or latest from database
    sensor_data = request.sensor_data
    if not sensor_data:
        from app.models import SensorReading
        from sqlalchemy import desc

        sensor_result = await db.execute(
            select(SensorReading)
            .where(SensorReading.user_id == user_id)
            .order_by(desc(SensorReading.timestamp))
            .limit(1)
        )
        latest_reading = sensor_result.scalar_one_or_none()

        if latest_reading:
            sensor_data = {
                "temperature": latest_reading.temperature,
                "humidity": latest_reading.humidity,
                "soil_moisture_surface": latest_reading.soil_moisture_surface,
                "soil_moisture_root": latest_reading.soil_moisture_root,
                "ph_level": latest_reading.ph_level,
                "rain_detected": latest_reading.rain_detected,
                "water_tank_level": latest_reading.water_tank_level
            }

    # Get weather context
    weather_data = None
    try:
        lat = user.location_lat or 21.1458
        lng = user.location_lng or 79.0882
        weather_data = await weather_service.get_weather_data(lat, lng)
    except Exception as e:
        print(f"[WARNING] Weather context failed: {e}")

    # Get advice history for continuity
    advice_history_result = await db.execute(
        select(AdviceLog)
        .where(AdviceLog.user_id == user_id)
        .order_by(desc(AdviceLog.timestamp))
        .limit(5)
    )
    advice_history_logs = advice_history_result.scalars().all()
    
    advice_history = [
        {
            "timestamp": log.timestamp.isoformat(),
            "question": log.question,
            "recommendation": log.recommendation_type,
            "reason": log.answer[:100] if log.answer else ""
        }
        for log in advice_history_logs
    ]

    # Get crop health history (from advice logs and sensor trends)
    crop_health_history = {
        "crop_type": user.crop_type,
        "growth_stage": user.growth_stage if hasattr(user, 'growth_stage') else None,
        "recent_issues": []
    }

    # Check for recent critical alerts
    from app.models import Alert
    alerts_result = await db.execute(
        select(Alert)
        .where(Alert.user_id == user_id, Alert.type == "CRITICAL")
        .order_by(desc(Alert.timestamp))
        .limit(3)
    )
    critical_alerts = alerts_result.scalars().all()
    if critical_alerts:
        crop_health_history["recent_issues"] = [
            alert.message_en or alert.message for alert in critical_alerts
        ]

    # Get advice from AI with full context
    try:
        advice = await ollama_service.get_farming_advice(
            user_id=user_id,
            question=request.question,
            sensor_data=sensor_data or {},
            crop_type=user.crop_type,
            language=user.language or "en",
            weather_data=weather_data,
            crop_health_history=crop_health_history,
            advice_history=advice_history
        )
    except Exception as e:
        import traceback
        error_detail = f"AI service failed: {str(e)}"
        print(f"[ERROR] AI Advice Error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_detail)

    # Log the advice
    advice_log = AdviceLog(
        user_id=user_id,
        question=request.question,
        answer=advice.get("reason", "") + "\n" + advice.get("action", ""),
        context_used={
            "crop": user.crop_type,
            "sensor_data": sensor_data,
            "weather": bool(weather_data),
            "advice_history_count": len(advice_history)
        },
        confidence_score=advice.get("confidence_score"),
        language=advice.get("language", user.language or "en"),
        recommendation_type=advice.get("recommendation")
    )

    db.add(advice_log)
    await db.commit()
    await db.refresh(advice_log)

    return AdviceResponse(
        recommendation=advice.get("recommendation", "WAIT"),
        reason=advice.get("reason", ""),
        action=advice.get("action", ""),
        risk=advice.get("risk"),
        confidence_score=advice.get("confidence_score"),
        language=advice.get("language", "en"),
        context_sources=advice.get("context_sources"),
        optimization_tips=advice.get("optimization_tips"),
        estimated_impact=advice.get("estimated_impact"),
        sensor_context=sensor_data,
        weather_context=weather_data
    )


@router.get("/history", response_model=list[AdviceHistoryItem])
async def get_advice_history(
    limit: int = 20,
    user_id: int = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Get user's advice history"""
    
    result = await db.execute(
        select(AdviceLog)
        .where(AdviceLog.user_id == user_id)
        .order_by(desc(AdviceLog.timestamp))
        .limit(limit)
    )
    advice_logs = result.scalars().all()
    
    return [
        AdviceHistoryItem(
            id=log.id,
            question=log.question,
            answer=log.answer,
            timestamp=log.timestamp,
            recommendation_type=log.recommendation_type,
            language=log.language
        )
        for log in advice_logs
    ]
