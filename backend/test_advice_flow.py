"""Test full AI advice flow"""
import asyncio
import httpx
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_advice():
    print("Testing AI advice flow...")
    
    # 1. Test Ollama call with simple farming prompt
    prompt = """You are KrishiDrishti AI. 
Current sensor data: {"temperature": 30, "humidity": 60, "soil_moisture": 400}
Question: Should I irrigate?
Respond with JSON ONLY:
{
  "recommendation": "WAIT",
  "reason": "Test",
  "action": "Wait",
  "risk": null,
  "confidence": 80
}
"""
    
    print("Calling Ollama...")
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:1.5b",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                    "format": "json",
                    "options": {"num_ctx": 4096, "num_predict": 512}
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                print("Raw response:", text[:200])
                
                # Try parsing
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    parsed = json.loads(text[start:end])
                    print("Parsed recommendation:", parsed.get("recommendation"))
                else:
                    print("No JSON found in response")
            else:
                print(f"Ollama error: {response.status_code} {response.text}")
                
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_advice())
