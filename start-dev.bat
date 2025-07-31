@echo off
echo Starting AI Tutor Bot Development Servers...

echo.
echo Starting backend server...
start "Backend Server" cmd /k "cd backend && uvicorn main:app --reload --port 8000"

timeout /t 3

echo.
echo Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
