@echo off
REM Windows Activity Logger - Run Script
REM This script starts the activity logger with administrator privileges

echo ============================================================
echo Windows Activity Logger
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

echo Starting Activity Logger...
echo.
python main.py

if %errorLevel% neq 0 (
    echo.
    echo ERROR: Activity Logger exited with errors
    pause
    exit /b 1
)

echo.
echo Activity Logger stopped
pause
