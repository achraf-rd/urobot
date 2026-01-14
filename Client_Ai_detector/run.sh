#!/bin/bash

# Robot Sorting Dashboard - Run Script
# Activates virtual environment and starts the application

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first: ./setup.sh"
    exit 1
fi

echo "Starting Robot Sorting Dashboard..."
source venv/bin/activate
python3 sorting_dashboard.py
deactivate
