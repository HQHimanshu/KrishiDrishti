@echo off
echo ============================================================
echo   KrishiDrishti - USB Serial Bridge Launcher
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Checking requirements...
venv\Scripts\python.exe -c "import serial" 2>nul
if errorlevel 1 (
    echo Installing pyserial...
    venv\Scripts\pip install pyserial
)

echo.
echo Starting USB Serial Bridge...
echo.

venv\Scripts\python.exe usb_serial_bridge.py %*

pause
