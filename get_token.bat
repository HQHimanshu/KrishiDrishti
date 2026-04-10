@echo off
echo ============================================================
echo   KrishiDrishti - Get Fresh Token
echo ============================================================
echo.

cd /d "%~dp0"

echo Getting fresh authentication token...
echo.

backend\venv\Scripts\python.exe get_token.py

pause
