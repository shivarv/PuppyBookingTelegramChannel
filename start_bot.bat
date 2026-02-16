@echo off
echo ======================================
echo Cane Corso Puppy Bot - Quick Start
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check dependencies
echo Checking dependencies...
python -c "import telegram" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed!
)
echo.

REM Check for bot token
if "%TELEGRAM_BOT_TOKEN%"=="" (
    echo WARNING: TELEGRAM_BOT_TOKEN not set!
    echo.
    echo Please set your bot token:
    echo   set TELEGRAM_BOT_TOKEN=your_token_here
    echo.
    echo Or edit cane_corso_bot.py and add it directly.
    echo.
    set /p token="Enter your bot token now (or press Enter to exit): "
    if "%token%"=="" (
        exit /b 1
    )
    set TELEGRAM_BOT_TOKEN=%token%
)

echo Bot token configured!
echo.

echo ======================================
echo Starting bot...
echo ======================================
echo.
echo Bot is running! Press Ctrl+C to stop.
echo.

REM Run the bot
python cane_corso_bot.py

pause
