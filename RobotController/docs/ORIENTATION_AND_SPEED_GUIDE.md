# Robot Orientation and Speed Control Guide

## Table of Contents
1. [Understanding Robot Orientation](#understanding-robot-orientation)
2. [Orientation Representation Methods](#orientation-representation-methods)
3. [Controlling Robot Speed](#controlling-robot-speed)
4. [Practical Examples](#practical-examples)

---

## Understanding Robot Orientation

### What is Orientation?

**Orientation** defines the rotational pose (attitude) of the robot's end-effector (tool) in 3D space. While **position** tells you *where* the robot tool is located (x, y, z coordinates), **orientation** tells you *how* the tool is rotated or tilted.

Think of it like this:
- **Position (x, y, z)**: "The robot is at coordinates (400, 200, 150) mm"
- **Orientation (rx, ry, rz)**: "The robot tool is tilted 90° forward and pointing downward"

### Why is Orientation Important?

Orientation is critical for:
- **Pick operations**: Gripper must approach from the correct angle
- **Assembly tasks**: Parts must be oriented correctly to fit together
- **Welding/painting**: Tool must be at specific angle to the workpiece
- **Avoiding collisions**: Different orientations may avoid obstacles

---

## Orientation Representation Methods

### 1. Euler Angles (Used in Our Code)

In our RobotController, we use **Euler angles** with the format: `[rx, ry, rz]`

```python
orientation = [rx, ry, rz]  # Rotation around X, Y, Z axes in degrees
```

#### Axis Definitions:
- **rx** (Roll): Rotation around the X-axis
- **ry** (Pitch): Rotation around the Y-axis  
- **rz** (Yaw): Rotation around the Z-axis

#### Common Orientations for UR5:

```python
# Gripper pointing straight down (most common for pick/place)
orientation = [0, 90, 0]     # 90° pitch (forward tilt)

# Gripper pointing straight down, rotated 180°
orientation = [180, 90, 0]

# Gripper horizontal, pointing forward
orientation = [0, 0, 0]

# Gripper tilted 45° to the side
orientation = [45, 90, 0]

# Gripper rotated 90° around vertical axis
orientation = [0, 90, 90]
```

### 2. Visual Understanding

```
Z-axis (vertical)
↑
|
|     ry (pitch)
|    ↻ 
|   /
|  /
| /________→ X-axis
/         rx (roll)
/
↙ Y-axis
   rz (yaw)
```

### 3. Real-World Examples

#### Example 1: Picking from Above
```python
position = [400, 200, 100]      # Location of object
orientation = [0, 90, 0]        # Gripper pointing down
robot.pick_object(position, orientation)
```
**Result**: Gripper approaches from directly above

#### Example 2: Picking from Side
```python
position = [400, 200, 100]      
orientation = [0, 0, 90]        # Gripper horizontal, rotated
robot.pick_object(position, orientation)
```
**Result**: Gripper approaches horizontally from the side

#### Example 3: Angled Approach
```python
position = [400, 200, 100]      
orientation = [0, 45, 0]        # 45° angle
robot.pick_object(position, orientation)
```
**Result**: Gripper approaches at 45° angle

---

## Controlling Robot Speed

### Speed Control Methods in RoboDK

RoboDK provides multiple ways to control robot speed:

### 1. Set Speed Directly (Recommended)

```python
from robot_controller import RobotController

robot = RobotController()

# Set speed as percentage of maximum (0-100%)
robot.robot.setSpeed(50)        # 50% of maximum speed
robot.robot.setSpeed(100)       # 100% (maximum speed)
robot.robot.setSpeed(25)        # 25% (slow, careful movements)

# Set acceleration as percentage (0-100%)
robot.robot.setAcceleration(50) # 50% of maximum acceleration
```

### 2. Speed in mm/s or deg/s

```python
# Set linear speed (mm/s) for Cartesian movements
robot.robot.setSpeed(100, linear=True)    # 100 mm/s

# Set joint speed (deg/s) for joint movements  
robot.robot.setSpeed(45, linear=False)    # 45 degrees/s per joint
```

### 3. Speed Zones for Rounding

```python
# Set rounding radius for smooth corners (in mm)
robot.robot.setRounding(5)      # 5mm rounding radius
robot.robot.setRounding(0)      # Sharp corners (stop at each point)
```

---

## Enhanced RobotController with Speed Control

### Updated Code Example

Here's how to add speed control to your RobotController:

```python
class RobotController:
    def __init__(self, robot_name=None, speed=50):
        """
        Initialize with speed control.
        
        Args:
            robot_name: Name of robot in RoboDK
            speed: Speed percentage (0-100), default 50%
        """
        self.rdk = Robolink()
        
        if robot_name:
            self.robot = self.rdk.Item(robot_name, robolink.ITEM_TYPE_ROBOT)
        else:
            self.robot = self.rdk.Item('', robolink.ITEM_TYPE_ROBOT)
        
        if not self.robot.Valid():
            raise Exception("Robot not found")
        
        # Set initial speed
        self.set_speed(speed)
        self.set_acceleration(50)
    
    def set_speed(self, speed_percent):
        """
        Set robot speed.
        
        Args:
            speed_percent: Speed as percentage (0-100)
        """
        if not 0 <= speed_percent <= 100:
            raise ValueError("Speed must be between 0 and 100")
        
        self.robot.setSpeed(speed_percent)
        print(f"Speed set to {speed_percent}%")
    
    def set_acceleration(self, accel_percent):
        """
        Set robot acceleration.
        
        Args:
            accel_percent: Acceleration as percentage (0-100)
        """
        if not 0 <= accel_percent <= 100:
            raise ValueError("Acceleration must be between 0 and 100")
        
        self.robot.setAcceleration(accel_percent)
        print(f"Acceleration set to {accel_percent}%")
    
    def set_rounding(self, radius_mm):
        """
        Set corner rounding radius.
        
        Args:
            radius_mm: Rounding radius in mm (0 = sharp corners)
        """
        self.robot.setRounding(radius_mm)
        print(f"Rounding set to {radius_mm}mm")
```

### Usage Examples

#### Example 1: Slow and Careful Movement
```python
robot = RobotController()
robot.set_speed(25)           # 25% speed - very slow
robot.set_acceleration(25)    # 25% acceleration - gentle

# Good for: Testing, delicate operations, safety
robot.pick_object([400, 200, 100], [0, 90, 0])
```

#### Example 2: Fast Movement
```python
robot.set_speed(100)          # 100% speed - maximum
robot.set_acceleration(75)    # 75% acceleration - fast but controlled

# Good for: Production, when path is tested and safe
robot.move_to_home()
```

#### Example 3: Smooth Curved Path
```python
robot.set_speed(50)           # Medium speed
robot.set_rounding(10)        # 10mm rounding - smooth corners

# Good for: Continuous paths, avoiding sudden stops
waypoints = [
    [400, 0, 300, 0, 90, 0],
    [400, 200, 300, 0, 90, 0],
    [300, 200, 300, 0, 90, 0]
]

for waypoint in waypoints:
    robot.move_to_pose(waypoint)
```

#### Example 4: Variable Speed Operation
```python
robot = RobotController()

# Phase 1: Approach slowly
robot.set_speed(30)
robot.move_to_pose([400, 200, 150, 0, 90, 0])  # Above object

# Phase 2: Pick at very slow speed
robot.set_speed(10)
robot.pick_object([400, 200, 100], [0, 90, 0])

# Phase 3: Move quickly to place location
robot.set_speed(75)
robot.move_to_pose([400, -200, 150, 0, 90, 0])

# Phase 4: Place carefully
robot.set_speed(10)
robot.place_object([400, -200, 100], [0, 90, 0])

# Phase 5: Return home at normal speed
robot.set_speed(50)
robot.move_to_home()
```

---

## Speed Recommendations

### Safety First Approach

| Operation | Recommended Speed | Reason |
|-----------|------------------|--------|
| **First testing** | 10-25% | Safe testing, easy to stop |
| **Pick/Place operations** | 25-50% | Controlled, accurate |
| **Moving between positions** | 50-75% | Efficient transport |
| **Emergency/Critical** | 10-15% | Maximum control |
| **Production (tested)** | 75-100% | Maximum efficiency |

### UR5 Typical Speeds

| Speed Type | Typical Value |
|------------|---------------|
| Maximum joint speed | 180 deg/s |
| Maximum TCP speed | 1000 mm/s |
| Recommended testing | 50-100 mm/s |
| Recommended production | 250-750 mm/s |

---

## Practical Examples

### Example 1: Testing New Positions

```python
from robot_controller import RobotController

robot = RobotController()

# START SLOW for testing
robot.set_speed(15)
robot.set_acceleration(20)

print("Testing new pick position...")
pick_pos = [350, 150, 80]
pick_orient = [0, 90, 0]  # Straight down

# Test the movement
robot.pick_object(pick_pos, pick_orient)
print("Position looks good!")

# If successful, increase speed for production
robot.set_speed(50)
```

### Example 2: Different Orientations

```python
robot = RobotController()
robot.set_speed(40)

# Test different approach angles for the same position
position = [400, 200, 100]

# Test 1: From above
print("Test 1: Approach from above")
robot.pick_object(position, [0, 90, 0])
robot.wait(1)

# Test 2: Tilted approach
print("Test 2: Tilted approach")
robot.pick_object(position, [0, 60, 0])  # 60° angle
robot.wait(1)

# Test 3: Different tool rotation
print("Test 3: Rotated 45°")
robot.pick_object(position, [0, 90, 45])  # Rotated around Z
robot.wait(1)
```

### Example 3: Circular Motion with Speed

```python
import math

robot = RobotController()
robot.set_speed(60)
robot.set_rounding(15)  # Smooth circular motion

# Create circular path
center_x = 400
center_y = 0
z_height = 300
radius = 100

for i in range(12):  # 12 points around circle
    angle = 2 * math.pi * i / 12
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    
    # Tool always points down
    orientation = [0, 90, 0]
    
    robot.move_to_pose([x, y, z_height, 0, 90, 0])

print("Circular motion complete!")
```

---

## Tips and Best Practices

### Orientation Tips

1. **Start with standard orientations**:
   - `[0, 90, 0]` for vertical (most common)
   - `[0, 0, 0]` for horizontal
   
2. **Test orientations in simulation first**
   
3. **Check for singularities**: Some orientations may cause robot singularities

4. **Consider workspace limits**: Some positions may only be reachable with specific orientations

### Speed Tips

1. **Always start slow** (10-25%) when testing new positions

2. **Increase gradually**: 25% → 50% → 75% → 100%

3. **Use slow speeds near objects** to prevent damage

4. **Use high speeds for free movement** between waypoints

5. **Emergency stop should always be accessible**

6. **Monitor robot behavior**: Listen for unusual sounds, watch for vibrations

---

## Quick Reference Card

### Orientation Quick Reference
```python
# Common orientations for UR5
STRAIGHT_DOWN = [0, 90, 0]
HORIZONTAL = [0, 0, 0]
ANGLED_45 = [0, 45, 0]
ROTATED_90 = [0, 90, 90]
```

### Speed Quick Reference
```python
# Speed presets
TESTING_SPEED = 15        # Safe for first tests
CAREFUL_SPEED = 25        # Delicate operations
NORMAL_SPEED = 50         # Standard operations
FAST_SPEED = 75           # Quick movements
MAXIMUM_SPEED = 100       # Production (use carefully)

robot.set_speed(TESTING_SPEED)
```

---

## Troubleshooting

### Orientation Issues

**Problem**: Robot can't reach position with specified orientation
- **Solution**: Try different orientation angles
- **Solution**: Check if position is at edge of workspace
- **Solution**: Verify orientation values are in degrees, not radians

**Problem**: Robot moves to strange positions
- **Solution**: Double-check orientation format `[rx, ry, rz]`
- **Solution**: Ensure values are in correct order
- **Solution**: Check that you're using degrees (0-360)

### Speed Issues

**Problem**: Robot moves too fast and overshoots
- **Solution**: Reduce speed percentage
- **Solution**: Reduce acceleration
- **Solution**: Increase rounding for smoother motion

**Problem**: Robot moves jerkily
- **Solution**: Check acceleration settings
- **Solution**: Ensure smooth path planning
- **Solution**: Add rounding to corners

**Problem**: Speed setting doesn't work
- **Solution**: Call `setSpeed()` before movement commands
- **Solution**: Check RoboDK connection
- **Solution**: Verify speed value is 0-100

---

## Additional Resources

- **RoboDK Documentation**: https://robodk.com/doc/en/PythonAPI/
- **UR5 Manual**: https://www.universal-robots.com/
- **Our Example Files**: 
  - `simple_test.py` - Basic movements
  - `custom_test.py` - Advanced patterns with speed control
  - `test_local.py` - Comprehensive testing

---

## Summary

**Orientation** = How the robot tool is rotated (rx, ry, rz in degrees)
- `[0, 90, 0]` = Standard downward pointing
- Experiment with different angles for different tasks

**Speed** = How fast the robot moves (0-100%)
- Start at 10-25% for testing
- Use 50% for normal operations
- Use 75-100% only when path is proven safe

Always prioritize **SAFETY** over speed!
