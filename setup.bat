@echo off
REM Windows Activity Logger - Startup Script
REM Run this script as Administrator

echo ============================================================
echo Windows Activity Logger - Setup
echo ============================================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Please right-click and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Installing required dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [3/3] Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "config" mkdir config
echo Directories created!
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To start the Activity Logger, run:
echo     python main.py
echo.
echo Press any key to exit...
pause >nul
