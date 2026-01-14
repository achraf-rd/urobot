#!/bin/bash
# Quick Start Script for UR5 AI Vision Client (Raspberry Pi/Linux)

echo "============================================================"
echo "  UR5 Robotic Sorting System - AI Vision Client"
echo "============================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found!"
    echo "Please install Python3:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "[1/5] Checking Python installation..."
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[2/5] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created"
else
    echo "[2/5] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[4/5] Installing dependencies..."
if [ -f "requirement.txt" ]; then
    pip install -r requirement.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed"
else
    echo "[WARNING] requirement.txt not found!"
    echo "Installing basic dependencies..."
    pip install ultralytics opencv-python numpy Pillow
fi
echo ""

# Check YOLO model
echo "[5/5] Checking YOLO model..."
if [ ! -f "yolo.pt" ]; then
    echo "[WARNING] yolo.pt not found!"
    echo ""
    echo "Please add your YOLO model:"
    echo "  cp /path/to/your/model.pt yolo.pt"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to cancel..."
fi
echo ""

# Check camera
echo "Testing camera..."
if [ -e "/dev/video0" ]; then
    echo "Camera detected at /dev/video0"
else
    echo "[WARNING] Camera not detected!"
    echo "Please check:"
    echo "  1. Camera is connected"
    echo "  2. Camera is enabled in raspi-config"
    echo "  3. Run: sudo raspi-config -> Interface Options -> Camera"
fi
echo ""

# Configuration check
echo "============================================================"
echo "  Configuration Checklist"
echo "============================================================"
echo ""
echo "Before starting, ensure:"
echo "  [1] Robot server is running on PC (python main.py)"
echo "  [2] Robot IP configured in sorting_dashboard.py"
echo "  [3] Camera is connected and enabled"
echo "  [4] YOLO model (yolo.pt) is present"
echo "  [5] Network connection to robot server works"
echo ""
read -p "Continue to start dashboard? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled by user"
    exit 0
fi

# Start the dashboard
echo ""
echo "============================================================"
echo "  Starting AI Vision Dashboard..."
echo "============================================================"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 sorting_dashboard.py

deactivate
