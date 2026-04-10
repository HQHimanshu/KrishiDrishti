# 🎯 SEE YOUR LIVE DASHBOARD DATA - 3 Simple Steps

## ✅ Status: Backend is Working Perfectly!
- Database has **3393+ sensor readings**
- USB Bridge is receiving live data
- All API endpoints are functional
- **You just need to authenticate in the browser**

---

## 🚀 HOW TO SEE YOUR DATA (Choose One Method)

### Method 1: Quick Console Command (30 seconds)

1. **Open Browser**: http://localhost:5173

2. **Open Console**: Press `F12` → Click "Console" tab

3. **Paste This Command** (then press Enter):
```javascript
localStorage.setItem("token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzc1OTI2MjE4fQ.WnJ8kfZMkFxkAbOZLSDiNYUBBDg_R_FHd7PzFZoJ7Gc")
```

4. **Refresh Page**: Press `F5`

5. **Go to Dashboard**: You should see live sensor data!

---

### Method 2: Login Normally (1 minute)

1. **Open Browser**: http://localhost:5173

2. **Click Login** (if not already on login page)

3. **Enter Phone**: `8626081052`

4. **Enter OTP**: `123456`

5. **Dashboard should load automatically**

---

### Method 3: Use Script (1 minute)

1. **Open PowerShell** in project folder

2. **Run**: 
```powershell
.\quick_login.bat
```

3. **Copy the token** it shows

4. **Open Browser**: http://localhost:5173

5. **Press F12** → Console tab

6. **Paste**: 
```javascript
localStorage.setItem("token", "YOUR_TOKEN_HERE")
```

7. **Refresh page**

---

## 📊 What You Should See

### Dashboard Page
✅ 6 sensor cards with LIVE data:
- 🌡️ Temperature: ~31°C
- 💧 Humidity: ~53%
- 🌊 Soil Moisture: ~668 ADC
- 🧪 pH Level: ~6.8
- 🌧️ Rain Detection: Active
- 💦 Water Tank: 75%

### Analytics Page
✅ Charts showing historical data:
- 440 readings in last 24 hours
- Line charts for Temperature, Humidity, Soil Moisture
- Table view with timestamps

---

## ❓ Still Not Working?

### Check 1: Is Token Set?
Open browser console (F12) and run:
```javascript
console.log(localStorage.getItem("token"))
```
Should show your token string (not null)

### Check 2: Is Backend Running?
Open browser and visit: http://localhost:8000/health
Should show: `{"status":"healthy","environment":"development"}`

### Check 3: Is Frontend Running?
Open browser and visit: http://localhost:5173
Should show the KrishiDrishti app

### Check 4: Any Console Errors?
Open browser console (F12) and look for red errors
Common issues:
- `401 Unauthorized` → Token expired or not set
- `Network Error` → Backend not running
- `CORS Error` → Backend CORS misconfigured

---

## 🔄 If Token Expires (After 60 minutes)

Just logout and login again, or run:
```powershell
.\quick_login.bat
```

And use the new token.

---

**Quick URLs:**
- Dashboard: http://localhost:5173/dashboard
- Analytics: http://localhost:5173/analytics
- Backend API: http://localhost:8000/docs

---

**Last Updated**: 2026-04-10 22:50 UTC  
**Database Readings**: 3393+ and counting!
