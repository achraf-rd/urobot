"""
Custom Test Script Template

Modify this script to test your own custom pick and place sequences.
Replace the positions and orientations with your specific requirements.

Usage:
    python custom_test.py
"""

from robot_controller import RobotController
import time


def my_custom_sequence(robot):
    """
    Define your custom sequence here.
    Modify the positions and operations as needed.
    """
    
    print("\n" + "=" * 60)
    print("  Running Custom Sequence")
    print("=" * 60)
    
    # ============================================================
    # CUSTOMIZE THESE VALUES FOR YOUR APPLICATION
    # ============================================================
    
    # Pick location 1
    pick_1_position = [350, 150, 80]
    pick_1_orientation = [0, 90, 0]
    
    # Place location 1
    place_1_position = [350, -150, 80]
    place_1_orientation = [0, 90, 0]
    
    # Pick location 2
    pick_2_position = [450, 100, 80]
    pick_2_orientation = [0, 90, 0]
    
    # Place location 2
    place_2_position = [300, 0, 120]
    place_2_orientation = [0, 90, 0]
    
    # ============================================================
    # SEQUENCE EXECUTION
    # ============================================================
    
    try:
        # Start at home
        print("\nMoving to home position...")
        robot.move_to_home()
        robot.wait(1.0)
        
        # Operation 1: Pick from location 1
        print("\n[Operation 1] Picking from location 1...")
        print(f"  Position: {pick_1_position}")
        robot.pick_object(pick_1_position, pick_1_orientation)
        robot.wait(0.5)
        
        # Operation 2: Place at location 1
        print("\n[Operation 2] Placing at location 1...")
        print(f"  Position: {place_1_position}")
        robot.place_object(place_1_position, place_1_orientation)
        robot.wait(0.5)
        
        # Operation 3: Pick from location 2
        print("\n[Operation 3] Picking from location 2...")
        print(f"  Position: {pick_2_position}")
        robot.pick_object(pick_2_position, pick_2_orientation)
        robot.wait(0.5)
        
        # Operation 4: Place at location 2
        print("\n[Operation 4] Placing at location 2...")
        print(f"  Position: {place_2_position}")
        robot.place_object(place_2_position, place_2_orientation)
        robot.wait(0.5)
        
        # Return to home
        print("\nReturning to home position...")
        robot.move_to_home()
        
        print("\n✓ Custom sequence completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during sequence: {e}")
        return False


def test_multiple_poses(robot):
    """
    Test moving to multiple poses in sequence.
    Useful for testing waypoints or intermediate positions.
    """
    
    print("\n" + "=" * 60)
    print("  Testing Multiple Poses")
    print("=" * 60)
    
    # Define waypoints
    waypoints = [
        [400, 0, 300, 0, 90, 0],      # Forward
        [350, 200, 300, 0, 90, 0],    # Right
        [350, -200, 300, 0, 90, 0],   # Left
        [300, 0, 400, 0, 90, 0],      # High center
        [450, 0, 200, 0, 90, 0],      # Low forward
    ]
    
    try:
        for i, pose in enumerate(waypoints, 1):
            print(f"\nWaypoint {i}: {pose}")
            robot.move_to_pose(pose)
            robot.wait(1.0)
        
        print("\n✓ All waypoints reached!")
        robot.move_to_home()
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_circular_pattern(robot):
    """
    Test moving in a circular pattern.
    Demonstrates smooth motion through multiple points.
    """
    
    print("\n" + "=" * 60)
    print("  Testing Circular Pattern")
    print("=" * 60)
    
    import math
    
    # Circle parameters
    center_x = 400
    center_y = 0
    z_height = 300
    radius = 150
    num_points = 8
    
    try:
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            pose = [x, y, z_height, 0, 90, 0]
            print(f"\nPoint {i+1}/{num_points}: ({x:.1f}, {y:.1f}, {z_height})")
            robot.move_to_pose(pose)
            robot.wait(0.5)
        
        print("\n✓ Circular pattern completed!")
        robot.move_to_home()
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_pick_place_grid(robot):
    """
    Test picking and placing objects in a grid pattern.
    Useful for palletizing or organized storage applications.
    """
    
    print("\n" + "=" * 60)
    print("  Testing Grid Pick and Place")
    print("=" * 60)
    
    # Grid parameters
    start_x = 300
    start_y = -150
    z_height = 80
    spacing_x = 100
    spacing_y = 100
    rows = 2
    cols = 3
    
    try:
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                
                print(f"\n[Grid {row},{col}] Position: ({x}, {y}, {z_height})")
                
                # Pick
                print(f"  Picking...")
                robot.pick_object([x, y, z_height], [0, 90, 0])
                robot.wait(0.3)
                
                # Place (offset to the right)
                place_x = x + 50
                print(f"  Placing at ({place_x}, {y}, {z_height})...")
                robot.place_object([place_x, y, z_height], [0, 90, 0])
                robot.wait(0.3)
        
        print("\n✓ Grid pattern completed!")
        robot.move_to_home()
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  Custom Robot Test Script")
    print("=" * 60)
    
    try:
        # Connect to robot
        print("\nConnecting to robot...")
        robot = RobotController()
        print(f"✓ Connected to: {robot.robot.Name()}\n")
        
        # Show menu
        print("Select test to run:")
        print("  1 - Custom sequence (edit my_custom_sequence function)")
        print("  2 - Multiple poses test")
        print("  3 - Circular pattern")
        print("  4 - Grid pick and place")
        print("  5 - Run all tests")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            my_custom_sequence(robot)
        elif choice == '2':
            test_multiple_poses(robot)
        elif choice == '3':
            test_circular_pattern(robot)
        elif choice == '4':
            test_pick_place_grid(robot)
        elif choice == '5':
            print("\nRunning all tests...\n")
            my_custom_sequence(robot)
            input("\nPress ENTER to continue...")
            test_multiple_poses(robot)
            input("\nPress ENTER to continue...")
            test_circular_pattern(robot)
            input("\nPress ENTER to continue...")
            test_pick_place_grid(robot)
        else:
            print("Invalid choice")
        
        # Cleanup
        robot.disconnect()
        print("\n✓ Test completed!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure RoboDK is running with a robot loaded.")


if __name__ == "__main__":
    main()
