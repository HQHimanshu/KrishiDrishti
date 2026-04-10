# 🚀 KrishiDrishti - Quick Reference Card

## ⚡ Start Everything (PowerShell)

```powershell
# Start all 3 services at once
.\start_all.bat
```

## 🔑 Get Authentication Token

```powershell
# Generate fresh token (shows command to paste in browser)
.\get_token.bat
```

## 🌐 Important URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |
| **Dashboard** | http://localhost:5173/dashboard |
| **Analytics** | http://localhost:5173/analytics |

## 🔐 Login Credentials

- **Phone**: `8626081052` (or `+919876543210`)
- **OTP**: `123456` (always the same in dev mode)

## 📊 What's Running

```
┌─────────────────────────┐
│ Terminal 1: Backend     │ → Port 8000 (FastAPI)
│ Terminal 2: USB Bridge  │ → Reads Arduino COM6
│ Terminal 3: Frontend    │ → Port 5173 (React)
└─────────────────────────┘
```

## ✅ Quick Health Check

```powershell
# Check backend
curl http://localhost:8000/health

# Check frontend (should return HTML)
curl http://localhost:5173
```

## 🛑 Stop Services

Press `Ctrl+C` in each terminal window, or just close the windows.

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed (replace PID)
taskkill /F /PID <PID>
```

### Frontend won't start
```powershell
# Check if port 5173 is in use
netstat -ano | findstr :5173
```

### Token expired
```powershell
# Get fresh token
.\get_token.bat

# Or just logout and login again at http://localhost:5173
```

### USB Bridge not receiving data
1. Check Arduino is connected to COM6
2. Close Arduino Serial Monitor (port conflict)
3. Check Device Manager for correct COM port

## 📁 Script Locations

All scripts are in: `D:\Himanshu_Project\KrishiDrishti\`

- `start_all.bat` - Starts all services
- `get_token.bat` - Gets authentication token
- `run_usb_bridge.bat` - Starts only USB bridge
- `get_token.py` - Token generator script

## 💡 Pro Tips

1. **Keep all 3 terminals open** while using the app
2. **Dashboard auto-refreshes** every 5 seconds
3. **USB Bridge logs** show each sensor reading
4. **Backend logs** show all API requests
5. **Token expires** after 60 minutes - just re-login

---

**Last Updated**: 2026-04-10 22:08 UTC
