@echo off
echo Starting SleepBuddy Application...
echo.

echo Starting Backend API Server...
cd "AIML FA 2"
start "SleepBuddy API" python sleepbuddy_api.py
cd ..

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend Development Server...
start "SleepBuddy Frontend" npm run dev

echo.
echo ✅ Both servers are starting!
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://127.0.0.1:5000
echo.
echo Press any key to close this window...
pause >nul


