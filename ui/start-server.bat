@echo off
REM Supply Chain Intelligence Dashboard Launcher
REM Run this file to start the development server on Windows

echo.
echo ======================================
echo Supply Chain Intelligence Dashboard
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Starting server...
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Run the Python server
python server.py 8000

REM If server exits, show message
echo.
echo Server stopped.
pause
