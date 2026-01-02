# RG2 Gripper Integration - Complete

## Overview
The OnRobot RG2 gripper has been successfully integrated into your UR5 robot project. The gripper is controlled automatically during pick and place operations - clients only need to send high-level commands.

## Architecture

```
Raspberry Pi (Client)          PC (Server)
┌─────────────────┐           ┌──────────────────────────────┐
│ client_example  │  TCP/IP   │   command_server.py          │
│     .py         ├──────────►│   (port 5000)                │
└─────────────────┘           └──────────┬───────────────────┘
                                         │
                              ┌──────────▼───────────────────┐
                              │   robot_controller.py        │
                              │   - Handles robot movement   │
                              │   - Manages gripper via      │
                              │     pick/place operations    │
                              └──────────┬───────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                  ┌──────▼────────┐            ┌────────▼──────────┐
                  │   RoboDK API  │            │ gripper_controller│
                  │   (Movement)  │            │ .py (RG2 Gripper) │
                  └───────────────┘            └───────────────────┘
                         │                               │
                         └───────────┬───────────────────┘
                                     │
                              ┌──────▼──────┐
                              │  UR5 Robot  │
                              │  + RG2      │
                              │  (URCaps)   │
                              └─────────────┘
```

## How It Works

### Client Side (Raspberry Pi)
The client only sends high-level commands:
```python
# Pick object - gripper opens and closes automatically
client.pick_object([300, 200, 150], [0, 90, 0])

# Place object - gripper opens automatically
client.place_object([400, 200, 150], [0, 90, 0])
```

### Server Side (PC)
1. **command_server.py** receives commands and routes them
2. **robot_controller.py** handles:
   - Robot movement to approach position
   - Moving down to pick/place position
   - **Automatic gripper control** (open before pick, close to grip, open to release)
   - Moving back up after operation

3. **gripper_controller.py** sends URScript commands:
   - `RG2(70,40,0.0,True,False,False)` to open (70mm)
   - `RG2(60,40,0.0,True,False,False)` to close/grip (60mm)

## Files Modified

### Core Files
- **gripper_controller.py** - NEW: Controls RG2 gripper via URScript
- **robot_controller.py** - MODIFIED: Added gripper integration
- **command_server.py** - MODIFIED: Removed direct gripper commands (gripper only controlled internally)

### Test Files
- **tests/test_rg2_gripper.py** - NEW: Test gripper directly on server
- **client_ex/client_example.py** - EXISTING: Shows how clients interact (no gripper commands)

## Usage

### Testing the Gripper (On Server PC)
```bash
cd RobotController\tests
python test_rg2_gripper.py
```
This tests the gripper directly with three modes:
1. Basic open/close test
2. Custom parameters test
3. Pick & place simulation

### Running the Server
```bash
cd RobotController
python main.py
```
Select "Yes" when asked about using the gripper.

### Running the Client (On Raspberry Pi)
```bash
cd client_ex
python client_example.py
```
Choose:
1. Run pick and place example
2. Interactive mode

## Client Commands Available

| Command | Description | Gripper Action |
|---------|-------------|----------------|
| `pick` | Pick object at position | Opens before approach, closes to grip |
| `place` | Place object at position | Opens to release object |
| `move_home` | Move to home position | No gripper action |
| `move_pose` | Move to specific pose | No gripper action |
| `wait` | Wait for duration | No gripper action |
| `get_pose` | Get current pose | No gripper action |
| `get_joints` | Get joint angles | No gripper action |

**Note:** Clients cannot directly control the gripper. It's managed automatically during pick/place operations.

## Gripper Parameters

### Default Values (From Your URScript)
- **Open width**: 70mm @ 40N force
- **Close/Grip width**: 60mm @ 40N force
- **Parameters**: `RG2(width, force, 0.0, True, False, False)`
  - `width`: Target width in mm (0-110mm)
  - `force`: Gripping force in N (4-40N)
  - `0.0`: Payload mass (not used)
  - `True`: Set payload automatically
  - `False`: Depth compensation disabled
  - `False`: Not slave gripper

### Modifying Gripper Settings
To change default gripper behavior, edit `gripper_controller.py`:
```python
def open(self, width_mm=70, force_n=40):  # Change defaults here
def close(self, width_mm=60, force_n=40):  # Change defaults here
```

## Pick and Place Sequence

### What Happens During `pick`:
1. Robot moves to approach position (50mm above target)
2. **Gripper opens** (70mm) - *automatic*
3. Robot moves down to pick position
4. **Gripper closes** (60mm) to grip object - *automatic*
5. Robot moves back to approach position
6. Returns success/failure

### What Happens During `place`:
1. Robot moves to approach position (50mm above target)
2. Robot moves down to place position
3. **Gripper opens** (70mm) to release object - *automatic*
4. Robot moves back to approach position
5. Returns success/failure

## Troubleshooting

### Gripper Not Working
1. Check RoboDK is running with UR5 loaded
2. Verify gripper is enabled: `use_gripper=True` in main.py
3. Check URCaps is installed on UR5 controller
4. Test gripper manually: `python tests/test_rg2_gripper.py`

### Client Can't Connect
1. Verify server is running: `python main.py`
2. Check IP address in client_example.py matches server PC
3. Ensure port 5000 is not blocked by firewall
4. Test connection: `telnet <server_ip> 5000`

### Pick/Place Not Gripping
1. Adjust grip width in `gripper_controller.py` (default 60mm)
2. Increase force if object is slipping (max 40N)
3. Check object size is within 0-110mm range
4. Verify `grip_detected` status in gripper logs

## Example Client Code

```python
from client_example import RobotClient

# Connect to server
client = RobotClient("192.168.1.100")
client.connect()

# Pick object
response = client.pick_object(
    position=[300, 200, 150],    # x, y, z in mm
    orientation=[0, 90, 0]        # rx, ry, rz in degrees
)
print(response)  # {'status': 'success', 'command': 'pick'}

# Place object
response = client.place_object(
    position=[400, 200, 150],
    orientation=[0, 90, 0]
)
print(response)  # {'status': 'success', 'command': 'place'}

client.disconnect()
```

## Summary

✅ **Gripper integrated** - Uses URScript RG2() function via RoboDK
✅ **Automatic control** - Opens/closes during pick/place operations
✅ **Client simplified** - Only high-level commands (pick, place, move)
✅ **Server tested** - test_rg2_gripper.py validates gripper functionality
✅ **Network ready** - Raspberry Pi can control robot remotely

**The client doesn't need to know about the gripper - just send pick/place commands!**
