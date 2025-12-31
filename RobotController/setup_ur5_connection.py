"""
RoboDK Setup and Connection Guide for UR5

This guide shows you how to:
1. Set up RoboDK with a UR5 robot
2. Connect to the robot from Python code
3. Troubleshoot connection issues
"""

# ============================================================================
# STEP 1: Install RoboDK Python API
# ============================================================================
# Run this in your terminal:
# pip install robodk

# ============================================================================
# STEP 2: Start RoboDK Software
# ============================================================================
# 1. Open RoboDK application on your computer
# 2. The software should start with an empty workspace

# ============================================================================
# STEP 3: Load a UR5 Robot in RoboDK
# ============================================================================

"""
Option A: Load from RoboDK Library
----------------------------------
1. In RoboDK, go to: File → Open online library
2. Navigate to: Robots → Universal Robots → UR5
3. Double-click on UR5 to load it into your station
4. The robot will appear in the station tree

Option B: Using the Robot Library Panel
---------------------------------------
1. In RoboDK, click on the "Library" button (book icon)
2. Search for "UR5"
3. Drag and drop UR5 into the main window

Option C: Create New Station with UR5
-------------------------------------
1. File → New Station
2. Select "Add robot from library"
3. Choose Universal Robots → UR5
4. Click OK
"""

# ============================================================================
# STEP 4: Verify Robot is Loaded
# ============================================================================

"""
In the RoboDK station tree (left panel), you should see:
- Station (root)
  └── UR5  (or "UR5 Base" depending on version)
      └── Tool
          └── TCP

The robot name in the tree is what you'll use in your code.
"""

# ============================================================================
# EXAMPLE 1: Connect to UR5 (Method 1 - By Name)
# ============================================================================

from robodk.robolink import Robolink, ITEM_TYPE_ROBOT

# Connect to RoboDK
rdk = Robolink()

# Get robot by name
robot = rdk.Item('UR5', ITEM_TYPE_ROBOT)

# Check if connection is successful
if not robot.Valid():
    print("❌ Failed to connect to UR5")
    print("Make sure:")
    print("  1. RoboDK is running")
    print("  2. A UR5 robot is loaded in the station")
    print("  3. The robot name matches (check station tree)")
else:
    print(f"✅ Connected to robot: {robot.Name()}")
    print(f"   Robot type: {robot.Type()}")

# ============================================================================
# EXAMPLE 2: Connect to UR5 (Method 2 - First Available Robot)
# ============================================================================

from robodk.robolink import Robolink, ITEM_TYPE_ROBOT

# Connect to RoboDK
rdk = Robolink()

# Get first available robot (use this if you only have one robot)
robot = rdk.Item('', ITEM_TYPE_ROBOT)

if robot.Valid():
    print(f"✅ Connected to robot: {robot.Name()}")
else:
    print("❌ No robot found in the station")

# ============================================================================
# EXAMPLE 3: Connect to UR5 (Method 3 - List All Robots)
# ============================================================================

from robodk.robolink import Robolink, ITEM_TYPE_ROBOT

# Connect to RoboDK
rdk = Robolink()

# Get all robots in the station
robots = rdk.ItemList(ITEM_TYPE_ROBOT)

if len(robots) == 0:
    print("❌ No robots found in the station")
else:
    print(f"✅ Found {len(robots)} robot(s):")
    for i, robot in enumerate(robots, 1):
        print(f"   {i}. {robot.Name()}")
    
    # Use the first robot
    robot = robots[0]
    print(f"\n✅ Using robot: {robot.Name()}")

# ============================================================================
# EXAMPLE 4: Using RobotController with UR5
# ============================================================================

from robot_controller import RobotController

# Method A: Connect to robot named "UR5"
robot_controller = RobotController(robot_name="UR5")

# Method B: Connect to first available robot
robot_controller = RobotController()  # Will use first robot it finds

# Method C: Connect to robot with specific name (if you renamed it in RoboDK)
robot_controller = RobotController(robot_name="UR5 Base")

# ============================================================================
# EXAMPLE 5: Complete Connection Test
# ============================================================================

def test_ur5_connection():
    """
    Complete test to verify UR5 connection and basic operations.
    """
    from robodk.robolink import Robolink, ITEM_TYPE_ROBOT
    import sys
    
    print("=" * 60)
    print("  UR5 Connection Test")
    print("=" * 60)
    
    # Step 1: Connect to RoboDK
    print("\n1. Connecting to RoboDK...")
    try:
        rdk = Robolink()
        print("   ✅ Connected to RoboDK")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print("   → Make sure RoboDK is running")
        return False
    
    # Step 2: Check RoboDK version
    print("\n2. Checking RoboDK version...")
    try:
        version = rdk.Version()
        print(f"   ✅ RoboDK Version: {version}")
    except:
        print("   ⚠️  Could not get version")
    
    # Step 3: List all items in station
    print("\n3. Station contents:")
    try:
        station = rdk.ActiveStation()
        print(f"   Station: {station.Name()}")
        
        # List all robots
        robots = rdk.ItemList(ITEM_TYPE_ROBOT)
        print(f"   Robots found: {len(robots)}")
        for robot in robots:
            print(f"     • {robot.Name()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 4: Connect to UR5
    print("\n4. Connecting to UR5 robot...")
    robot = rdk.Item('UR5', ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("   ❌ UR5 not found by name, trying first available robot...")
        robot = rdk.Item('', ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("   ❌ No robot available")
        print("\n   Troubleshooting:")
        print("   1. Load UR5 in RoboDK: File → Open online library → UR5")
        print("   2. Check the robot name in the station tree")
        print("   3. Make sure RoboDK station is active")
        return False
    
    print(f"   ✅ Connected to: {robot.Name()}")
    
    # Step 5: Get robot info
    print("\n5. Robot information:")
    try:
        joints = robot.Joints()
        pose = robot.Pose()
        
        print(f"   Number of joints: {len(joints.list())}")
        print(f"   Current joints: {[f'{j:.2f}°' for j in joints.list()]}")
        print(f"   Robot is connected and responsive")
        
        return True
    except Exception as e:
        print(f"   ❌ Error getting robot info: {e}")
        return False

# ============================================================================
# RUN THE TEST
# ============================================================================

if __name__ == "__main__":
    print("\n")
    success = test_ur5_connection()
    
    if success:
        print("\n" + "=" * 60)
        print("  ✅ CONNECTION SUCCESSFUL!")
        print("=" * 60)
        print("\nYou can now use:")
        print("  • python simple_test.py")
        print("  • python test_local.py")
        print("  • python main.py (for network server)")
        print("\n")
    else:
        print("\n" + "=" * 60)
        print("  ❌ CONNECTION FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above and try again.\n")
