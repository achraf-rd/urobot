"""
Local Testing Script for RobotController

This script tests all RobotController functions in the RoboDK simulator.
Run this script with RoboDK open and a robot loaded.

Usage:
    python test_local.py
"""

import time
from robot_controller import RobotController


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_connection():
    """Test 1: Connect to the robot."""
    print_section("TEST 1: Robot Connection")
    
    try:
        robot = RobotController()
        print("✓ Successfully connected to robot")
        print(f"  Robot name: {robot.robot.Name()}")
        return robot
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        print("\nMake sure:")
        print("  1. RoboDK is running")
        print("  2. A robot is loaded in the station")
        print("  3. RoboDK API is installed: pip install robodk")
        return None


def test_get_current_state(robot):
    """Test 2: Get current robot state."""
    print_section("TEST 2: Get Current State")
    
    try:
        joints = robot.get_current_joints()
        pose = robot.get_current_pose()
        
        print("✓ Current Joint Angles (degrees):")
        for i, angle in enumerate(joints, 1):
            print(f"    Joint {i}: {angle:.2f}°")
        
        print("\n✓ Current Pose (x, y, z, rx, ry, rz):")
        print(f"    Position: ({pose[0]:.2f}, {pose[1]:.2f}, {pose[2]:.2f}) mm")
        print(f"    Orientation: ({pose[3]:.2f}, {pose[4]:.2f}, {pose[5]:.2f})°")
        
        return True
    except Exception as e:
        print(f"✗ Failed to get state: {e}")
        return False


