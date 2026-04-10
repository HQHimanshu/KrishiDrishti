# 🌾 KrishiDrishti - USB Serial Setup Guide

## ✅ Your Setup

- **Arduino**: Connected via USB cable
- **Sensors**: DHT11, Soil Moisture, Rain, Water Level
- **Output**: JSON via Serial at 9600 baud
- **Backend**: Running on localhost:8000

---

## 🚀 QUICK START (3 Steps)

### Step 1: Login & Get Token

1. **Start Backend** (if not running):
   ```bash
   cd D:\Himanshu_Project\KrishiDrishti\backend
   venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend** (if not running):
   ```bash
   cd D:\Himanshu_Project\KrishiDrishti\frontend
   npm run dev
   ```

3. **Login**:
   - Open: http://localhost:5173
   - Phone: `+919876543210`
   - OTP: `123456`

4. **Get Token**:
   - Press `F12` → Console tab
   - Type: `localStorage.getItem('token')`
   - **Copy the token** (looks like: `eyJhbGci...`)

### Step 2: Connect Arduino

1. **Upload your Arduino code** (the one you already have)
2. **Note the COM port** (Tools → Port in Arduino IDE)
   - Usually: `COM3`, `COM4`, `COM5`, etc.
3. **Close Arduino Serial Monitor** (important - port will be in use!)

### Step 3: Run the USB Bridge

**Option A - Easy (Double-click)**:
1. Double-click: `run_usb_bridge.bat`
2. It will auto-detect your Arduino
3. Paste your JWT token when prompted
4. Done! Data will start flowing

**Option B - Command Line**:
```bash
cd D:\Himanshu_Project\KrishiDrishti
run_usb_bridge.bat --port COM3 --token YOUR_TOKEN_HERE
```

Replace `COM3` with your actual Arduino port.

---

## 📊 What You'll See

```
============================================================
🌾 KrishiDrishti - USB Serial Bridge
============================================================
📡 Arduino Port: COM3
🔗 Backend URL: http://localhost:8000/api/sensors/
⚡ Baud Rate: 9600
============================================================
✅ Connected to Arduino on COM3
📡 Listening for sensor data...

Press Ctrl+C to stop

============================================================
📊 Sensor Reading #1
============================================================
🌡️  Temperature: 28.5 °C  🟢 Normal
💧 Humidity:    65.2 %  🟢 Normal
🌱 Soil Moist:  58.0 %  🟢 Good
🌧️  Rain:       NO ☀️
💧 Water Tank: 75.0 %  🟢 Good
============================================================
  ✅ Sent to backend (ID: 170)

📈 Summary: 1 readings | 1 sent | 0 errors
```

---

## 🔍 Find Your Arduino COM Port

**Method 1 - Device Manager**:
1. Press `Win + X` → Device Manager
2. Expand "Ports (COM & LPT)"
3. Look for "Arduino Uno" or "USB Serial Device"
4. Note the COM number (e.g., COM3)

**Method 2 - Auto-detect**:
The bridge will auto-detect your Arduino. Just run it and it will show:
```
🔍 Scanning for Arduino...
  ✅ Found: COM3 - Arduino Uno
```

**Method 3 - Arduino IDE**:
1. Open Arduino IDE
2. Tools → Port
3. Note the COM port shown

---

## 🐛 Troubleshooting

### "Port is already in use" error
- ❌ **Cause**: Arduino Serial Monitor is open
- ✅ **Fix**: Close Serial Monitor and try again

### "Cannot connect to backend"
- ❌ **Cause**: Backend not running on port 8000
- ✅ **Fix**: Start backend first:
  ```bash
  cd D:\Himanshu_Project\KrishiDrishti\backend
  venv\Scripts\python.exe -m uvicorn app.main:app --reload
  ```

### "Token expired"
- ❌ **Cause**: JWT token expired (valid for 24 hours)
- ✅ **Fix**: Re-login and get new token from browser console

### "No data received"
- ❌ **Cause**: Arduino not uploading code or wrong baud rate
- ✅ **Fix**: 
  1. Verify Arduino code is uploaded
  2. Check baud rate matches (9600 in both places)
  3. Open Serial Monitor to verify JSON output

### JSON parse errors
- ❌ **Cause**: Corrupted serial data
- ✅ **Fix**: 
  1. Check USB cable connection
  2. Try different USB port
  3. Verify Arduino code outputs valid JSON

---

## 📝 Arduino Code Verification

Your Arduino should output JSON like this in Serial Monitor:

```json
{"temperature":28.5,"humidity":65.2,"soil_moisture":58.0,"rain_detection":12.5,"water_level":75.0,"timestamp":12345}
```

**To verify**:
1. Open Arduino IDE
2. Upload your code
3. Open Serial Monitor (9600 baud)
4. You should see JSON lines every 3 seconds

---

## 🎯 How It Works

```
┌──────────────┐
│  ARDUINO     │
│  + Sensors   │
│  (USB Cable) │
└──────┬───────┘
       │ Serial @ 9600 baud
       │ JSON output every 3 seconds
       ▼
┌──────────────────┐
│  USB BRIDGE      │
│  (Python Script) │
│  Reads serial    │
│  Parses JSON     │
└──────┬───────────┘
       │ HTTP POST
       │ Every 3 seconds
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
│  http://localhost:5173
└──────────────────┘
```

---

## ⚙️ Advanced Usage

**Run with custom settings**:
```bash
python usb_serial_bridge.py --port COM4 --token YOUR_TOKEN --baud 115200
```

**Available options**:
- `--port COMx` : Specify Arduino COM port
- `--token JWT` : JWT authentication token
- `--baud 9600` : Serial baud rate (default: 9600)
- `--help` : Show help message

---

## ✅ Checklist Before Running

- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 5173
- [ ] You have logged in and got a JWT token
- [ ] Arduino code is uploaded
- [ ] Arduino Serial Monitor is CLOSED
- [ ] You know the Arduino COM port
- [ ] USB cable is connected

**Once everything checks out, run `run_usb_bridge.bat` and you're good to go!** 🚀

---

## 📊 Verify Data is Flowing

1. **Check USB Bridge output**: Should show "✅ Sent to backend"
2. **Check backend logs**: Should show `POST /api/sensors/` requests
3. **Check dashboard**: Refresh http://localhost:5173/dashboard
4. You should see **real sensor readings** from your Arduino!

---

**Happy Farming!** 🌾🤖
