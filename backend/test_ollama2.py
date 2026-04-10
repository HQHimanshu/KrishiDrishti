import asyncio
import sys
sys.path.insert(0, '.')

async def test():
    from app.services import ollama_service
    
    print("Testing ollama service directly...")
    result = await ollama_service.get_farming_advice(
        user_id=1,
        question="Should I water my crops?",
        sensor_data={"temperature": 30, "humidity": 60, "soil_moisture_root": 400},
        crop_type="wheat",
        language="en"
    )
    print("Result:", result)

asyncio.run(test())