def test_move_home(robot):
    """Test 3: Move to home position."""
    print_section("TEST 3: Move to Home Position")
    
    try:
        print("Moving to home position...")
        success = robot.move_to_home()
        
        if success:
            print("✓ Successfully moved to home")
            joints = robot.get_current_joints()
            print(f"  Home joint angles: {[f'{j:.2f}' for j in joints]}")
        else:
            print("✗ Move to home failed")
        
        return success
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_wait(robot):
    """Test 4: Wait function."""
    print_section("TEST 4: Wait Function")
    
    try:
        wait_time = 2.0
        print(f"Waiting for {wait_time} seconds...")
        start = time.time()
        robot.wait(wait_time)
        elapsed = time.time() - start
        print(f"✓ Wait completed (actual time: {elapsed:.2f}s)")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_move_to_pose(robot):
    """Test 5: Move to specific poses."""
    print_section("TEST 5: Move to Specific Poses")
    
    # Define some test poses
    test_poses = [
        {
            "name": "Pose 1 - Forward position",
            "pose": [400, 0, 300, 0, 90, 0]
        },
        {
            "name": "Pose 2 - Right position",
            "pose": [300, 200, 300, 0, 90, 0]
        },
        {
            "name": "Pose 3 - Left position",
            "pose": [300, -200, 300, 0, 90, 0]
        }
    ]
    
    try:
        for test in test_poses:
            print(f"\n→ Testing: {test['name']}")
            print(f"  Target: {test['pose']}")
            
            success = robot.move_to_pose(test['pose'])
            
            if success:
                actual_pose = robot.get_current_pose()
                print(f"  ✓ Move successful")
                print(f"  Actual: [{actual_pose[0]:.1f}, {actual_pose[1]:.1f}, "
                      f"{actual_pose[2]:.1f}, {actual_pose[3]:.1f}, "
                      f"{actual_pose[4]:.1f}, {actual_pose[5]:.1f}]")
            else:
                print(f"  ✗ Move failed")
                return False
            
            robot.wait(1.0)
        
        print("\n✓ All pose moves completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_pick_operation(robot):
    """Test 6: Pick operation."""
    print_section("TEST 6: Pick Operation")
    
    # Define pick location
    pick_position = [350, 150, 100]
    pick_orientation = [0, 90, 0]
    
    try:
        print(f"Pick position: {pick_position}")
        print(f"Pick orientation: {pick_orientation}")
        print("\nExecuting pick operation...")
        
        success = robot.pick_object(pick_position, pick_orientation)
        
        if success:
            print("✓ Pick operation completed successfully")
            pose = robot.get_current_pose()
            print(f"  Final position: [{pose[0]:.1f}, {pose[1]:.1f}, {pose[2]:.1f}]")
        else:
            print("✗ Pick operation failed")
        
        return success
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_place_operation(robot):
    """Test 7: Place operation."""
    print_section("TEST 7: Place Operation")
    
    # Define place location
    place_position = [350, -150, 100]
    place_orientation = [0, 90, 0]
    
    try:
        print(f"Place position: {place_position}")
        print(f"Place orientation: {place_orientation}")
        print("\nExecuting place operation...")
        
        success = robot.place_object(place_position, place_orientation)
        
        if success:
            print("✓ Place operation completed successfully")
            pose = robot.get_current_pose()
            print(f"  Final position: [{pose[0]:.1f}, {pose[1]:.1f}, {pose[2]:.1f}]")
        else:
            print("✗ Place operation failed")
        
        return success
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_complete_pick_and_place_sequence(robot):
    """Test 8: Complete pick and place sequence."""
    print_section("TEST 8: Complete Pick and Place Sequence")
    
    # Define pick and place positions
    sequence = [
        {
            "operation": "pick",
            "position": [400, 200, 80],
            "orientation": [0, 90, 0],
            "description": "Pick from right side"
        },
        {
            "operation": "place",
            "position": [400, -200, 80],
            "orientation": [0, 90, 0],
            "description": "Place on left side"
        },
        {
            "operation": "pick",
            "position": [450, 0, 80],
            "orientation": [0, 90, 0],
            "description": "Pick from center"
        },
        {
            "operation": "place",
            "position": [350, 0, 120],
            "orientation": [0, 90, 0],
            "description": "Place at elevated position"
        }
    ]
    
    try:
        print("Starting complete pick and place sequence...\n")
        
        for i, step in enumerate(sequence, 1):
            print(f"Step {i}: {step['description']}")
            print(f"  Position: {step['position']}")
            print(f"  Orientation: {step['orientation']}")
            
            if step['operation'] == 'pick':
                success = robot.pick_object(step['position'], step['orientation'])
            else:
                success = robot.place_object(step['position'], step['orientation'])
            
            if success:
                print(f"  ✓ {step['operation'].capitalize()} completed")
            else:
                print(f"  ✗ {step['operation'].capitalize()} failed")
                return False
            
            # Small delay between operations
            robot.wait(0.5)
            print()
        
        # Return to home at the end
        print("Returning to home position...")
        robot.move_to_home()
        
        print("✓ Complete sequence finished successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error during sequence: {e}")
        return False


def run_all_tests():
    """Run all tests in sequence."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ROBOT CONTROLLER TEST SUITE" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Test 1: Connection
    robot = test_connection()
    if not robot:
        print("\n✗ Cannot proceed without robot connection")
        return
    
    input("\nPress ENTER to continue with testing...")
    
    # Test 2: Get current state
    test_get_current_state(robot)
    input("\nPress ENTER to continue...")
    
    # Test 3: Move to home
    test_move_home(robot)
    input("\nPress ENTER to continue...")
    
    # Test 4: Wait function
    test_wait(robot)
    input("\nPress ENTER to continue...")
    
    # Test 5: Move to poses
    test_move_to_pose(robot)
    input("\nPress ENTER to continue...")
    
    # Return to home before pick/place tests
    robot.move_to_home()
    robot.wait(1.0)
    
    # Test 6: Pick operation
    test_pick_operation(robot)
    input("\nPress ENTER to continue...")
    
    # Test 7: Place operation
    test_place_operation(robot)
    input("\nPress ENTER to continue...")
    
    # Return to home
    robot.move_to_home()
    robot.wait(1.0)
    
    # Test 8: Complete sequence
    test_complete_pick_and_place_sequence(robot)
    
    # Final summary
    print_section("TEST SUMMARY")
    print("✓ All tests completed!")
    print("\nRobot is ready for use.")
    print("You can now:")
    print("  - Run the network server: python main.py")
    print("  - Send commands from Raspberry Pi using client_example.py")
    
    # Cleanup
    robot.disconnect()


def quick_demo():
    """Quick demo without pauses - for automated testing."""
    print_section("QUICK DEMO MODE")
    
    robot = test_connection()
    if not robot:
        return
    
    print("\nRunning quick demonstration...")
    
    # Quick sequence
    robot.move_to_home()
    robot.wait(1.0)
    
    # Pick and place
    robot.pick_object([400, 150, 100], [0, 90, 0])
    robot.wait(0.5)
    
    robot.place_object([400, -150, 100], [0, 90, 0])
    robot.wait(0.5)
    
    # Return home
    robot.move_to_home()
    
    print("\n✓ Quick demo completed!")
    robot.disconnect()


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 70)
    print("  Robot Controller - Local Simulator Test")
    print("=" * 70)
    print("\nSelect test mode:")
    print("  1 - Full test suite (with pauses)")
    print("  2 - Quick demo (automated)")
    print("  3 - Individual function test")
    print("=" * 70)
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        run_all_tests()
    elif choice == '2':
        quick_demo()
    elif choice == '3':
        robot = test_connection()
        if robot:
            print("\nIndividual Tests:")
            print("  a - Get current state")
            print("  b - Move to home")
            print("  c - Move to pose")
            print("  d - Pick operation")
            print("  e - Place operation")
            print("  f - Complete sequence")
            
            test_choice = input("\nSelect test: ").strip().lower()
            
            if test_choice == 'a':
                test_get_current_state(robot)
            elif test_choice == 'b':
                test_move_home(robot)
            elif test_choice == 'c':
                test_move_to_pose(robot)
            elif test_choice == 'd':
                test_pick_operation(robot)
            elif test_choice == 'e':
                test_place_operation(robot)
            elif test_choice == 'f':
                test_complete_pick_and_place_sequence(robot)
            else:
                print("Invalid choice")
            
            robot.disconnect()
    else:
        print("Invalid choice")
