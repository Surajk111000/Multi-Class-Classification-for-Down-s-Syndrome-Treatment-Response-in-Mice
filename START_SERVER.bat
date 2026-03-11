@echo off
REM Windows batch file to start FastAPI server
REM Make sure you ran TRAIN_MODELS.bat first!

echo.
echo ==========================================
echo Starting FastAPI Server
echo ==========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Error: Virtual environment not found!
    echo Please run TRAIN_MODELS.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if models exist
if not exist "models\saved_models\pca_37.pkl" (
    echo Error: Models not found!
    echo Please run TRAIN_MODELS.bat first
    pause
    exit /b 1
)

REM Start server
echo.
echo Server starting on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
