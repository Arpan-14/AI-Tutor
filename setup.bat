@echo off
echo Setting up AI Tutor Bot...

echo.
echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo Installing backend dependencies...
cd ..\backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo To start the development servers:
echo 1. Frontend: cd frontend && npm run dev
echo 2. Backend:  cd backend && uvicorn main:app --reload
echo.
echo Don't forget to:
echo 1. Get a Hugging Face API key from https://huggingface.co
echo 2. Update backend\.env with your API key
echo.
pause
