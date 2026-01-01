@echo off
REM Script to download Real-ESRGAN model manually

echo ============================================================
echo Real-ESRGAN Model Downloader
echo ============================================================
echo.

REM Create directory if it doesn't exist
if not exist "models\realesrgan" mkdir models\realesrgan

REM Check if model already exists
if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
    echo Model already exists at: models\realesrgan\RealESRGAN_x4plus.pth
    echo.
    echo File size:
    dir "models\realesrgan\RealESRGAN_x4plus.pth" | find "RealESRGAN_x4plus.pth"
    echo.
    choice /C YN /M "Do you want to re-download the model?"
    if errorlevel 2 goto :end
    if errorlevel 1 (
        echo.
        echo Deleting existing model...
        del "models\realesrgan\RealESRGAN_x4plus.pth"
    )
)

echo.
echo Downloading RealESRGAN_x4plus.pth...
echo Size: ~65 MB
echo This may take 2-5 minutes depending on your internet speed...
echo.
echo Source: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
echo.

REM Download using PowerShell with progress
powershell -Command "& { ^
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ^
    $ProgressPreference = 'SilentlyContinue'; ^
    Write-Host 'Starting download...' -ForegroundColor Green; ^
    try { ^
        Invoke-WebRequest -Uri 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth' ^
        -OutFile 'models\realesrgan\RealESRGAN_x4plus.pth' ^
        -UseBasicParsing; ^
        Write-Host 'Download completed successfully!' -ForegroundColor Green ^
    } catch { ^
        Write-Host 'Download failed:' $_.Exception.Message -ForegroundColor Red; ^
        exit 1 ^
    } ^
}"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Download Failed!
    echo ============================================================
    echo.
    echo Possible solutions:
    echo 1. Check your internet connection
    echo 2. Try downloading manually from:
    echo    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
    echo 3. Save the file to: models\realesrgan\RealESRGAN_x4plus.pth
    echo.
    goto :end
)

echo.
echo ============================================================
echo Download Complete!
echo ============================================================
echo.

REM Verify the file
if exist "models\realesrgan\RealESRGAN_x4plus.pth" (
    echo ✅ File successfully saved to: models\realesrgan\RealESRGAN_x4plus.pth
    echo.
    echo File details:
    dir "models\realesrgan\RealESRGAN_x4plus.pth" | find "RealESRGAN_x4plus.pth"
    echo.
    echo The model is ready to use!
    echo You can now run your application with Real-ESRGAN upscaling.
) else (
    echo ❌ Error: File not found after download
    echo Please try downloading manually
)

:end
echo.
pause