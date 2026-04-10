@echo off
echo ============================================================
echo   KrishiDrishti - Arduino USB Bridge (COM6)
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Starting Arduino USB Serial Bridge on COM6...
echo.

venv\Scripts\python.exe usb_serial_bridge.py

pause
