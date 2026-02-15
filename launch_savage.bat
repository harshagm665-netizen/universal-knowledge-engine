@echo off
setlocal
title SAVAGE SYSTEM BOOTLOADER
color 0B

echo ==================================================
echo           NOVATECH ROBO PVT LTD
echo    UNIVERSAL KNOWLEDGE ENGINE - BOOT SEQUENCE
echo ==================================================
echo.

:: 1. Check if UV is installed for the Backend
echo [1/3] Checking Backend Environment...
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: 'uv' not found. Please install it first.
    pause
    exit /b
)
echo ✅ UV detected.

:: 2. Start the FastAPI Backend
echo [2/3] Launching Sentinel AI (Backend)...
:: We use 'start' to open a new window so you can see the logs
start "SAVAGE_BACKEND" cmd /k "uv run python apps/api-server/main.py"

:: Wait for the backend to claim port 8000
echo ⏳ Waiting for API to initialize...
timeout /t 5 /nobreak > nul

:: 3. Start the Next.js Frontend
echo [3/3] Launching Command Center (Frontend)...
if not exist "apps\web-ui\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd apps\web-ui && npm install && cd ..\..
)

start "SAVAGE_FRONTEND" cmd /k "cd apps\web-ui && npm run dev"

echo.
echo ==================================================
echo ✅ BOOT SEQUENCE COMPLETE
echo.
echo 🖥️  API SERVER  : http://localhost:8000
echo 🖥️  WEB DASHBOARD: http://localhost:3000
echo.
echo 🤖 SYSTEM STATUS: ONLINE
echo ==================================================
echo.
echo Press any key to terminate the bootloader (Note: Windows will stay open).
pause > nul