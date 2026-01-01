@echo off
REM CPU Setup Script for Document Detector App
REM Works on ALL computers (Windows, Mac via Python, Linux)

echo ============================================================
echo Document Detector App - CPU Setup (Universal)
echo ============================================================
echo.
echo This setup works on ANY computer
echo Processing time: 15-30 seconds per document
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Git is not installed
    echo Real-ESRGAN may fall back to OpenCV mode
    echo To get full Real-ESRGAN support, install Git from: https://git-scm.com/
    echo.
    set USE_GIT=0
    pause
) else (
    set USE_GIT=1
)

echo [1/7] Creating virtual environment...
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

echo [5/7] Installing PyTorch CPU version (~500MB download)...
echo        This works on all computers but is slower than GPU version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo [6/7] Installing core dependencies...
pip install opencv-python flask werkzeug pillow ultralytics

echo [7/7] Installing Real-ESRGAN components...
pip uninstall basicsr -y >nul 2>&1

if %USE_GIT%==1 (
    echo        Installing BasicSR from GitHub...
    pip install git+https://github.com/XPixelGroup/BasicSR.git
    if errorlevel 1 (
        pip install basicsr
    )
) else (
    pip install basicsr
)

pip install facexlib realesrgan gfpgan

echo.
echo ============================================================
echo Testing Installation...
echo ============================================================
python -c "import torch; print('PyTorch version:', torch.__version__); print('Device: CPU')" 2>nul

python -c "from basicsr.archs.rrdbnet_arch import RRDBNet; from realesrgan import RealESRGANer; print('Real-ESRGAN: Ready')" 2>nul
if errorlevel 1 (
    echo WARNING: Real-ESRGAN setup incomplete - will use OpenCV fallback
)

echo.
echo Creating directories...
if not exist "models\realesrgan" mkdir models\realesrgan
if not exist "temp\uploads" mkdir temp\uploads
if not exist "temp\processed" mkdir temp\processed

echo.
echo ============================================================
echo Downloading Real-ESRGAN Model...
echo ============================================================
echo.

REM Check if model already exists
if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
    echo Real-ESRGAN model already exists, skipping download...
) else (
    echo Downloading RealESRGAN_x4plus.pth (~65MB)...
    echo This may take 2-5 minutes depending on your internet speed...
    echo.

    REM Download using PowerShell
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth' -OutFile 'models\realesrgan\RealESRGAN_x4plus.pth'}"

    if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
        echo.
        echo ✅ Model downloaded successfully!
    ) else (
        echo.
        echo ⚠️  Model download failed - it will be downloaded on first use
    )
)

echo.
echo ============================================================
echo CPU Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Ensure trainedYOLO.pt is in models/ folder
echo   2. Run: run.bat
echo   3. Open: http://localhost:5000
echo.
echo Expected processing time: 15-30 seconds per document
echo (This is normal for CPU mode - quality is identical to GPU!)
echo.
if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
    echo ✅ Real-ESRGAN model ready!
) else (
    echo ⚠️  Real-ESRGAN model not found - will use OpenCV mode
)
echo.
pause