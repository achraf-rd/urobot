# OnRobot RG2 Gripper - Quick Reference

## 🚀 Quick Start

### Test Gripper First
```bash
cd RobotController/tests
python gripper_test.py
```

### Run with Main System
```bash
cd RobotController
python main.py
# Answer 'y' when asked about gripper
# Enter robot IP (e.g., 192.168.1.100)
```

## 📋 Key Specifications

- **Stroke**: 0-110mm
- **Force**: 3-40N
- **Protocol**: Modbus TCP (Port 502)
- **Default IP**: Robot IP address

## 💻 Code Examples

### Initialize with Gripper
```python
from robot_controller import RobotController

robot = RobotController(
    robot_ip="192.168.1.100",
    use_gripper=True
)
```

### Basic Operations
```python
# Open fully
robot.gripper_open()

# Open to 50mm with 20N force
robot.gripper_open(width_mm=50, force_n=20)

# Close fully
robot.gripper_close()

# Close to 30mm with 25N force
robot.gripper_close(width_mm=30, force_n=25)

# Get status
status = robot.gripper_status()
print(f"Width: {status['width_mm']}mm")
print(f"Gripped: {status['grip_detected']}")

# Check if object gripped
if robot.is_object_gripped():
    print("Object detected!")
```

### Pick & Place
```python
# Open gripper
robot.gripper_open()

# Pick (automatically closes gripper)
robot.pick_object([300, 200, 100], [0, 0, 0])

# Check if gripped
if robot.is_object_gripped():
    print("Object picked!")
    
    # Place (automatically opens gripper)
    robot.place_object([400, 200, 100], [0, 0, 0])
```

## 🌐 Network Commands

### Open Gripper
```json
{"command": "gripper_open"}
{"command": "gripper_open", "width_mm": 110, "force_n": 20}
```

### Close Gripper
```json
{"command": "gripper_close"}
{"command": "gripper_close", "width_mm": 30, "force_n": 25}
```

### Get Status
```json
{"command": "gripper_status"}
```

## 📊 Recommended Parameters

### Force by Object Type
| Object | Force (N) |
|--------|-----------|
| Fragile | 5-10 |
| Standard | 15-25 |
| Heavy | 25-40 |

### Width by Object Size
| Size | Width (mm) |
|------|------------|
| Small | 0-30 |
| Medium | 30-70 |
| Large | 70-110 |

## 🔧 Troubleshooting

### Can't Connect
- ✓ Check robot is powered on
- ✓ Verify IP address
- ✓ Ping robot to test network
- ✓ Ensure gripper is connected to robot

### Gripper Not Moving
- ✓ Check gripper power
- ✓ Verify no mechanical obstruction
- ✓ Check status: `robot.gripper_status()`

### Object Not Detected
- ✓ Increase grip force
- ✓ Adjust grip width
- ✓ Check object surface and size

## 📁 New Files

| File | Purpose |
|------|---------|
| `gripper_controller.py` | Gripper control module |
| `tests/gripper_test.py` | Test script |
| `GRIPPER_GUIDE.md` | Complete guide |
| `GRIPPER_QUICK_REF.md` | This file |

## 🎯 Testing Checklist

- [ ] Run `gripper_test.py` - Basic operations
- [ ] Test pick & place simulation
- [ ] Test with actual objects
- [ ] Adjust force parameters
- [ ] Test network commands
- [ ] Integrate with your workflow

## 🔗 Important Links

See [GRIPPER_GUIDE.md](GRIPPER_GUIDE.md) for detailed documentation.
