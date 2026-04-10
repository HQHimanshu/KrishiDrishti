# 🎯 KrishiDrishti - Dashboard & Analytics Fixed!

## ✅ What's Working

### Backend Server (Port 8000)
- ✅ FastAPI server is running
- ✅ Database has **3092+ sensor readings**
- ✅ All API endpoints functional
- ✅ USB Bridge sending data every ~5 seconds

### Sensor Data Status
- ✅ **Temperature**: 32.9°C
- ✅ **Humidity**: 61.6%
- ✅ **Soil Moisture**: 667 ADC
- ✅ **pH Level**: 6.8
- ✅ **Rain Detection**: Yes/No working
- ✅ **Water Tank**: 75%

### Dashboard & Analytics APIs
- ✅ `/api/dashboard/metrics` - Returns current sensor data
- ✅ `/api/dashboard/trends` - Returns historical data (1337 readings in last 24h)
- ✅ `/api/sensors/latest` - Returns latest reading
- ✅ `/api/sensors/history` - Returns historical readings

## 🔧 How to View Dashboard & Analytics

### Option 1: Quick Start (Recommended)

1. **Run the complete startup script:**
   ```powershell
   .\start_all.bat
   ```
   This launches:
   - Backend API Server
   - USB Serial Bridge
   - Frontend Dev Server

2. **Get authenticated:**
   ```powershell
   .\get_token.bat
   ```
   This gives you a fresh token to paste in browser console

3. **Open the dashboard:**
   - Navigate to: http://localhost:5173
   - Login with:
     - Phone: `+919876543210`
     - OTP: `123456`

4. **View your data:**
   - **Dashboard** → Shows live sensor data, weather, resources
   - **Analytics** → Shows historical charts and tables

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - USB Bridge:**
```powershell
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe usb_serial_bridge.py
```

**Terminal 3 - Frontend:**
```powershell
cd D:\Himanshu_Project\KrishiDrishti\frontend
npm run dev
```

## 📊 What You'll See

### Dashboard Page
- **Sensor Grid**: 6 cards showing:
  - Temperature (°C)
  - Humidity (%)
  - Soil Moisture (%)
  - pH Level
  - Rain Status
  - Water Tank Level

- **Weather Widget**: Current weather + forecast
- **Resource Metrics**: Water, fertilizer, cost tracking
- **Recent Alerts**: Critical warnings and info

### Analytics Page
- **Chart View**: Line charts showing trends over time
  - Temperature trend
  - Humidity trend
  - Soil moisture trend

- **Table View**: Tabular data with timestamps
- **Time Selectors**: 1 day, 3 days, 7 days

## 🐛 If Dashboard Shows "No Sensor Data"

### Check 1: Is Backend Running?
```powershell
curl http://localhost:8000/health
```
Should return: `{"status":"healthy","environment":"development"}`

### Check 2: Is Frontend Authenticated?
1. Open browser console (F12)
2. Run: `console.log(localStorage.getItem('token'))`
3. If `null`, you need to login or run `get_token.bat`

### Check 3: Is USB Bridge Sending Data?
Look at the USB Bridge terminal - should show:
```
[Sensor Reading #1234] 16:18:33
  Temperature: 32.9°C
  Humidity: 61.6%
  Soil Moisture: 667 ADC
  pH Level: 6.8
  Rain: No
  Water Tank: 75%
  
  [OK] Sent (ID: 3092)
```

### Check 4: Database Has Data?
```powershell
cd D:\Himanshu_Project\KrishiDrishti\backend
venv\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('krishidrishti.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM sensor_readings'); print('Total readings:', cursor.fetchone()[0])"
```

## 🔑 Quick Token Refresh

If your token expires (after 60 minutes), you have 3 options:

### Method 1: Use Script
```powershell
.\get_token.bat
```

### Method 2: Browser Console
1. Login at http://localhost:5173
2. Open console (F12)
3. Token is automatically stored

### Method 3: API Call
```bash
curl -X POST http://localhost:8000/api/auth/send-otp -H "Content-Type: application/json" -d "{\"phone\": \"+919876543210\"}"
curl -X POST http://localhost:8000/api/auth/verify-otp -H "Content-Type: application/json" -d "{\"phone\": \"+919876543210\", \"otp_code\": \"123456\"}"
```

## 📈 System Architecture

```
Arduino Sensors (COM6)
       ↓ USB Serial
USB Bridge (Python)
       ↓ HTTP POST every 5s
FastAPI Backend (Port 8000)
       ↓ SQLite Database
       ↓
React Frontend (Port 5173)
       ↓ Polls every 5s
Dashboard & Analytics Pages
```

## 🎯 Current Data Flow Status

| Component | Status | Details |
|-----------|--------|---------|
| Arduino Hardware | ✅ Running | Sending data on COM6 |
| USB Bridge | ✅ Running | Parsing & forwarding data |
| Backend API | ✅ Running | Accepting & storing data |
| Database | ✅ Active | 3092+ readings |
| Frontend Server | ✅ Running | React dev server |
| Dashboard Page | ✅ Ready | Will show data when authenticated |
| Analytics Page | ✅ Ready | Will show charts when authenticated |

## 🚀 Next Steps

1. **If not already logged in:**
   - Open http://localhost:5173
   - Login with phone `+919876543210` and OTP `123456`
   - Navigate to Dashboard or Analytics

2. **If already logged in but showing "No data":**
   - Open browser console (F12)
   - Check for 401 errors
   - If token expired, logout and login again

3. **To monitor live data:**
   - Keep all 3 terminals open
   - Watch USB Bridge terminal for incoming readings
   - Refresh Dashboard to see latest data

## 📝 Important URLs

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 💡 Pro Tips

- Dashboard auto-refreshes every 5 seconds
- Analytics shows up to 7 days of history
- Use Debug button on Dashboard to see raw API response
- USB Bridge auto-reconnects on token expiry

---

**Status**: ✅ **ALL SYSTEMS OPERATIONAL**
**Last Updated**: 2026-04-10 16:18 UTC
