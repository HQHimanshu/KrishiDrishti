import asyncio
import sys
sys.path.insert(0, '.')

async def test():
    from app.services import ollama_service
    
    # Test with minimal context
    result = await ollama_service.get_farming_advice(
        user_id=1,
        question="Should I water my crops?",
        sensor_data={"temperature": 30, "humidity": 60, "soil_moisture_root": 400},
        crop_type="wheat",
        language="en",
        weather_data=None,
        crop_health_history=None,
        advice_history=None
    )
    
    print("Success!")
    print(f"Recommendation: {result.get('recommendation')}")
    print(f"Reason: {result.get('reason', '')[:100]}")

asyncio.run(test())
