@echo off
REM Quick Run Script - Starts the app

echo Starting Document Detector App...
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate venv and run
call venv\Scripts\activate.bat
python app.py