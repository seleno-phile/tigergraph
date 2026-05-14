@echo off
REM GraphRAG Multi-Document Intelligence Assistant Launcher
REM This script starts both the FastAPI backend and Streamlit frontend

echo.
echo ===========================================
echo GraphRAG Multi-Document Intelligence Assistant
echo ===========================================
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

REM Check if requirements are installed
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting GraphRAG Intelligence Assistant...
echo.
echo Backend (FastAPI): http://localhost:8000
echo Frontend (Streamlit): Will open automatically
echo.
echo Press Ctrl+C to stop both services
echo.

REM Start both services
start "GraphRAG Backend" cmd /c "python backend.py"
timeout /t 3 /nobreak >nul
start "GraphRAG Frontend" cmd /c "streamlit run app.py"

echo.
echo Services started! Check your browser for the Streamlit interface.
echo If it doesn't open automatically, visit: http://localhost:8501
echo.
pause
