@echo off
echo ============================================================
echo   KrishiDrishti - Quick Login
echo ============================================================
echo.
echo This will:
echo   1. Get a fresh authentication token
echo   2. Show you the exact command to paste in browser
echo.
pause

cd /d "%~dp0"
backend\venv\Scripts\python.exe get_token.py
