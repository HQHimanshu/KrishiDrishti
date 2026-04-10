"""Test Ollama JSON generation directly"""
import requests
import json

prompt = """You are an AI assistant. Respond with JSON ONLY:
{
  "test": "ok",
  "message": "Hello"
}
"""

print("Testing Ollama JSON generation...")
try:
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "num_ctx": 4096,
            "num_predict": 128
        }
    }, timeout=60)
    
    print("Status:", r.status_code)
    data = r.json()
    resp_text = data.get("response", "")
    print("Response:", resp_text[:500])
    
    # Try to parse as JSON
    try:
        parsed = json.loads(resp_text)
        print("Parsed JSON successfully!")
    except:
        # Try to extract JSON
        start = resp_text.find('{')
        end = resp_text.rfind('}') + 1
        if start >= 0 and end > start:
            extracted = json.loads(resp_text[start:end])
            print("Extracted JSON successfully!")
        else:
            print("Failed to parse JSON")
            
except Exception as e:
    print("Error:", e)
