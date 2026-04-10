@echo off
echo ============================================================
echo   KrishiDrishti - Complete System Startup
echo ============================================================
echo.
echo This will start:
echo   1. Backend API Server (Port 8000)
echo   2. USB Serial Bridge (COM6)
echo   3. Frontend Dev Server (Port 5173)
echo.
echo Press Ctrl+C in any window to stop that service
echo.
pause

echo.
echo [1/3] Starting Backend API Server...
start "KrishiDrishti Backend" cmd /k "cd /d D:\Himanshu_Project\KrishiDrishti\backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo.
echo [2/3] Starting USB Serial Bridge...
start "KrishiDrishti USB Bridge" cmd /k "cd /d D:\Himanshu_Project\KrishiDrishti\backend && venv\Scripts\python.exe usb_serial_bridge.py"

timeout /t 2 /nobreak >nul

echo.
echo [3/3] Starting Frontend Dev Server...
start "KrishiDrishti Frontend" cmd /k "cd /d D:\Himanshu_Project\KrishiDrishti\frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo   All Services Started!
echo ============================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo To get a fresh authentication token:
echo   1. Run: get_token.bat
echo   2. Or login at http://localhost:5173 with your phone
echo.
echo Monitor the three windows for status updates
echo.
pause
