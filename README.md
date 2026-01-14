# UR5 Robotic Sorting System with AI Detection

A complete automated sorting system combining:
- **UR5 Robot Control** - RoboDK-based robot controller with network API
- **AI-Powered Vision** - YOLO object detection for quality control
- **Real-time Dashboard** - Visual monitoring and control interface

Perfect for automated manufacturing, quality inspection, and intelligent pick-and-place operations.

---

## 🎯 Features

### Robot Controller (Server Side)
- ✅ RoboDK API integration for UR5 control
- ✅ TCP/IP network server (port 5000)
- ✅ OnRobot RG2 gripper control via Dashboard Server
- ✅ Predefined position management (positions.txt)
- ✅ Automatic RoboDK reconnection after gripper operations
- ✅ Pick and place operations with approach positions
- ✅ JSON command protocol for easy integration

### AI Vision Client (Raspberry Pi)
- ✅ Real-time YOLO object detection
- ✅ Quality classification (good/bad pieces)
- ✅ Live camera feed with bounding boxes
- ✅ Automatic robot commands for sorting
- ✅ Dashboard with detection statistics
- ✅ Configurable piece regions and robot IP

---

## 📁 Project Structure

```
urobot/
├── RobotController/              # Robot control server (runs on PC with RoboDK)
│   ├── robot_controller.py       # Core robot control class
│   ├── command_server.py         # TCP server for network commands
│   ├── dashboard_gripper.py      # Gripper control via Dashboard Server
│   ├── positions_manager.py      # Position file management
│   ├── main.py                   # Server entry point
│   ├── positions.txt             # Robot positions (home, pieces, bins)
│   ├── client_ex/                # Client examples and tests
│   │   ├── client_example.py     # RobotClient class
│   │   └── test_client_pick_place.py  # Comprehensive test suite
│   ├── tests/                    # Local tests (no network)
│   │   ├── simple_test.py
│   │   ├── test_local.py
│   │   └── custom_test.py
│   ├── gripper_tests/            # Gripper control tests
│   │   ├── test_gripper_simple.py
│   │   ├── test_gripper_programs.py
│   │   └── test_gripper_diagnostic.py
│   ├── docs/                     # Documentation
│   │   ├── UR5_CONNECTION_GUIDE.md
│   │   ├── ORIENTATION_AND_SPEED_GUIDE.md
│   │   └── command_examples.py
│   └── README.md                 # Robot controller documentation
│
├── Client_Ai_detector/           # AI vision client (runs on Raspberry Pi)
│   ├── sorting_dashboard.py      # Main dashboard application
│   ├── robot_client.py           # Robot communication module
│   ├── run_sorting_system.py     # Launcher script
│   ├── camera_raspberry_test.py  # Camera test utility
│   ├── yolo.pt                   # YOLO model file (required)
│   ├── requirement.txt           # Python dependencies
│   ├── setup.sh                  # Installation script
│   ├── run.sh                    # Run script
│   └── README.md                 # Client documentation
│
├── oled/                         # OLED display module (optional)
│   ├── display.py
│   ├── ui.py
│   └── state.py
│
└── README.md                     # This file - main documentation
```

---

## 🚀 Quick Start

### Prerequisites

**Robot Controller (PC):**
- Windows 10/11
- Python 3.8+
- RoboDK installed and licensed
- UR5 robot (real or simulated)

**AI Vision Client (Raspberry Pi):**
- Raspberry Pi 4 (recommended)
- Raspberry Pi Camera Module or USB camera
- Python 3.8+
- Network connection to robot server

### Installation

#### 1. Robot Controller Setup (PC)

```bash
# Clone repository
git clone https://github.com/achraf-rd/urobot
cd urobot/RobotController

# Install Python dependencies
pip install robodk

# Configure robot positions
# Edit positions.txt with your robot positions

# Start the server
python main.py
```

#### 2. AI Vision Client Setup (Raspberry Pi)

```bash
# Navigate to client directory
cd urobot/Client_Ai_detector

# Run setup script (creates virtual environment)
chmod +x setup.sh
./setup.sh

# Configure robot IP
# Edit sorting_dashboard.py - set robot_ip to your PC's IP

# Run the system
./run.sh
```

---

## 📖 Usage

### Running the Robot Server

```bash
cd RobotController
python main.py
```

**Server Output:**
```
Connected to robot: UR5
Gripper helper initialized (Dashboard will connect on first use)
Speed set to 10%
Acceleration set to 10%
✓ Loaded 9 positions

Server listening on 0.0.0.0:5000
Ready to accept commands from clients...
```

### Running the AI Vision Client

```bash
cd Client_Ai_detector
./run.sh
```

**Dashboard Features:**
- Live camera feed with YOLO detection
- Start/Stop detection
- Manual robot control (Pick/Place buttons)
- Detection statistics
- Connection status indicator

### Testing Robot Functions

**Quick Test (local, no network):**
```bash
cd RobotController/tests
python simple_test.py
```

**Network Client Test:**
```bash
cd RobotController/client_ex
python test_client_pick_place.py
```

---

## 🔧 Configuration

### Robot Positions (positions.txt)

Define your robot positions in `RobotController/positions.txt`:

