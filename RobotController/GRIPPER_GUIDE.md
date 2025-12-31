# OnRobot RG2 Gripper Integration Guide

## Overview

This guide explains how to use the OnRobot RG2 gripper with your UR5 robot project. The gripper is controlled via Modbus TCP protocol and has been integrated into your existing RobotController system.

## Hardware Requirements

- OnRobot RG2 gripper
- UR5 robot with gripper mounted
- Network connection between PC and robot
- Gripper properly connected to robot controller

## Gripper Specifications (RG2)

- **Stroke**: 0-110mm
- **Force Range**: 3-40N
- **Communication**: Modbus TCP (Port 502)
- **Default Slave ID**: 65

## Quick Start

### 1. Test the Gripper

Before integrating with your full system, test the gripper independently:

```bash
cd RobotController/tests
python gripper_test.py
```

The test script provides two test modes:
1. **Basic Operations Test**: Tests opening, closing, partial movements, and force control
2. **Pick & Place Simulation**: Simulates a pick and place cycle

**During the test, you will need:**
- Your UR5 robot IP address (e.g., 192.168.1.100)
- The gripper should be properly mounted and connected
- The robot should be powered on

### 2. Integrate with Your Robot Controller

Once the gripper is tested, you can use it with your main robot controller system.

#### Starting the Robot Controller with Gripper

```bash
cd RobotController
python main.py
```

When prompted:
- Enter 'y' to use the gripper
- Enter your robot IP address (or press Enter for default: 192.168.1.100)

## Usage in Code

### Basic Gripper Control

```python
from robot_controller import RobotController

# Initialize robot with gripper
robot = RobotController(
    robot_ip="192.168.1.100",  # Your robot IP
    use_gripper=True
)

# Open gripper (fully)
robot.gripper_open()

# Open gripper to specific width
robot.gripper_open(width_mm=50, force_n=20)

# Close gripper (fully)
robot.gripper_close()

# Close gripper to specific width with custom force
robot.gripper_close(width_mm=30, force_n=25)

# Check gripper status
status = robot.gripper_status()
if status:
    print(f"Width: {status['width_mm']}mm")
    print(f"Force: {status['force_n']}N")
    print(f"Busy: {status['busy']}")
    print(f"Object gripped: {status['grip_detected']}")

# Check if object is gripped
if robot.is_object_gripped():
    print("Object detected!")
```

### Pick and Place Example

```python
# Pick operation with gripper
def pick_with_gripper(robot, position, orientation):
    # Open gripper before approaching
    robot.gripper_open()
    
    # Move to pick position (using your existing pick method)
    robot.pick_object(position, orientation)
    
    # The pick_object method already closes the gripper internally
    # But you can check if object was gripped
    if robot.is_object_gripped():
        print("Object successfully picked!")
        return True
    else:
        print("No object detected")
        return False

# Place operation with gripper
def place_with_gripper(robot, position, orientation):
    # Move to place position (using your existing place method)
    robot.place_object(position, orientation)
    
    # The place_object method already opens the gripper internally
    print("Object placed!")
```

## Network Commands

When using the command server, you can send gripper commands via TCP:

### Gripper Open

```json
{
    "command": "gripper_open"
}
```

Or with specific parameters:

```json
{
    "command": "gripper_open",
    "width_mm": 110,
    "force_n": 20
}
```

### Gripper Close

```json
{
    "command": "gripper_close"
}
```

Or with specific parameters:

```json
{
    "command": "gripper_close",
    "width_mm": 30,
    "force_n": 25
}
```

### Gripper Status

```json
{
    "command": "gripper_status"
}
```

Response:

```json
{
    "status": "success",
    "command": "gripper_status",
    "gripper_status": {
        "status": 0,
        "width_mm": 45.2,
        "force_n": 20.5,
        "busy": false,
        "grip_detected": true
    }
}
```

## Client Example (Raspberry Pi)

```python
import socket
import json

def send_gripper_command(command, **kwargs):
    """Send a gripper command to the robot server."""
    # Connect to robot server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('ROBOT_PC_IP', 5000))
    
    # Prepare command
    cmd = {'command': command}
    cmd.update(kwargs)
    
    # Send command
    sock.send(json.dumps(cmd).encode('utf-8'))
    
    # Receive response
    response = sock.recv(4096).decode('utf-8')
    sock.close()
    
    return json.loads(response)

# Usage examples
# Open gripper
response = send_gripper_command('gripper_open')
print(response)

# Close gripper with specific parameters
response = send_gripper_command('gripper_close', width_mm=30, force_n=25)
print(response)

# Get gripper status
response = send_gripper_command('gripper_status')
print(response)
```

