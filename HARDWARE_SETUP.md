# 🌾 KrishiDrishti - Hardware Setup Guide

## 📦 What You Need

### Hardware Components
- **Arduino with WiFi**: ESP8266 (NodeMCU) or ESP32
- **DHT11 Sensor**: Temperature & Humidity
- **Soil Moisture Sensor**: Capacitive type (recommended over resistive)
- **Rain Sensor Module**: Digital + Analog output
- **Jumper Wires**: Male-to-Female
- **Breadboard**: For prototyping

### Software Requirements
- Arduino IDE (with ESP8266/ESP32 board support)
- Libraries:
  - `ArduinoJson` (Install via Library Manager)
  - `DHT sensor library` by Adafruit

---

## 🔧 Step-by-Step Setup

### Step 1: Wire the Sensors

```
ESP8266/ESP32 Pin Mapping:
┌─────────────────────────────────────────┐
│          SENSOR WIRING                   │
├─────────────────────────────────────────┤
│ DHT11:                                  │
│   VCC  → 5V (or 3.3V for ESP32)        │
│   GND  → GND                            │
│   DATA → GPIO 2 (D4)                   │
│                                         │
│ Soil Moisture:                          │
│   VCC  → 5V (or 3.3V)                  │
│   GND  → GND                            │
│   AOUT → A0 (Analog Input)             │
│                                         │
│ Rain Sensor:                            │
│   VCC  → 5V (or 3.3V)                  │
│   GND  → GND                            │
│   DOUT → GPIO 3 (RX)                   │
│   AOUT → A1 (if available)             │
└─────────────────────────────────────────┘
```

### Step 2: Install Arduino IDE & Libraries

1. **Download Arduino IDE**: https://www.arduino.cc/en/software
2. **Install ESP8266 Board**:
   - File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Tools → Board → Boards Manager → Search "ESP8266" → Install

3. **Install Libraries**:
   - Sketch → Include Library → Manage Libraries
   - Search and install:
     - `ArduinoJson` by Benoit Blanchon
     - `DHT sensor library` by Adafruit

### Step 3: Calibrate Soil Moisture Sensor

1. Upload `calibrate_sensors.ino` to your Arduino
2. Open Serial Monitor (115200 baud)
3. **Hold sensor in air** for 10 seconds → Note the "DRY VALUE"
4. **Dip sensor in water** for 10 seconds → Note the "WET VALUE"
5. Update these values in `sensor_node.ino`:
   ```cpp
   const int SOIL_MOISTURE_DRY = 800;  // Your dry value
   const int SOIL_MOISTURE_WET = 300;  // Your wet value
   ```

### Step 4: Configure sensor_node.ino

Open `arduino/sensor_node.ino` and update:

```cpp
// WiFi Credentials
const char* WIFI_SSID = "Your_WiFi_Name";
const char* WIFI_PASSWORD = "Your_WiFi_Password";

// Backend API (Your computer's IP on same network)
const char* BACKEND_HOST = "192.168.1.100";  // Find with 'ipconfig' on Windows
const int BACKEND_PORT = 8000;

// Authentication Token (get from backend after login)
const char* USER_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
```

**To get your JWT token:**
1. Login to KrishiDrishti: http://localhost:5173
2. Phone: `+919876543210`
3. OTP: `123456`
4. Open browser console (F12) and run:
   ```javascript
   console.log(localStorage.getItem('token'))
   ```
5. Copy the token to `USER_AUTH_TOKEN` in the Arduino code

**To find your computer's IP:**
```bash
# Windows
ipconfig

# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.100
```

### Step 5: Upload to Arduino

1. Connect Arduino via USB
2. Select correct board: Tools → Board → ESP8266/ESP32
3. Select correct port: Tools → Port → COMx
4. Click Upload (→ button)
5. Open Serial Monitor (115200 baud)
6. You should see:
   ```
   🌾 KrishiDrishti - Smart Farming Sensor Node
   📡 Connecting to WiFi: Your_WiFi_Name
   ✅ WiFi connected!
   📍 IP Address: 192.168.1.150
   
   ✅ Setup complete! Starting sensor readings...
   📊 Reading sensors...
   🌡️  Temperature: 28.5 °C
   💧 Humidity: 65.2 %
   🌱 Soil Moisture: 520 ADC (58.0%)
   🌧️  Rain: NO
   📤 Sending data to: http://192.168.1.100:8000/api/sensors
   ✅ Response: 201
   ```

---

## 🚀 Start the Complete System

### 1. Start Backend
```bash
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start Frontend
```bash
cd D:\Himanshu_Project\KrishiDrishti\frontend
npm run dev
```

### 3. Ensure Ollama is Running
```bash
ollama serve
# In another terminal:
ollama list  # Should show qwen2.5vl:3b
```

### 4. Login & Test
1. Open http://localhost:5173
2. Login with:
   - Phone: `+919876543210`
   - OTP: `123456`
3. Go to Dashboard → You should see **real sensor data**!
4. Go to AI Advice → Ask questions like:
   - "Should I irrigate now?"
   - "What's the soil condition?"
   - "Is it going to rain?"

---

## 🎯 How It Works

```
┌─────────────┐
│  ARDUINO    │
│  + Sensors  │
└──────┬──────┘
       │ HTTP POST every 60 seconds
       │ {temperature, humidity, soil_moisture, rain}
       ▼
┌─────────────────┐
│  FastAPI Backend │
│  (SQLite DB)     │
└──────┬──────────┘
       │ Stores readings
       │ Retrieves for AI context
       ▼
┌─────────────────────┐
│  Ollama Qwen 2.5    │
│  + RAG (ChromaDB)   │
└──────┬──────────────┘
       │ Structured advice
       ▼
┌──────────────────┐
│  React Frontend  │
│  Dashboard/Chat  │
└──────────────────┘
```

---

## 🐛 Troubleshooting

### Arduino can't connect to WiFi
- Check SSID and password (case-sensitive)
- Ensure 2.4GHz WiFi (ESP8266 doesn't support 5GHz)
- Check firewall on your computer allows port 8000

### Backend not receiving data
- Verify `BACKEND_HOST` is correct (your computer's IP)
- Check Windows Firewall allows port 8000
- Test with curl:
  ```bash
  curl -X POST http://localhost:8000/api/sensors \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"temperature":28.5,"humidity":65.2,"soil_moisture_root":520,"rain_detected":false}'
  ```

### Token expired
- Tokens last 24 hours
- Re-login to get new token
- Update `USER_AUTH_TOKEN` in Arduino code

### Sensor readings seem wrong
- Run calibration tool first
- Check wiring connections
- DHT11 needs 3-5 seconds between readings (code handles this)

---

## 📊 Next Steps After Hardware Works

1. **Add more sensors**:
   - pH sensor (analog)
   - Ultrasonic sensor for water tank level
   - Light intensity (LDR or BH1750)

2. **Improve accuracy**:
   - Take multiple readings and average
   - Add sensor error handling
   - Implement deep sleep for battery operation

3. **Production deployment**:
   - Use permanent JWT tokens
   - Add device authentication
   - Set up cloud backend

---

## 💡 Pro Tips

- **Capacitive soil moisture sensors** last longer than resistive (no corrosion)
- Place soil moisture sensor at **root depth** (10-15cm for most crops)
- Mount DHT11 in **shade** with airflow (not in direct sun)
- Position rain sensor **horizontally** and clear of obstructions
- Update sensor readings every **1-5 minutes** for best AI advice

---

**Ready to start? Follow the steps above and your smart farming system will be live!** 🌾🤖
