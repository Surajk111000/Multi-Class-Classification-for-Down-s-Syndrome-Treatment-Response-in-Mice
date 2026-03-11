@echo off
REM Windows batch file to run QuickTrain
REM This trains the ML models and generates pkl files

echo.
echo ==========================================
echo Mice Protein Classification - Quick Train
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if needed
echo Installing required packages...
pip install -q -r requirements.txt

REM Run training
echo.
echo Starting model training (this may take 2-3 minutes)...
echo.
python quick_train.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Training failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Training Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Keep this terminal open OR open a new one
echo 2. Run: START_SERVER.bat
echo 3. Open browser: http://localhost:8000/docs
echo.
pause
