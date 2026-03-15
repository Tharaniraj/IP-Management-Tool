# IP Management Tool - Web Version - PowerShell Startup Script
# This script sets up the environment and starts the web application
# Usage: Run this script as Administrator if needed
# Usage: .\START.ps1

# Requires: Python 3.8+ installed and in PATH
# On first run takes 1-2 minutes to install dependencies

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error_ { Write-Host "[ERROR] $args" -ForegroundColor Red }
function Write-Info { Write-Host "[*] $args" -ForegroundColor Cyan }
function Write-Header { Write-Host $args -ForegroundColor Yellow }

try {
    Write-Host ""
    Write-Header "============================================================"
    Write-Header "IP MANAGEMENT TOOL - WEB VERSION - STARTUP"
    Write-Header "============================================================"
    Write-Host ""

    # Get script directory
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $ScriptDir

    # Check Python installation
    Write-Info "Checking Python installation..."
    $PythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error_ "Python is not installed or not in PATH"
        Write-Host "Please install Python 3.8+ from https://www.python.org/"
        Write-Host "Make sure to check 'Add Python to PATH' during installation"
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Success "Python found: $PythonVersion"

    # Check/Create virtual environment
    Write-Host ""
    Write-Info "Checking virtual environment..."
    
    $VenvPath = ".\.venv"
    if (-not (Test-Path $VenvPath)) {
        Write-Info "Creating virtual environment..."
        python -m venv $VenvPath
        if ($LASTEXITCODE -ne 0) {
            Write-Error_ "Failed to create virtual environment"
            Read-Host "Press Enter to exit"
            exit 1
        }
        Write-Success "Virtual environment created"
    } else {
        Write-Success "Virtual environment already exists"
    }

    # Activate virtual environment
    Write-Host ""
    Write-Info "Activating virtual environment..."
    & "$VenvPath\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"

    # Install dependencies
    Write-Host ""
    Write-Info "Checking/installing dependencies..."
    Write-Host "  (This may take a minute on first run...)"
    
    python -m pip install -q --upgrade pip 2>&1 | Out-Null
    pip install -q -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error_ "Failed to install dependencies"
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Success "Dependencies installed successfully"

    # Create necessary directories
    Write-Info "Creating data directories..."
    if (-not (Test-Path "data")) { New-Item -ItemType Directory -Path "data" -Force | Out-Null }
    if (-not (Test-Path "data\backups")) { New-Item -ItemType Directory -Path "data\backups" -Force | Out-Null }
    if (-not (Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" -Force | Out-Null }
    Write-Success "Directories ready"

    # Get local IP address
    Write-Host ""
    $HostName = [System.Net.Dns]::GetHostName()
    $LocalIP = ([System.Net.Dns]::GetHostAddresses($HostName) | Where-Object { $_.AddressFamily -eq "InterNetwork" } | Select-Object -First 1).IPAddressToString
    
    # Start the application
    Write-Host ""
    Write-Header "============================================================"
    Write-Header "Starting IP Management Tool Web Server..."
    Write-Header "============================================================"
    Write-Host ""
    Write-Success "✓ Flask server ready"
    Write-Host ""
    Write-Header "ACCESS THE APPLICATION:"
    Write-Host "  Local:        http://localhost:5000"
    Write-Host "  From LAN:     http://$LocalIP`:5000"
    Write-Host "  Hostname:     $HostName"
    Write-Host ""
    Write-Header "Press Ctrl+C to stop the server"
    Write-Header "============================================================"
    Write-Host ""

    # Run Flask app
    python app.py

} catch {
    Write-Error_ $_
    Read-Host "Press Enter to exit"
    exit 1
}
