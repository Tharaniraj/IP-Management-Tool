#!/bin/bash
# IP Management Tool - Web Version - Linux/Mac Startup Script
# This script sets up the environment and starts the web application
# Usage: bash START.sh or ./START.sh (after chmod +x START.sh)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${YELLOW}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_info() {
    echo -e "${CYAN}[*] $1${NC}"
}

# Main script
echo ""
print_header "============================================================"
print_header "IP MANAGEMENT TOOL - WEB VERSION - STARTUP"
print_header "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python installation
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "Python found: $PYTHON_VERSION"

# Check/Create virtual environment
echo ""
print_info "Checking virtual environment..."

if [ ! -d ".venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
print_info "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
echo ""
print_info "Checking/installing dependencies..."
echo "  (This may take a minute on first run...)"

pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    exit 1
fi
print_success "Dependencies installed successfully"

# Create necessary directories
print_info "Creating data directories..."
mkdir -p data/backups logs
print_success "Directories ready"

# Get local IP address
echo ""
HOSTNAME=$(hostname)

# Try to get IP address (works on Linux and Mac)
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$LOCAL_IP" ]; then
        # For Mac
        LOCAL_IP=$(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
    fi
fi

# Start the application
echo ""
print_header "============================================================"
print_header "Starting IP Management Tool Web Server..."
print_header "============================================================"
echo ""
print_success "Flask server ready"
echo ""
print_header "ACCESS THE APPLICATION:"
echo "  Local:        http://localhost:5000"
if [ ! -z "$LOCAL_IP" ]; then
    echo "  From LAN:     http://$LOCAL_IP:5000"
fi
echo "  Hostname:     $HOSTNAME"
echo ""
print_header "Press Ctrl+C to stop the server"
print_header "============================================================"
echo ""

# Run Flask app
python app.py
