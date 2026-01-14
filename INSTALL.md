# Installation Guide - UR5 Robotic Sorting System

Complete step-by-step installation instructions for both robot controller and AI vision client.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Robot Controller Setup (PC)](#robot-controller-setup-pc)
3. [AI Vision Client Setup (Raspberry Pi)](#ai-vision-client-setup-raspberry-pi)
4. [Network Configuration](#network-configuration)
5. [Hardware Setup](#hardware-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Robot Controller (PC/Windows)
- **Operating System:** Windows 10/11 (64-bit)
- **Python:** 3.8 or higher
- **RAM:** 8 GB minimum, 16 GB recommended
- **Disk Space:** 10 GB free space
- **Software:**
  - RoboDK (licensed version for real robot)
  - Python with pip
- **Hardware:**
  - UR5 robot (real or simulated)
  - OnRobot RG2 gripper (or compatible)
  - Ethernet connection to robot

### AI Vision Client (Raspberry Pi)
- **Hardware:** Raspberry Pi 4 (4GB+ RAM recommended)
- **OS:** Raspberry Pi OS (64-bit recommended)
- **Python:** 3.8 or higher
- **Camera:** Raspberry Pi Camera Module v2 or USB camera
- **Storage:** 16 GB+ microSD card
- **Network:** WiFi or Ethernet connection

---

## Robot Controller Setup (PC)

### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Install RoboDK

1. Download RoboDK from [robodk.com](https://robodk.com/download)
2. Run installer and follow setup wizard
3. Activate license (required for real robot connection)
4. Open RoboDK and load UR5 robot:
   - File → Open → Online Library → Universal Robots → UR5
   - Add OnRobot RG2 gripper if available

### Step 3: Clone Repository

```cmd
# Using Git
git clone <repository-url>
cd urobot

# Or download and extract ZIP
```

### Step 4: Install Python Dependencies

```cmd
cd RobotController
pip install robodk
```

### Step 5: Configure Robot Connection

#### For Simulation:
1. Open RoboDK
2. Load UR5 robot model
3. Robot is ready - no additional connection needed

#### For Real Robot:
1. Ensure robot is powered on and connected to network
2. In RoboDK, right-click robot → **Connect to robot**
3. Select **Universal Robots** driver
4. Enter robot IP (default: 192.168.1.10)
5. Click **Connect**
6. Wait for "Connected" status

### Step 6: Set Up Gripper Programs

On UR5 teach pendant:

1. Create **open-gripper.urp**:
   ```
   Program
     RG2(110, 40, 0.0, True, False)
   ```
   Save to `/programs/open-gripper.urp`

2. Create **close-gripper.urp**:
   ```
   Program
     RG2(30, 60, 0.0, True, False)
   ```
   Save to `/programs/close-gripper.urp`

### Step 7: Configure Positions

1. Open `RobotController/positions.txt`
2. Record robot positions:
   - Manually move robot in RoboDK
   - Right-click robot → **Copy pose**
   - Paste values into positions.txt

Example format:
```
home pose : [58.22, 13.90, 353.84] with orientation: [-3.07, 0.046, 1.98]
piece 1 : [103.43, -46.61, 123.26, 3.06, 0.002, 2.25]
bad bin : [-68.18, -59.93, 203.93, -3.14, 0.086, 2.34]
good bin : [-71.31, 205.24, 182.67, 3.12, 0.046, 2.36]
```

### Step 8: Test Robot Controller

```cmd
cd RobotController/tests
python simple_test.py
```

Expected output:
```
Connected to robot: UR5
Moving to home position...
✓ Reached home position
Pick and place sequence...
✓ Test completed successfully!
```

### Step 9: Start Server

```cmd
cd RobotController
python main.py
```

Server should display:
```
Connected to robot: UR5
Gripper helper initialized (Dashboard will connect on first use)
✓ Loaded 9 positions

Server listening on 0.0.0.0:5000
Ready to accept commands from clients...
```

**Keep this terminal open** - server is now running!

---

## AI Vision Client Setup (Raspberry Pi)

### Step 1: Prepare Raspberry Pi

1. Install Raspberry Pi OS (64-bit recommended)
2. Update system:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. Install system dependencies:
   ```bash
   sudo apt install -y python3-pip python3-venv git
   sudo apt install -y libcap-dev libatlas-base-dev libhdf5-dev
   sudo apt install -y python3-opencv
   ```

### Step 2: Clone Repository

```bash
cd ~
git clone <repository-url>
cd urobot/Client_Ai_detector
```

### Step 3: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Set up camera permissions

### Step 4: Verify Camera

```bash
# Test camera
python camera_raspberry_test.py

# Should show camera feed - press 'q' to exit
```

If camera not detected:
```bash
# Enable camera in raspi-config
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot
sudo reboot
```

### Step 5: Add YOLO Model

Copy your trained YOLO model:
```bash
# Model must be named yolo.pt
cp /path/to/your/model.pt ~/urobot/Client_Ai_detector/yolo.pt

# Verify file exists
ls -l yolo.pt
```

### Step 6: Configure Robot IP

Edit `sorting_dashboard.py`:
```bash
nano sorting_dashboard.py
```

Find and change robot IP:
```python
robot_ip = "192.168.1.10"  # Your PC's IP address
```

Save: `Ctrl+X`, `Y`, `Enter`

### Step 7: Test Connection

```bash
# Ping robot server
ping 192.168.1.10

# Should get replies - press Ctrl+C to stop
```

### Step 8: Run Dashboard

```bash
./run.sh
```

Dashboard should open with:
- Camera feed (once started)
- Connection status (green = connected)
- Control buttons
- Detection statistics

---

## Network Configuration

### Recommended Network Setup

#### Option 1: Same Network (Easiest)
```
Router
  ├── PC (192.168.1.10)
  └── Raspberry Pi (192.168.1.20)
```

#### Option 2: Direct Connection
```
PC (192.168.137.1) ←→ Raspberry Pi (192.168.137.100)
```

### Configure Static IP (Recommended)

**On PC (Windows):**
1. Network & Internet Settings → Ethernet
2. Change adapter options → Properties
3. Internet Protocol Version 4 → Properties
4. Use: 192.168.1.10
5. Subnet: 255.255.255.0

**On Raspberry Pi:**
```bash
sudo nano /etc/dhcpcd.conf
```

Add:
```
interface eth0
static ip_address=192.168.1.20/24
static routers=192.168.1.1
```

Reboot: `sudo reboot`

### Firewall Configuration

**Windows Firewall:**
1. Windows Security → Firewall & Network Protection
2. Advanced Settings → Inbound Rules
3. New Rule → Port → TCP → 5000
4. Allow connection → Name: "Robot Controller"

**Raspberry Pi (if ufw enabled):**
```bash
sudo ufw allow 5000/tcp
```

---

## Hardware Setup

### Robot Workspace Layout

```
        [Camera Above]
             |
      ---------------
      |    Pieces   |  piece 1-6
      |  (grid 2x3) |
      ---------------
           |  |
    [Bad Bin] [Good Bin]
```

### Camera Positioning
- **Height:** 400-600mm above workspace
- **Angle:** Perpendicular (90°) or slight angle
- **Lighting:** Uniform, avoid shadows
- **Focus:** Adjust for clear piece visibility

### Robot Base
- **Position:** Adjacent to workspace
- **Reach:** All pieces and bins accessible
- **Safety:** Adequate clearance around robot

---

## Verification

### Robot Controller Verification

1. **Test Connection:**
   ```cmd
   cd RobotController/tests
   python simple_test.py
   ```

2. **Test Network Server:**
   ```cmd
   cd RobotController/client_ex
   python test_client_pick_place.py
   # Choose option 1 (Quick Test)
   ```

3. **Test Gripper:**
   ```cmd
   cd RobotController/gripper_tests
   python test_gripper_simple.py
   # Test open/close operations
   ```

### AI Client Verification

1. **Camera Test:**
   ```bash
   python camera_raspberry_test.py
   ```

2. **Connection Test:**
   ```bash
   # Start dashboard
   ./run.sh
   # Check connection status indicator (should be green)
   ```

3. **Detection Test:**
   - Click "Start Detection"
   - Place object in view
   - Verify bounding boxes appear
   - Check classification (good/bad)

### Complete System Test

1. Start robot server (PC)
2. Start dashboard (Raspberry Pi)
3. Verify connection (green indicator)
4. Click "Start Detection"
5. Place test piece in camera view
6. Click "Pick" when detected
7. Verify robot picks piece
8. Click "Place (Bad)" or "Place (Good)"
9. Verify robot places piece in bin

---

## Troubleshooting

### Robot Controller Issues

**"Robot not found"**
- ✓ Check RoboDK is running
- ✓ Verify robot loaded in workspace
- ✓ Try restarting RoboDK

**"Connection refused"**
- ✓ Ensure server is running (python main.py)
- ✓ Check firewall allows port 5000
- ✓ Verify IP address correct

**"Robot busy"**
- ✓ Wait for current movement to complete
- ✓ Check RoboDK connection status
- ✓ Restart server if persistent

**Gripper doesn't move**
- ✓ Verify URCap installed on robot
- ✓ Check programs exist: open-gripper.urp, close-gripper.urp
- ✓ Test Dashboard: `telnet 192.168.1.10 29999`
- ✓ Verify robot IP correct

### AI Client Issues

**Camera not working**
```bash
# Check camera
vcgencmd get_camera

# Should show: detected=1

# Test camera
raspistill -o test.jpg

# List video devices
ls -la /dev/video*
```

**Connection timeout**
- ✓ Verify server running
- ✓ Check IP address in sorting_dashboard.py
- ✓ Test ping: `ping <server-ip>`
- ✓ Check firewall settings

**Low FPS**
- Reduce camera resolution in code
- Close unnecessary applications
- Use Raspberry Pi 4 (recommended)
- Consider hardware acceleration

**YOLO errors**
- ✓ Verify yolo.pt exists
- ✓ Check model file not corrupted
- ✓ Sufficient disk space
- ✓ Enough RAM (check with `free -h`)

### Network Issues

**Cannot ping server**
```bash
# Check network interface
ifconfig

# Check route
ip route

# Test DNS
ping 8.8.8.8
```

**Slow response**
- Check network bandwidth
- Verify no packet loss: `ping -c 100 <server-ip>`
- Try wired connection instead of WiFi

---

## Post-Installation

### Regular Maintenance

1. **Update positions** when workspace changes
2. **Backup positions.txt** regularly
3. **Test system** before critical operations
4. **Monitor logs** for errors
5. **Keep software updated**

### Performance Tuning

1. **Adjust robot speed** in main.py:
   ```python
   controller = RobotController(speed=20, acceleration=20)
   ```

2. **Optimize camera resolution** in sorting_dashboard.py

3. **Tune detection confidence** threshold

---

## Next Steps

1. ✅ Complete installation
2. ✅ Verify all tests pass
3. ✅ Calibrate camera positions
4. ✅ Train/tune YOLO model
5. ✅ Record production positions
6. ✅ Run system test with real pieces
7. ✅ Monitor and optimize

---

**Installation complete!** Your UR5 Robotic Sorting System is ready to use.

For detailed usage instructions, see the main [README.md](README.md).
For troubleshooting, check individual component documentation in respective folders.
