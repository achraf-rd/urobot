"""
Quick UR5 Connection Script

Run this script to verify your UR5 connection before using the full robot controller.
This script will help you identify the correct robot name to use.

Usage:
    python connect_ur5.py
"""

from robodk.robolink import Robolink, ITEM_TYPE_ROBOT
import sys


def find_and_connect_ur5():
    """
    Find and connect to UR5 robot in RoboDK.
    """
    print("\n" + "=" * 70)
    print("  UR5 Robot Connection Helper")
    print("=" * 70)
    
    # Step 1: Connect to RoboDK
    print("\n[Step 1] Connecting to RoboDK API...")
    try:
        rdk = Robolink()
        print("  ✅ RoboDK API connected")
    except Exception as e:
        print(f"  ❌ Failed to connect to RoboDK: {e}")
        print("\n  Troubleshooting:")
        print("    • Make sure RoboDK software is running")
        print("    • Try restarting RoboDK")
        return None
    
    # Step 2: Check if RoboDK is running
    print("\n[Step 2] Checking RoboDK status...")
    try:
        station = rdk.ActiveStation()
        if station.Valid():
            print(f"  ✅ Active station: {station.Name()}")
        else:
            print("  ⚠️  No active station found")
            print("     Create a new station in RoboDK")
    except Exception as e:
        print(f"  ⚠️  Warning: {e}")
    
    # Step 3: List all robots
    print("\n[Step 3] Searching for robots in station...")
    try:
        robots = rdk.ItemList(ITEM_TYPE_ROBOT)
        
        if len(robots) == 0:
            print("  ❌ No robots found in the station!")
            print("\n  How to add UR5 robot:")
            print("    1. In RoboDK: File → Open online library")
            print("    2. Navigate to: Robots → Universal Robots → UR5")
            print("    3. Double-click UR5 to add it to your station")
            print("    4. Run this script again")
            return None
        
        print(f"  ✅ Found {len(robots)} robot(s):")
        for i, robot in enumerate(robots, 1):
            print(f"     {i}. {robot.Name()}")
        
        # Step 4: Try to find UR5 specifically
        print("\n[Step 4] Looking for UR5 robot...")
        ur5_robot = None
        
        # Try common UR5 names
        ur5_names = ['UR5', 'UR5 Base', 'UR5e', 'Universal Robots UR5']
        
        for name in ur5_names:
            test_robot = rdk.Item(name, ITEM_TYPE_ROBOT)
            if test_robot.Valid():
                ur5_robot = test_robot
                print(f"  ✅ Found UR5 with name: '{name}'")
                break
        
        # If not found by name, check if any robot contains "UR5" in name
        if not ur5_robot:
            for robot in robots:
                if 'UR5' in robot.Name().upper() or 'UR' in robot.Name().upper():
                    ur5_robot = robot
                    print(f"  ✅ Found UR-type robot: '{robot.Name()}'")
                    break
        
        # If still not found, use first robot
        if not ur5_robot:
            ur5_robot = robots[0]
            print(f"  ⚠️  UR5 not found by name, using: '{ur5_robot.Name()}'")
        
        # Step 5: Test robot connection
        print("\n[Step 5] Testing robot connection...")
        try:
            joints = ur5_robot.Joints()
            pose = ur5_robot.Pose()
            
            print(f"  ✅ Robot is responsive!")
            print(f"     Name: {ur5_robot.Name()}")
            print(f"     DOF: {len(joints.list())} joints")
            print(f"     Joint angles: {[f'{j:.1f}°' for j in joints.list()]}")
            
            return ur5_robot
            
        except Exception as e:
            print(f"  ❌ Error communicating with robot: {e}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def test_robot_movement(robot):
    """
    Test basic robot movement.
    """
    print("\n[Step 6] Testing robot movement...")
    
    try:
        # Get current position
        current_joints = robot.Joints()
        print(f"  Current position: {[f'{j:.1f}' for j in current_joints.list()]}")
        
        # Ask user if they want to test movement
        response = input("\n  Test a small movement? (y/n): ").strip().lower()
        
        if response == 'y':
            print("  Moving joint 1 by 10 degrees...")
            test_joints = current_joints.list()
            test_joints[0] += 10  # Move first joint by 10 degrees
            
            robot.MoveJ(test_joints)
            robot.WaitMove()
            
            print("  ✅ Movement test successful!")
            
            # Move back
            print("  Returning to original position...")
            robot.MoveJ(current_joints)
            robot.WaitMove()
            print("  ✅ Returned to original position")
        else:
            print("  Skipped movement test")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Movement test failed: {e}")
        return False


def show_usage_examples(robot_name):
    """
    Show how to use the robot in your code.
    """
    print("\n" + "=" * 70)
    print("  How to Use This Robot in Your Code")
    print("=" * 70)
    
    print(f"""
1. Using RobotController class:
   
   from robot_controller import RobotController
   
   # Connect to your robot
   robot = RobotController(robot_name="{robot_name}")
   
   # Use robot methods
   robot.move_to_home()
   robot.pick_object([400, 200, 100], [0, 90, 0])
   robot.place_object([400, -200, 100], [0, 90, 0])


2. Direct RoboDK API:
   
   from robodk.robolink import Robolink, ITEM_TYPE_ROBOT
   
   rdk = Robolink()
   robot = rdk.Item('{robot_name}', ITEM_TYPE_ROBOT)
   
   # Move robot
   robot.MoveJ([0, -90, 90, 0, 90, 0])  # Joint move
   robot.WaitMove()


3. Run test scripts:
   
   python simple_test.py        # Simple pick and place test
   python test_local.py          # Full test suite
   python main.py                # Start network server
""")


def main():
    """
    Main function to test UR5 connection.
    """
    
    # Try to find and connect to UR5
    robot = find_and_connect_ur5()
    
    if robot:
        print("\n" + "=" * 70)
        print("  ✅ CONNECTION SUCCESSFUL!")
        print("=" * 70)
        
        # Test movement (optional)
        test_robot_movement(robot)
        
        # Show usage examples
        show_usage_examples(robot.Name())
        
        print("\n  You are ready to use the robot controller!\n")
        
    else:
        print("\n" + "=" * 70)
        print("  ❌ CONNECTION FAILED")
        print("=" * 70)
        print("\n  Please follow the steps above to fix the issues.\n")
        
        print("  Quick Setup Guide:")
        print("  " + "-" * 66)
        print("  1. Open RoboDK software")
        print("  2. File → Open online library")
        print("  3. Robots → Universal Robots → UR5")
        print("  4. Double-click UR5 to add it")
        print("  5. Run this script again: python connect_ur5.py")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user\n")
    except Exception as e:
        print(f"\n  ❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
