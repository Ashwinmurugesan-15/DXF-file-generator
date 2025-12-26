@echo off
echo Starting Backend...
start cmd /k "python -m backend.main"

echo Starting Frontend...
cd frontend
start cmd /k "npm run dev"

echo.
echo Servers are starting...
echo Backend will be at http://localhost:8000
echo Frontend will be at http://localhost:5173 (usually)
pause
