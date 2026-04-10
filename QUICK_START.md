# 🚀 KrishiDrishti - Quick Start Guide (Hardware + AI Complete Setup)

## ✅ YOUR TEST CREDENTIALS

**Login Details:**
- 📱 Phone: `+919876543210`
- 🔐 OTP: `123456`
- 👤 User: Rajesh Kumar
- 🌾 Crop: Wheat (5 acres)
- 📍 Location: Nagpur, Maharashtra

---

## 📋 STEP-BY-STEP SETUP

### 1️⃣ Start All Services

**Terminal 1 - Backend:**
```bash
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd D:\Himanshu_Project\KrishiDrishti\frontend
npm run dev
```

**Terminal 3 - Ollama (AI Model):**
```bash
ollama serve
# Verify model is loaded:
ollama list
# Should show: qwen2.5vl:3b
```

### 2️⃣ Login to Get Token

1. Open browser: http://localhost:5173
2. Login with phone + OTP above
3. Open browser console (F12)
4. Run: `console.log(localStorage.getItem('token'))`
5. **Copy this token** - you'll need it for Arduino

### 3️⃣ Find Your Computer's IP Address

```bash
ipconfig
```
Look for "IPv4 Address" under WiFi adapter (e.g., `192.168.1.100`)

### 4️⃣ Configure Arduino

1. Open `arduino/sensor_node.ino` in Arduino IDE
2. Update these values:
   ```cpp
   const char* WIFI_SSID = "Your_WiFi_Name";
   const char* WIFI_PASSWORD = "Your_WiFi_Password";
   const char* BACKEND_HOST = "192.168.1.XXX";  // Your computer's IP
   const char* USER_AUTH_TOKEN = "YOUR_TOKEN_HERE";  // From browser
   ```

3. **Install required libraries** (Sketch → Include Library → Manage Libraries):
   - `ArduinoJson` by Benoit Blanchon
   - `DHT sensor library` by Adafruit

4. **Calibrate soil moisture sensor** (optional but recommended):
   - Upload `arduino/calibrate_sensors.ino`
   - Follow serial monitor instructions
   - Update `SOIL_MOISTURE_DRY` and `SOIL_MOISTURE_WET` values

5. Upload to ESP8266/ESP32

### 5️⃣ Verify Everything Works

**Check sensor data is being received:**
```bash
# After Arduino starts sending, check backend logs
# You should see POST /api/sensors/ responses with 201 status
```

**Test dashboard:**
1. Refresh http://localhost:5173/dashboard
2. You should see **real sensor data** from your Arduino!

**Test AI Chat:**
1. Go to http://localhost:5173/advice
2. Ask: "Should I irrigate now?"
3. AI will analyze your **real sensor data** + weather + crop knowledge
4. Get structured advice with recommendations

---

## 🔧 TROUBLESHOOTING

### Arduino won't connect to WiFi
- ✅ Check SSID/password (case-sensitive)
- ✅ Use 2.4GHz WiFi (ESP8266 doesn't support 5GHz)
- ✅ Check serial monitor for error messages

### Backend not receiving sensor data
- ✅ Verify `BACKEND_HOST` is correct (your computer's IP)
- ✅ Windows Firewall: Allow port 8000
- ✅ Test with curl:
  ```bash
  curl -X POST http://localhost:8000/api/sensors/ ^
    -H "Content-Type: application/json" ^
    -H "Authorization: Bearer YOUR_TOKEN" ^
    -d "{\"temperature\":28.5,\"humidity\":65.2,\"soil_moisture_root\":520,\"rain_detected\":false}"
  ```

### Token expired (after 24 hours)
- ✅ Just re-login to get new token
- ✅ Update token in Arduino code

### AI Chat not responding
- ✅ Check Ollama is running: `ollama list`
- ✅ Should show `qwen2.5vl:3b`
- ✅ If not, run: `ollama pull qwen2.5vl:3b`

### Dashboard shows no data
- ✅ Check Arduino serial monitor - should show "✅ Response: 201"
- ✅ Check backend terminal - should show POST requests
- ✅ Try refreshing the page

---

## 📡 ARDUINO PIN REFERENCE

```
ESP8266/ESP32 Wiring:
┌──────────────────────────────┐
│ DHT11:                       │
│   VCC → 5V (or 3.3V)        │
│   GND → GND                  │
│   DATA → GPIO 2             │
│                              │
│ Soil Moisture:               │
│   VCC → 5V (or 3.3V)        │
│   GND → GND                  │
│   AOUT → A0                 │
│                              │
│ Rain Sensor:                 │
│   VCC → 5V (or 3.3V)        │
│   GND → GND                  │
│   DOUT → GPIO 3             │
│   AOUT → A1 (optional)      │
└──────────────────────────────┘
```

---

## 🎯 WHAT HAPPENS WHEN IT ALL WORKS

```
Every 60 seconds:
┌──────────────┐
│  ARDUINO     │
│  + Sensors   │
│  DHT11       │
│  Soil        │
│  Rain        │
└──────┬───────┘
       │ HTTP POST
       │ {temp: 32.5, humidity: 68.2, soil: 580, rain: false}
       ▼
┌──────────────────┐
│  FastAPI Backend  │
│  Port 8000        │
│  Saves to SQLite  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  React Dashboard  │
│  Shows live data  │
└──────┬───────────┘
       │
       ▼ (when you ask a question)
┌──────────────────────┐
│  Ollama Qwen 2.5     │
│  + RAG ChromaDB      │
│  Context:             │
│   - Sensor data       │
│   - Weather           │
│   - Crop knowledge    │
│   - History           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  AI Advice           │
│  💧 IRRIGATE NOW     │
│  Reason: ...         │
│  Action: 500L/acre   │
│  Risk: ...           │
│  Confidence: 85%     │
└──────────────────────┘
```

---

## 🌟 FEATURES NOW WORKING

✅ **Real-time sensor data** from your Arduino  
✅ **Weather integration** (mock data, or real with API key)  
✅ **RAG-powered AI** with crop knowledge base  
✅ **Contextual advice** based on YOUR farm conditions  
✅ **Dashboard analytics** with live charts  
✅ **Alert system** for critical conditions  
✅ **Multi-language** support (EN/HI/MR)  
✅ **Advice history** tracking in database  

---

## 🚀 READY TO GO!

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 5173
3. ✅ Ollama serving qwen2.5vl:3b
4. ✅ Database seeded with test user + sample data
5. ✅ Arduino code ready to upload
6. ✅ All API endpoints working

**Next:** Upload Arduino code and watch your dashboard come alive! 🌾🤖
