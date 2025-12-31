"""
Simple Pick and Place Test

A minimal example showing basic pick and place operations.
Perfect for quick testing and understanding the basics.

Usage:
    python simple_test.py
"""

from robot_controller import RobotController
import time


def main():
    print("=" * 60)
    print("  Simple Pick and Place Test")
    print("=" * 60)
    
    try:
        # 1. Connect to robot
        print("\n1. Connecting to robot...")
        robot = RobotController()
        print(f"   ✓ Connected to: {robot.robot.Name()}")
        
        # 2. Show current position
        print("\n2. Current robot state:")
        pose = robot.get_current_pose()
        print(f"   Position: ({pose[0]:.1f}, {pose[1]:.1f}, {pose[2]:.1f}) mm")
        print(f"   Orientation: ({pose[3]:.1f}, {pose[4]:.1f}, {pose[5]:.1f})°")
        
        # 3. Move to home
        print("\n3. Moving to home position...")
        robot.move_to_home()
        print("   ✓ At home position")
        time.sleep(7)
        
        # 4. Pick object
        print("\n4. Picking object...")
        pick_pos = [400, 200, 100]      # x, y, z in mm
        pick_orient = [0, 90, 0]        # rx, ry, rz in degrees
        print(f"   From: {pick_pos}")
        robot.pick_object(pick_pos, pick_orient)
        print("   ✓ Object picked")
        time.sleep(7)
        
        # 5. Place object
        print("\n5. Placing object...")
        place_pos = [400, -200, 100]    # x, y, z in mm
        place_orient = [0, 90, 0]       # rx, ry, rz in degrees
        print(f"   To: {place_pos}")
        robot.place_object(place_pos, place_orient)
        print("   ✓ Object placed")
        time.sleep(7)
        
        # 6. Return home
        print("\n6. Returning to home...")
        robot.move_to_home()
        print("   ✓ Back at home")
        
        print("\n" + "=" * 60)
        print("  ✓ Test completed successfully!")
        print("=" * 60)
        
        # Cleanup
        robot.disconnect()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("  • Make sure RoboDK is running")
        print("  • Verify a robot is loaded in the station")
        print("  • Check that positions are within robot reach")


if __name__ == "__main__":
    main()
