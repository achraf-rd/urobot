#!/bin/bash

# Robot Sorting Dashboard - Quick Setup Script for Raspberry Pi
# This script creates a virtual environment and installs all dependencies

echo "=========================================="
echo "Robot Sorting Dashboard Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 is not installed!"
    exit 1
fi

# Update system packages and install dependencies
echo ""
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-tk python3-pil python3-pil.imagetk python3-venv

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment!"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing dependencies in virtual environment..."
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirement.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    deactivate
    exit 1
fi

# Ensure PIL/Pillow is installed with full support
pip install --upgrade pillow

deactivate

# Check if YOLO model exists
echo ""
echo "Checking YOLO model..."
if [ ! -f "yolo.pt" ]; then
    echo "WARNING: yolo.pt not found! Please copy your trained model."
else
    echo "YOLO model found: yolo.pt"
fi

# Check camera
echo ""
echo "Checking camera devices..."
ls -l /dev/video* 2>/dev/null

if [ $? -ne 0 ]; then
    echo "WARNING: No camera detected. Please connect USB camera."
else
    echo "Camera device(s) found!"
fi

# Make scripts executable
echo ""
echo "Setting permissions..."
chmod +x run.sh

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "✅ System dependencies installed"
echo "✅ Virtual environment created"
echo "✅ Python packages installed"
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python3 sorting_dashboard.py"
echo "  deactivate"
echo ""
echo "See README.md for full documentation."
echo ""
