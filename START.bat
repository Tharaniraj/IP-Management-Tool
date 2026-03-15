@echo off
REM IP Management Tool - Web Version - Windows Startup Script
REM This script sets up the environment and starts the web application
REM Requires: Python 3.8+ installed and in PATH

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo IP MANAGEMENT TOOL - WEB VERSION - STARTUP
echo ============================================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if virtual environment exists, if not create it
echo.
echo [*] Checking virtual environment...
if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo [*] Installing dependencies...
echo     This may take a minute on first run...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully

REM Create backup directory if it doesn't exist
if not exist "data" mkdir data
if not exist "data\backups" mkdir data\backups
if not exist "logs" mkdir logs

REM Start the application
echo.
echo ============================================================
echo Starting IP Management Tool Web Server...
echo ============================================================
echo.
echo [*] Flask server starting on http://localhost:5000
echo [*] Waiting for server to be ready...
echo.
timeout /t 2 /nobreak

REM Run Flask app
python app.py

REM If we get here, the app stopped
echo.
echo [*] Application stopped
pause
