# Robot Sorting Dashboard - YOLO UR5

A real-time robotic sorting system with YOLO object detection for automated quality control and piece classification.

## Required Files (DO NOT DELETE)

### Core Application
- `sorting_dashboard.py` - Main dashboard application
- `robot_client.py` - Robot communication module
- `run_sorting_system.py` - Launcher script

### Model
- `yolo.pt` - YOLO detection model (REQUIRED)

### Configuration
- `requirement.txt` - Python dependencies

## Installation (Raspberry Pi)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd yolo_ur5
   ```

2. **Run setup script (creates virtual environment):**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Verify YOLO model exists:**
   ```bash
   ls -l yolo.pt
   ```

> **Note:** The setup creates a Python virtual environment to avoid system package conflicts.

## Configuration

Before running, configure in `sorting_dashboard.py`:

### 1. Robot IP Address
- Default: `192.168.137.1`
- Change in the GUI or edit `robot_ip` variable

### 2. Piece Regions (if needed)
- Adjust `self.piece_regions` coordinates
- Match your camera view

### 3. YOLO Confidence
- Default: `0.3`
- Adjust `self.conf_thresh` if needed

## Usage

### **IMPORTANT: Always use virtual environment!**

```bash
# Method 1: Use run script (recommended)
./run.sh

# Method 2: Manual activation
source venv/bin/activate
python3 sorting_dashboard.py
deactivate
```

### ❌ DO NOT run directly:
```bash
# This will fail with ImageTk import error:
python3 sorting_dashboard.py  # WRONG - not using venv!
```

## Display Setup (RealVNC)

Since you're using RealVNC:

1. **Enable VNC on Raspberry Pi:**
   ```bash
   sudo raspi-config
   # Interface Options → VNC → Enable
   ```

2. **Connect via VNC Viewer from your laptop:**
   - Open VNC Viewer
   - Connect to: `<raspberry-pi-ip>:5900`
   - Login with Pi credentials

3. **Run from VNC desktop terminal:**
   ```bash
   cd ~/Desktop/yolo_ur5
   ./run.sh
   ```

## Workflow

1. Click **"Start Camera"** - Initialize camera and YOLO
2. Enter Robot IP and click **"Connect Robot"**
3. Click **"Capture & Detect"** - Classify all 6 pieces
4. Click **"START SORTING"** - Begin automated sorting

## Piece ID Mapping

Visual Display (Screen) → Robot Command:

| Visual ID | Robot ID |
|-----------|----------|
| Piece 5   | piece 1  |
| Piece 4   | piece 2  |
| Piece 2   | piece 3  |
| Piece 3   | piece 4  |
| Piece 6   | piece 5  |
| Piece 1   | piece 6  |

The system automatically remaps IDs when sending commands to the robot server.

## Sorting Process

For each piece:
1. Pick piece (using `pick_piece` function)
2. Place in good/bad bin (using `place_piece` function)
3. Return to home position (using `move_home` function)
4. Move to next piece

**BAD pieces are sorted first, then GOOD pieces.**  
All pieces processed in numerical ID order.

## Troubleshooting

### "cannot import name 'ImageTk' from 'PIL'"
**Solution:** You must use the virtual environment!
```bash
source venv/bin/activate  # Always activate first!
python3 sorting_dashboard.py
```
If still failing, re-run setup:
```bash
./setup.sh
```

### Camera not detected
- Check USB connection
- Try different camera index in code (0, 1, 2)
- Verify camera works: `ls /dev/video*`
- Check permissions: `sudo usermod -a -G video $USER` (logout/login required)

### Model not loading
- Verify `yolo.pt` exists in same directory
- Check file permissions: `chmod +r yolo.pt`

### Robot connection fails
- Verify robot server is running
- Check IP address and port 5000
- Test network: `ping <robot-ip>`

### Low detection accuracy
- Adjust `conf_thresh` (lower = more sensitive)
- Retrain YOLO model with more samples
- Adjust lighting conditions

### Display issues with VNC
- Ensure VNC is enabled: `sudo raspi-config`
- Check VNC service: `sudo systemctl status vncserver-x11-serviced`
- Restart VNC: `sudo systemctl restart vncserver-x11-serviced`

## Hardware Requirements

- Raspberry Pi 3/4 (2GB+ RAM recommended)
- USB Camera
- Network connection to robot
- Python 3.7 or higher
- Display (physical monitor or VNC)

## Quick Reference

### First Time Setup:
```bash
cd ~/Desktop/yolo_ur5
chmod +x setup.sh
./setup.sh
```

### Every Time You Run:
```bash
./run.sh
```

### Check Virtual Environment:
```bash
which python3  # Should show: .../yolo_ur5/venv/bin/python3
```

## Project Structure

```
yolo_ur5/
├── sorting_dashboard.py      # Main application
├── robot_client.py            # Robot communication
├── run_sorting_system.py      # Python launcher
├── setup.sh                   # Setup script (creates venv)
├── run.sh                     # Run script (activates venv)
├── yolo.pt                    # YOLO model
├── requirement.txt            # Dependencies
├── README.md                  # This file
└── venv/                      # Virtual environment (created by setup)
```

## Support

For issues or questions, check:
1. This README.md file
2. Code comments in `sorting_dashboard.py`
3. Robot server documentation

---

**Version:** 1.0 (January 2026)
