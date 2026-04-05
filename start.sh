#!/bin/bash

# DeepGuard Startup Script
# Initializes and starts the multi-agentic deepfake detection system

echo "=========================================="
echo "  DeepGuard Multi-Agentic System"
echo "  Deepfake Detection with RAI Guardrails"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/5]${NC} Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python $python_version detected"

# Create necessary directories
echo -e "${BLUE}[2/5]${NC} Creating directories..."
mkdir -p uploads
mkdir -p outputs
mkdir -p static
mkdir -p logs
echo "   ✓ Directories created"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[3/5]${NC} Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo -e "${BLUE}[3/5]${NC} Virtual environment found"
fi

# Activate virtual environment
echo -e "${BLUE}[4/5]${NC} Activating virtual environment..."
source venv/bin/activate
echo "   ✓ Virtual environment activated"

# Install dependencies
echo -e "${BLUE}[5/5]${NC} Installing dependencies..."
echo "   This may take a few minutes..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"

echo ""
echo -e "${GREEN}=========================================="
echo -e "  DeepGuard is ready!"
echo -e "==========================================${NC}"
echo ""
echo "Starting FastAPI server..."
echo ""
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🌐 Web Interface: http://localhost:8000/static/index.html"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the API server
python3 api.py