## Troubleshooting

### Connection Issues

**Problem**: "Failed to connect to gripper"

**Solutions**:
1. Check robot is powered on and network connection is working
2. Verify robot IP address is correct
3. Ensure gripper is properly connected to robot
4. Check if Modbus TCP port (502) is accessible
5. Try pinging the robot IP address

### Gripper Not Responding

**Problem**: Commands sent but gripper doesn't move

**Solutions**:
1. Check gripper power supply
2. Verify gripper is not in error state (check status)
3. Ensure gripper is properly mounted and not mechanically blocked
4. Check gripper status using `robot.gripper_status()`

### Object Detection Not Working

**Problem**: `grip_detected` always False

**Solutions**:
1. Increase gripping force
2. Ensure object is within gripper's gripping range (0-110mm)
3. Check object material and surface (smooth surfaces may be harder to detect)
4. Adjust grip width to appropriate size for the object

### Timeout Issues

**Problem**: "Gripper movement timeout"

**Solutions**:
1. Increase timeout value in `wait_for_completion()`
2. Check if gripper is mechanically blocked
3. Verify gripper is receiving proper power

## Configuration

### Default Gripper Parameters

You can set default parameters for grip and release operations:

```python
from gripper_controller import GripperController

gripper = GripperController(robot_ip="192.168.1.100")
gripper.connect()

# Set default parameters
gripper.set_defaults(
    grip_width=0,       # Default grip width (mm)
    grip_force=20,      # Default grip force (N)
    release_width=110,  # Default release width (mm)
    release_force=20    # Default release force (N)
)
```

### Adjusting Force for Different Objects

| Object Type | Recommended Force |
|-------------|-------------------|
| Soft/Fragile | 5-10N |
| Standard | 15-25N |
| Heavy/Rigid | 25-40N |

### Adjusting Width for Different Objects

The width parameter represents the target gripper opening. When gripping:
- **0mm**: Fully closed (maximum grip)
- **Small objects (< 30mm)**: Use 0-30mm
- **Medium objects (30-70mm)**: Use 30-70mm
- **Large objects (> 70mm)**: Use 70-110mm

## Advanced Usage

### Direct Gripper Control

For more advanced control, you can directly use the `GripperController` class:

```python
from gripper_controller import GripperController

# Create standalone gripper controller
gripper = GripperController(robot_ip="192.168.1.100")

# Connect
if gripper.connect():
    # Custom grip sequence
    gripper.open(width_mm=110, force_n=20)
    gripper.wait_for_completion()
    
    # Gradual closing
    for width in [80, 60, 40, 20, 0]:
        gripper.close(width_mm=width, force_n=15)
        gripper.wait_for_completion()
        time.sleep(0.5)
    
    # Disconnect
    gripper.disconnect()
```

### Status Monitoring

Continuously monitor gripper status:

```python
import time

while True:
    status = robot.gripper_status()
    if status:
        print(f"Width: {status['width_mm']:.1f}mm | "
              f"Force: {status['force_n']:.1f}N | "
              f"Busy: {status['busy']} | "
              f"Gripped: {status['grip_detected']}")
    time.sleep(0.5)
```

## Integration with Existing Pick/Place

Your existing `pick_object()` and `place_object()` methods in `robot_controller.py` have been updated to automatically use the real gripper when connected. They will fall back to simulation mode if the gripper is not connected.

```python
# This will automatically use the real gripper if connected
robot.pick_object([300, 200, 100], [0, 0, 0])
robot.place_object([400, 200, 100], [0, 0, 0])
```

## Summary of New Features

### New Methods in RobotController

- `gripper_open(width_mm, force_n)` - Open gripper
- `gripper_close(width_mm, force_n)` - Close gripper
- `gripper_status()` - Get gripper status
- `is_object_gripped()` - Check if object is gripped

### New Network Commands

- `gripper_open` - Open gripper
- `gripper_close` - Close gripper
- `gripper_status` - Get gripper status

### New Files

- `gripper_controller.py` - Gripper controller module
- `tests/gripper_test.py` - Standalone gripper test script
- `GRIPPER_GUIDE.md` - This guide

## Next Steps

1. **Test the gripper** using `gripper_test.py`
2. **Adjust default parameters** based on your objects
3. **Integrate with your workflow** using the new gripper methods
4. **Test with actual pick and place operations**
5. **Fine-tune force and width parameters** for your specific use case

## Support

For OnRobot RG2 specific questions, refer to the official OnRobot documentation:
- [OnRobot RG2 Manual](https://onrobot.com/en/products/rg2-gripper)
- [OnRobot Modbus TCP Guide](https://onrobot.com/en/support)
