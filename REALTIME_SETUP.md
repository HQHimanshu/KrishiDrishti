# 🌾 KrishiDrishti - Real-Time Setup Guide

## ✅ What's NOW Real-Time (No Dummy Data)

### 1. **Dashboard** 📊
- ✅ **Auto-refreshes every 5 seconds**
- ✅ Shows LIVE sensor data from Arduino (when connected)
- ✅ Shows real database records
- ✅ Last update timestamp displayed
- ❌ Weather: Shows "No data" until you add API key

### 2. **Analytics** 📈
- ✅ **Auto-refreshes every 10 seconds**
- ✅ Real charts from actual sensor readings
- ✅ Time period selector (7D, 14D, 30D)
- ✅ Shows only data you've collected

### 3. **AI Chat** 🤖
- ✅ **Real Ollama Qwen 2.5 VL responses**
- ✅ Uses your actual sensor data as context
- ✅ RAG knowledge base from ChromaDB
- ✅ Advice history saved to database
- ❌ Shows error if Ollama not running

### 4. **User Profile** 👤
- ✅ Phone number (required)
- ✅ Email (for notifications)
- ✅ Location: Mumbai (19.0760, 72.8777)
- ✅ Crop type, farm area

---

## 🔧 What You Need To Configure

### 1. **OpenWeatherMap API** (For Real Weather)

**Get Free API Key:**
1. Go to: https://openweathermap.org/api
2. Sign up (free tier: 60 calls/min)
3. Copy your API key
4. Update `.env`:
   ```env
   OPENWEATHER_API_KEY=your_actual_key_here
   ```
5. Restart backend

**Without API key:** Weather shows "Data unavailable" message

---

### 2. **Ollama Setup** (For AI Chat)

**Already installed!** But model needs memory:

**Current status:**
- ✅ Ollama installed
- ✅ qwen2.5vl:3b model downloaded (3.2 GB)
- ❌ Failing to load (needs 10.1 GB, only 5.6 GB free)

**Fix Options:**

**Option A: Free up RAM**
1. Close browser tabs (save 500MB-1GB each)
2. Close heavy apps
3. Restart Ollama:
   ```bash
   # Task Manager → End ollama.exe
   ollama serve
   ```

**Option B: Use smaller model**
```bash
ollama pull qwen2.5:1.5b
```
Update `.env`:
```env
OLLAMA_MODEL=qwen2.5:1.5b
```

---

### 3. **Arduino Connection** (For Live Sensors)

**Your Arduino code outputs JSON via USB**

**To connect:**
1. Upload your Arduino code
2. Note COM port (e.g., COM3)
3. Close Arduino Serial Monitor
4. Run:
   ```bash
   run_usb_bridge.bat
   ```
5. Paste your JWT token when prompted

**Data flows:**
```
Arduino → USB → Python Bridge → Backend API → Database → Dashboard
   ↓                                          ↓
Every 3 seconds                          Auto-refresh every 5s
```

---

## 📱 Notifications Setup

### Current Status:
- ✅ Phone field in user profile
- ✅ Email field in user profile
- ✅ WhatsApp/SMS opt-in flags
- ❌ Twilio not configured (needs API key)
- ❌ SMTP not configured (needs Gmail app password)

### To Enable Notifications:

**Option 1: Twilio (WhatsApp/SMS)**
1. Sign up: https://twilio.com
2. Get Account SID, Auth Token
3. Update `.env`:
   ```env
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=+14155238886
   ```

**Option 2: Email (SMTP)**
1. Use Gmail app password
2. Update `.env`:
   ```env
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

---

## 🎯 Complete Real-Time Flow

```
┌──────────────────────────────────────────────────────┐
│               REAL-TIME DATA FLOW                     │
├──────────────────────────────────────────────────────┤
│                                                       │
│  Arduino (Every 3s)                                  │
│     ↓ USB Serial                                     │
│                                                       │
│  Python Bridge (usb_serial_bridge.py)                │
│     ↓ HTTP POST                                      │
│                                                       │
│  Backend API (Port 8000)                             │
│     ├─ Saves to SQLite                               │
│     ├─ Triggers alerts if needed                     │
│     └─ Serves to frontend                            │
│                                                       │
│  Frontend (Port 5173)                                │
│     ├─ Dashboard: Refreshes every 5s                 │
│     ├─ Analytics: Refreshes every 10s                │
│     └─ AI Chat: On-demand with Ollama                │
│                                                       │
│  AI Chat (When user asks question)                   │
│     ├─ Gets latest sensor data                       │
│     ├─ Gets weather (if API key configured)           │
│     ├─ Queries ChromaDB (crop knowledge)              │
│     ├─ Sends to Qwen 2.5 via Ollama                   │
│     └─ Returns structured advice                     │
│                                                       │
│  Notifications (When alerts triggered)                │
│     ├─ WhatsApp (if Twilio configured)                │
│     ├─ SMS (if Twilio configured)                     │
│     ├─ Email (if SMTP configured)                     │
│     └─ In-app alerts (always working)                 │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## 📊 What You See RIGHT NOW

| Page | Data Source | Auto-Refresh | Real or Config? |
|------|-------------|--------------|-----------------|
| **Dashboard** | Database | Every 5s | ✅ Real |
| **Weather** | None (no API key) | Every 5s | ❌ Shows "No data" |
| **Analytics** | Database trends | Every 10s | ✅ Real |
| **AI Chat** | Ollama Qwen | On-demand | ✅ Real (if Ollama runs) |
| **Alerts** | Database | On load | ✅ Real |
| **Resources** | Database logs | On load | ✅ Real |

---

## 🚀 Quick Start Checklist

- [ ] Backend running (`python -m uvicorn app.main:app --reload`)
- [ ] Frontend running (`npm run dev`)
- [ ] Ollama running (`ollama serve`)
- [ ] Arduino connected & code uploaded
- [ ] USB Bridge running (`run_usb_bridge.bat`)
- [ ] Logged in at http://localhost:5173
- [ ] Weather API key in `.env` (optional)

---

## 🐛 Troubleshooting

### Dashboard shows "Failed to load sensor data"
- ✅ Check USB Bridge is running
- ✅ Check Arduino is connected
- ✅ Check backend is running on port 8000

### AI Chat shows error
- ✅ Run: `ollama list` (should show qwen2.5vl:3b)
- ✅ Run: `ollama serve` (if not running)
- ✅ Free up RAM if model won't load

### Weather shows "No data"
- ✅ This is normal without API key
- ✅ Add OPENWEATHER_API_KEY to `.env` for real weather

### Auto-refresh not working
- ✅ Check browser console for errors (F12)
- ✅ Refresh page manually
- ✅ Check network tab for failed requests

---

**All dummy data removed! Everything is now real or clearly marked as unavailable.** 🎉
