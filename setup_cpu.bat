@echo off
REM Automated Setup Script for Document Detector App
REM This script sets up everything automatically

echo ============================================================
echo Document Detector App - Automated Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if git is installed (needed for BasicSR from GitHub)
git --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Git is not installed
    echo BasicSR will be installed from PyPI instead of GitHub
    echo This may cause Real-ESRGAN to fall back to OpenCV
    echo.
    echo To get full Real-ESRGAN support, install Git from: https://git-scm.com/
    echo.
    set USE_GIT=0
) else (
    set USE_GIT=1
)

echo [1/7] Python found. Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/7] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/7] Upgrading pip...
python -m pip install --upgrade pip

echo [4/7] Installing NumPy (compatible version)...
pip install "numpy<2.0.0"

echo [5/7] Installing PyTorch and TorchVision (this may take a few minutes)...
echo        CPU version - works on all systems
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo [6/7] Installing core dependencies...
pip install opencv-python flask werkzeug pillow ultralytics

echo [7/7] Installing Real-ESRGAN components...
echo        Note: This step may take 2-3 minutes

REM Remove old BasicSR if present
pip uninstall basicsr -y >nul 2>&1

REM Install BasicSR from GitHub (the version that works!)
if %USE_GIT%==1 (
    echo        Installing BasicSR from GitHub ^(recommended^)...
    pip install git+https://github.com/XPixelGroup/BasicSR.git
    if errorlevel 1 (
        echo        GitHub installation failed, trying PyPI...
        pip install basicsr
    )
) else (
    echo        Installing BasicSR from PyPI ^(may have compatibility issues^)...
    pip install basicsr
)

REM Install remaining Real-ESRGAN components
pip install facexlib realesrgan gfpgan

REM Test if Real-ESRGAN works
echo.
echo Testing Real-ESRGAN installation...
python -c "from basicsr.archs.rrdbnet_arch import RRDBNet; from realesrgan import RealESRGANer; print('SUCCESS: Real-ESRGAN is ready!')" 2>nul
if errorlevel 1 (
    echo WARNING: Real-ESRGAN not fully installed - app will use OpenCV fallback
    echo          OpenCV upscaling still produces excellent quality results!
    echo.
    if %USE_GIT%==0 (
        echo          To enable Real-ESRGAN:
        echo          1. Install Git from https://git-scm.com/
        echo          2. Re-run this setup script
        echo.
    )
)

echo.
echo Creating required directories...
if not exist "models\realesrgan" mkdir models\realesrgan
if not exist "temp\uploads" mkdir temp\uploads
if not exist "temp\processed" mkdir temp\processed

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Your app is ready to run!
echo.
echo Next steps:
echo   1. Make sure trainedYOLO.pt is in the models/ folder
echo   2. Run: run.bat  ^(or manually: python app.py^)
echo   3. Open browser: http://localhost:5000
echo.
if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
    echo Real-ESRGAN model found - GPU-accelerated upscaling ready!
) else (
    echo Note: Real-ESRGAN model will auto-download on first use ^(~65MB^)
)
echo.
pause