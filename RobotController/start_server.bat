@echo off
REM Quick Start Script for UR5 Robot Controller (Windows)

echo ============================================================
echo   UR5 Robotic Sorting System - Robot Controller
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Check if RoboDK is installed
echo [2/5] Checking dependencies...
pip show robodk >nul 2>&1
if errorlevel 1 (
    echo Installing RoboDK Python API...
    pip install robodk
    if errorlevel 1 (
        echo [ERROR] Failed to install robodk
        pause
        exit /b 1
    )
) else (
    echo RoboDK Python API already installed
)
echo.

REM Check if positions.txt exists
echo [3/5] Checking configuration...
if not exist "positions.txt" (
    echo [WARNING] positions.txt not found!
    echo Creating example positions.txt file...
    echo home pose : [0.0, 0.0, 300.0] with orientation: [0.0, 0.0, 0.0] > positions.txt
    echo piece 1 : [100.0, 100.0, 100.0, 0.0, 0.0, 0.0] >> positions.txt
    echo bad bin : [-100.0, -100.0, 200.0, 0.0, 0.0, 0.0] >> positions.txt
    echo good bin : [-100.0, 100.0, 200.0, 0.0, 0.0, 0.0] >> positions.txt
    echo.
    echo [!] Please edit positions.txt with your actual robot positions
    echo     Run tests in RoboDK and record positions
)
echo Configuration OK
echo.

REM Check if main.py exists
echo [4/5] Checking main program...
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Please ensure you are in the RobotController directory
    pause
    exit /b 1
)
echo Main program found
echo.

REM Instructions
echo [5/5] Setup complete!
echo.
echo ============================================================
echo   IMPORTANT: Before starting the server
echo ============================================================
echo.
echo 1. Open RoboDK and load your UR5 robot
echo 2. For real robot: Right-click robot -^> Connect to robot
echo 3. Verify positions.txt contains your robot positions
echo 4. Ensure gripper programs exist on robot controller:
echo    - open-gripper.urp
echo    - close-gripper.urp
echo.
echo ============================================================
echo   Starting Robot Controller Server...
echo ============================================================
echo.
echo Press Ctrl+C to stop the server
echo.
pause

REM Start the server
python main.py

pause
