# UR5 Connection Guide for RoboDK

## Quick Start - 3 Steps

### 1️⃣ Open RoboDK Software
- Launch RoboDK on your computer
- You should see an empty workspace with a 3D view

### 2️⃣ Add UR5 Robot to Station

**Method A - From Online Library:**
```
1. File → Open online library
2. Navigate to: Robots → Universal Robots → UR5
3. Double-click on "UR5" 
4. The robot will appear in your station
```

**Method B - Drag and Drop:**
```
1. Click the "Library" button (book icon) in RoboDK
2. Search for "UR5"
3. Drag and drop UR5 into the main 3D window
```

### 3️⃣ Test Connection from Python

**Run the connection test:**
```bash
cd RobotController
python connect_ur5.py
```

This script will:
- ✅ Check if RoboDK is running
- ✅ Find your UR5 robot
- ✅ Show you the correct robot name to use
- ✅ Test basic communication

---

## Using UR5 in Your Code

Once connected, use it in your scripts:

### Option 1: Using RobotController (Recommended)
```python
from robot_controller import RobotController

# If your robot is named "UR5" in RoboDK
robot = RobotController(robot_name="UR5")

# Or let it find the first robot automatically
robot = RobotController()

# Now use the robot
robot.move_to_home()
robot.pick_object([400, 200, 100], [0, 90, 0])
robot.place_object([400, -200, 100], [0, 90, 0])
```

### Option 2: Direct RoboDK API
```python
from robodk.robolink import Robolink, ITEM_TYPE_ROBOT

rdk = Robolink()
robot = rdk.Item('UR5', ITEM_TYPE_ROBOT)

if robot.Valid():
    print(f"Connected to: {robot.Name()}")
    robot.MoveJ([0, -90, 90, 0, 90, 0])
    robot.WaitMove()
```

---

## Common Robot Names in RoboDK

Depending on your RoboDK version, the robot might be named:
- `UR5` - Most common
- `UR5 Base` - Some versions
- `UR5e` - If using UR5e model
- `Universal Robots UR5` - Full name

**To check your robot's name:**
1. Look at the station tree on the left side of RoboDK
2. The robot name is shown there
3. Use that exact name in your code

---

## Testing Scripts

After connection, run these tests:

### 1. Simple Test (Quick verification)
```bash
python simple_test.py
```
Does: Connect → Home → Pick → Place → Home

### 2. Full Test Suite
```bash
python test_local.py
```
Tests all functions with interactive prompts

### 3. Custom Patterns
```bash
python custom_test.py
```
Test circular patterns, grids, and custom sequences

---

## Troubleshooting

### ❌ "Robot not found" Error

**Solution 1 - Check Robot Name:**
```python
from robodk.robolink import Robolink, ITEM_TYPE_ROBOT

rdk = Robolink()
robots = rdk.ItemList(ITEM_TYPE_ROBOT)

print(f"Found {len(robots)} robots:")
for robot in robots:
    print(f"  - {robot.Name()}")
```

**Solution 2 - Use Auto-Connect:**
```python
# Don't specify name, use first robot
robot = RobotController()
```

### ❌ "Cannot connect to RoboDK" Error

1. **Check RoboDK is running:**
   - Open RoboDK application
   - Should see the main window with 3D view

2. **Check RoboDK API is installed:**
   ```bash
   pip install robodk
   ```

3. **Check Python version compatibility:**
   - RoboDK works with Python 3.6+
   - Check: `python --version`

### ❌ Robot moves incorrectly

1. **Check coordinate system:**
   - RoboDK uses mm for positions
   - Degrees for rotations
   - Right-hand coordinate system

2. **Verify robot reach:**
   - Make sure positions are within robot workspace
   - UR5 reach is approximately 850mm

---

## Example: Complete Working Script

```python
from robot_controller import RobotController

# Connect to UR5
print("Connecting to UR5...")
robot = RobotController(robot_name="UR5")
print(f"Connected to: {robot.robot.Name()}")

# Get current position
current_pose = robot.get_current_pose()
print(f"Current position: {current_pose}")

# Move to home
print("Moving to home...")
robot.move_to_home()

# Pick and place sequence
print("Pick and place...")
robot.pick_object([400, 200, 100], [0, 90, 0])
robot.wait(1.0)
robot.place_object([400, -200, 100], [0, 90, 0])

# Return home
robot.move_to_home()
print("Done!")

# Cleanup
robot.disconnect()
```

---

## Network Server for Raspberry Pi

Once UR5 is working locally, start the network server:

```bash
python main.py
```

This will:
- Connect to UR5
- Start TCP server on port 5000
- Accept commands from Raspberry Pi in JSON format

From Raspberry Pi, use [client_example.py](client_example.py):
```python
from robot_client import RobotClient

client = RobotClient("192.168.1.100")  # Your PC's IP
client.connect()
client.pick_object([400, 200, 100], [0, 90, 0])
client.disconnect()
```

---

## Help & Support

**Run the connection helper:**
```bash
python connect_ur5.py
```

**Check setup guide:**
```bash
python setup_ur5_connection.py
```

**Read documentation:**
- [RoboDK Python API Docs](https://robodk.com/doc/en/PythonAPI/index.html)
- [UR5 Specifications](https://www.universal-robots.com/products/ur5-robot/)

---

## Next Steps

✅ Connection verified → Run `simple_test.py`  
✅ Tests passing → Run `test_local.py` for full suite  
✅ Everything works → Start `main.py` for network control  
✅ Ready for production → Use custom sequences in `custom_test.py`