```
home pose : [x, y, z] with orientation: [rx, ry, rz]
piece 1 : [x, y, z, rx, ry, rz]
piece 2 : [x, y, z, rx, ry, rz]
bad bin : [x, y, z, rx, ry, rz]
good bin : [x, y, z, rx, ry, rz]
```

**To record positions:**
1. Manually move robot to desired position in RoboDK
2. Right-click robot(on robodk) → "Copy pose"
3. Add to positions.txt

### Gripper Programs

Create `.urp` programs on UR5 controller:

**open-gripper.urp**


**close-gripper.urp**


Save programs in `/programs/` on robot controller.

### Network Configuration

**Robot Server:**
- Default port: `5000`
- Binds to all interfaces: `0.0.0.0`

**Client Configuration:**
Edit `Client_Ai_detector/sorting_dashboard.py`:
```python
robot_ip = "192.168.1.10"  # Your PC's IP address
```

---

## 📡 API Reference

### Network Commands (JSON over TCP)

**Pick Piece by Name:**
```json
{
  "command": "pick_piece",
  "piece": "piece 1"
}
```

**Place Piece at Location:**
```json
{
  "command": "place_piece",
  "location": "bad bin"
}
```

**Move to Home:**
```json
{
  "command": "move_home"
}
```

**Get Current Position:**
```json
{
  "command": "get_pose"
}
```

**List Available Positions:**
```json
{
  "command": "list_positions"
}
```

See `RobotController/docs/command_examples.py` for complete API documentation.

---

## 🧪 Testing

### Robot Controller Tests

**Local Tests (no network required):**
```bash
cd RobotController/tests
python simple_test.py          # Basic pick and place
python test_local.py           # Comprehensive suite
python custom_test.py          # Advanced patterns
```

**Client Tests (network required):**
```bash
cd RobotController/client_ex
python test_client_pick_place.py
# Choose: 1=Quick test, 2=All positions, 3=Specific, 4=Custom
```

**Gripper Tests:**
```bash
cd RobotController/gripper_tests
python test_gripper_simple.py      # URCap commands
python test_gripper_programs.py    # URP program loading
python test_gripper_diagnostic.py  # TCP diagnostic
```

### Camera Tests

```bash
cd Client_Ai_detector
python camera_raspberry_test.py
```

---

## 📋 Dependencies

### Robot Controller
```
robodk>=5.6.0
```

### AI Vision Client
```
ultralytics>=8.0.0
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
```

Install all:
```bash
# Robot Controller
pip install robodk

# AI Client (automatically installed by setup.sh)
cd Client_Ai_detector
./setup.sh
```

---

## 🔍 Troubleshooting

### Robot Controller Issues

**"Robot not found" error:**
- Ensure RoboDK is running
- Check robot is loaded in RoboDK workspace
- Verify robot name matches (default searches for UR5)

**"Robot busy" error:**
- Wait for robot to complete current movement
- Check RoboDK connection status
- Restart RoboDK and reconnect robot

**Gripper doesn't move:**
- Verify OnRobot RG2 URCap is installed on robot
- Check gripper programs exist: open-gripper.urp, close-gripper.urp
- Verify robot IP is correct (192.168.1.10 default)
- Test Dashboard connection: `telnet 192.168.1.10 29999`

### AI Client Issues

**Camera not detected:**
```bash
# Test camera
python camera_raspberry_test.py

# List available cameras
ls /dev/video*
```

**Connection refused:**
- Verify robot server is running
- Check PC firewall allows port 5000
- Test connection: `ping <robot-server-ip>`
- Verify IP address in sorting_dashboard.py

**YOLO model error:**
- Ensure yolo.pt file exists in Client_Ai_detector/
- Download model if missing
- Check file permissions

**Low FPS:**
- Reduce camera resolution
- Use Raspberry Pi 4 or higher
- Close other applications
- Consider using Coral TPU for acceleration

---

## 🛠️ Development

### Adding New Commands

**1. Add handler in command_server.py:**
```python
def _handle_my_command(self, data):
    # Your logic here
    return {'status': 'success', 'command': 'my_command'}
```

**2. Register handler:**
```python
self.command_handlers = {
    'my_command': self._handle_my_command,
    # ... existing handlers
}
```

**3. Add client method in client_example.py:**
```python
def my_command(self, param):
    command = {"command": "my_command", "param": param}
    return self.send_command(command)
```

### Adding New Positions

1. Move robot to position in RoboDK
2. Record pose: Right-click robot → "Copy pose" 
3. Add to positions.txt:
```
my_position : [x, y, z, rx, ry, rz]
```
4. Restart server to reload positions

---

## 📚 Additional Documentation

- **RobotController/README.md** - Detailed robot controller documentation
- **RobotController/docs/UR5_CONNECTION_GUIDE.md** - Robot connection setup
- **RobotController/docs/ORIENTATION_AND_SPEED_GUIDE.md** - Motion control guide
- **RobotController/docs/command_examples.py** - Complete API examples
- **Client_Ai_detector/README.md** - AI client detailed documentation

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 👥 Authors

Achraf RACHID

---

## 🙏 Acknowledgments

- RoboDK for robot simulation and control API
- Ultralytics for YOLO object detection
- Universal Robots for UR5 robot platform
- OnRobot for RG2 gripper

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation in /docs folders
- Run test scripts to verify setup

---

**Last Updated:** January 2026
**Version:** 1.0.0
