"""
Speed Control Example for RobotController

This script demonstrates how to control robot speed and acceleration
in different scenarios.

Usage:
    python speed_control_demo.py
"""

from robot_controller import RobotController
import time


def demo_speed_variations():
    """
    Demonstrate different speed settings.
    """
    print("=" * 70)
    print("  Speed Control Demonstration")
    print("=" * 70)
    
    robot = RobotController()
    
    # Define a test position
    test_position = [400, 200, 300, 0, 90, 0]
    
    # Test different speeds
    speeds = [10, 25, 50, 75, 100]
    
    for speed in speeds:
        print(f"\n→ Testing at {speed}% speed...")
        robot.robot.setSpeed(speed)
        robot.robot.setAcceleration(speed)
        
        print(f"  Moving to test position...")
        start_time = time.time()
        robot.move_to_pose(test_position)
        elapsed = time.time() - start_time
        
        print(f"  ✓ Completed in {elapsed:.2f} seconds")
        
        print(f"  Returning home...")
        robot.move_to_home()
        robot.wait(0.5)
    
    print("\n✓ Speed demonstration complete!")


def demo_variable_speed_operation():
    """
    Demonstrate using different speeds for different phases of operation.
    """
    print("\n" + "=" * 70)
    print("  Variable Speed Pick and Place")
    print("=" * 70)
    
    robot = RobotController()
    
    # Define positions
    pick_pos = [400, 200, 100]
    pick_orient = [0, 90, 0]
    place_pos = [400, -200, 100]
    place_orient = [0, 90, 0]
    
    # Phase 1: Approach at medium speed
    print("\n[Phase 1] Approaching pick location (50% speed)...")
    robot.robot.setSpeed(50)
    robot.robot.setAcceleration(50)
    approach_pose = pick_pos + pick_orient
    approach_pose[2] += 50  # 50mm above
    robot.move_to_pose(approach_pose)
    
    # Phase 2: Pick at slow speed for accuracy
    print("\n[Phase 2] Picking object (20% speed - careful)...")
    robot.robot.setSpeed(20)
    robot.robot.setAcceleration(20)
    robot.pick_object(pick_pos, pick_orient)
    
    # Phase 3: Move to place location at high speed
    print("\n[Phase 3] Moving to place location (80% speed)...")
    robot.robot.setSpeed(80)
    robot.robot.setAcceleration(70)
    approach_place = place_pos + place_orient
    approach_place[2] += 50
    robot.move_to_pose(approach_place)
    
    # Phase 4: Place at slow speed
    print("\n[Phase 4] Placing object (20% speed - careful)...")
    robot.robot.setSpeed(20)
    robot.robot.setAcceleration(20)
    robot.place_object(place_pos, place_orient)
    
    # Phase 5: Return home at normal speed
    print("\n[Phase 5] Returning home (60% speed)...")
    robot.robot.setSpeed(60)
    robot.robot.setAcceleration(60)
    robot.move_to_home()
    
    print("\n✓ Variable speed operation complete!")


def demo_smooth_vs_sharp_corners():
    """
    Demonstrate smooth vs sharp corner movements using rounding.
    """
    print("\n" + "=" * 70)
    print("  Smooth vs Sharp Corners")
    print("=" * 70)
    
    robot = RobotController()
    robot.robot.setSpeed(60)
    robot.robot.setAcceleration(60)
    
    # Define waypoints (square pattern)
    waypoints = [
        [400, 0, 300, 0, 90, 0],
        [400, 200, 300, 0, 90, 0],
        [300, 200, 300, 0, 90, 0],
        [300, 0, 300, 0, 90, 0],
        [400, 0, 300, 0, 90, 0],
    ]
    
    # Test 1: Sharp corners (stop at each point)
    print("\n[Test 1] Sharp corners (rounding = 0mm)...")
    robot.robot.setRounding(0)
    
    for i, waypoint in enumerate(waypoints, 1):
        print(f"  Waypoint {i}/{len(waypoints)}")
        robot.move_to_pose(waypoint)
    
    print("  ✓ Sharp corners complete (robot stopped at each point)")
    robot.wait(1)
    
    # Test 2: Smooth corners
    print("\n[Test 2] Smooth corners (rounding = 15mm)...")
    robot.robot.setRounding(15)
    
    for i, waypoint in enumerate(waypoints, 1):
        print(f"  Waypoint {i}/{len(waypoints)}")
        robot.move_to_pose(waypoint)
    
    print("  ✓ Smooth corners complete (continuous motion)")
    
    # Reset rounding
    robot.robot.setRounding(0)
    robot.move_to_home()
    
    print("\n✓ Corner demonstration complete!")


def demo_orientation_variations():
    """
    Demonstrate different orientations at the same position.
    """
    print("\n" + "=" * 70)
    print("  Orientation Variations")
    print("=" * 70)
    
    robot = RobotController()
    robot.robot.setSpeed(40)
    robot.robot.setAcceleration(40)
    
    # Same position, different orientations
    position = [400, 0, 250]
    
    orientations = [
        ([0, 90, 0], "Straight down (standard)"),
        ([0, 60, 0], "Tilted 60° forward"),
        ([0, 45, 0], "Tilted 45° forward"),
        ([0, 90, 45], "Straight down, rotated 45°"),
        ([0, 90, 90], "Straight down, rotated 90°"),
        ([45, 90, 0], "Rolled 45° to side"),
    ]
    
    for orient, description in orientations:
        print(f"\n→ Testing: {description}")
        print(f"  Orientation: {orient}")
        
        try:
            pose = position + orient
            robot.move_to_pose(pose)
            robot.wait(1.5)
            print(f"  ✓ Success")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
    
    robot.move_to_home()
    print("\n✓ Orientation demonstration complete!")


def main():
    """
    Main menu for speed control demonstrations.
    """
    print("\n" + "=" * 70)
    print("  Speed Control and Orientation Demo")
    print("=" * 70)
    print("\nSelect demonstration:")
    print("  1 - Speed variations (10% to 100%)")
    print("  2 - Variable speed operation (different speeds per phase)")
    print("  3 - Smooth vs sharp corners")
    print("  4 - Orientation variations")
    print("  5 - Run all demonstrations")
    print("=" * 70)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    try:
        if choice == '1':
            demo_speed_variations()
        elif choice == '2':
            demo_variable_speed_operation()
        elif choice == '3':
            demo_smooth_vs_sharp_corners()
        elif choice == '4':
            demo_orientation_variations()
        elif choice == '5':
            print("\n Running all demonstrations...")
            demo_speed_variations()
            input("\nPress ENTER to continue to next demo...")
            demo_variable_speed_operation()
            input("\nPress ENTER to continue to next demo...")
            demo_smooth_vs_sharp_corners()
            input("\nPress ENTER to continue to next demo...")
            demo_orientation_variations()
        else:
            print("Invalid choice")
            return
        
        print("\n" + "=" * 70)
        print("  All demonstrations complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  • RoboDK is running")
        print("  • UR5 robot is loaded")
        print("  • Positions are within robot reach")


if __name__ == "__main__":
    main()
