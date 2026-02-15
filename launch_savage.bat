@echo off
title SAVAGE SYSTEM BOOTLOADER
echo ==================================================
echo 🚀 STARTING UNIVERSAL KNOWLEDGE ENGINE
echo ==================================================

:: 1. Start the FastAPI Backend in a new window
echo 🧠 Initializing Sentinel AI (Backend)...
start "SAVAGE BACKEND" cmd /k "cd apps\api-server && uv run python main.py"

:: Wait 3 seconds to let the backend port (8000) initialize
timeout /t 3 /nobreak > nul

:: 2. Start the Next.js Frontend in a new window
echo 🌐 Initializing Command Center (Frontend)...
start "SAVAGE FRONTEND" cmd /k "cd apps\web-ui && npm run dev"

echo ==================================================
echo ✅ BOOT SEQUENCE COMPLETE
echo 🖥️  Backend: http://localhost:8000
echo 🖥️  Frontend: http://localhost:3000
echo ==================================================
pause