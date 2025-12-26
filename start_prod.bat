@echo off
echo Building Frontend for Production...
cd frontend
call npm install
call npm run build
cd ..

echo.
echo Starting Production Server...
echo Open http://localhost:8000 in your browser.
call python -m backend.main
