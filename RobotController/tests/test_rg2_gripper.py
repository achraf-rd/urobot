"""
RG2 Gripper Test Script
=======================
Test script for OnRobot RG2 gripper using URScript commands via RoboDK.

This test uses the actual RG2() function from your URCaps:
- RG2(60,40,0.0,True,False,False) for closing/gripping
- RG2(70,40,0.0,True,False,False) for opening/releasing
"""

import sys
import os
import time

# Add parent directory to path to import robot_controller
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robot_controller import RobotController


def test_basic_gripper():
    """Test basic gripper open and close operations."""
    print("\n" + "="*60)
    print("RG2 Gripper - Basic Open/Close Test")
    print("="*60)
    
    try:
        # Initialize robot with gripper
        print("\n1. Initializing robot controller with gripper...")
        robot = RobotController(robot_name=None, use_gripper=True)
        
        if not robot.gripper or not robot.gripper.is_connected():
            print("✗ Gripper not available")
            return False
        
        print("✓ Robot and gripper initialized")
        
        # Test 1: Open gripper (70mm)
        print("\n2. Opening gripper to 70mm...")
        success = robot.gripper_open()
        if success:
            print("✓ Gripper opened successfully")
            print("   Command sent: RG2(70,40,0.0,True,False,False)")
        else:
            print("✗ Failed to open gripper")
            return False
        
        time.sleep(2)
        
        # Get status after opening
        print("\n3. Checking gripper status after opening...")
        status = robot.gripper_status()
        if status:
            print(f"✓ Gripper status:")
            print(f"   Width: {status['width_mm']}mm")
            print(f"   Force: {status['force_n']}N")
            print(f"   Grip detected: {status['grip_detected']}")
        
        input("\nPress Enter to close gripper...")
        
        # Test 2: Close gripper (60mm)
        print("\n4. Closing gripper to 60mm...")
        success = robot.gripper_close()
        if success:
            print("✓ Gripper closed successfully")
            print("   Command sent: RG2(60,40,0.0,True,False,False)")
        else:
            print("✗ Failed to close gripper")
            return False
        
        time.sleep(2)
        
        # Get status after closing
        print("\n5. Checking gripper status after closing...")
        status = robot.gripper_status()
        if status:
            print(f"✓ Gripper status:")
            print(f"   Width: {status['width_mm']}mm")
            print(f"   Force: {status['force_n']}N")
            print(f"   Grip detected: {status['grip_detected']}")
            
            if status['grip_detected']:
                print("   ✓ Object gripped!")
        
        # Check if object gripped using helper method
        if robot.is_object_gripped():
            print("\n✓ Object detection confirmed")
        
        print("\n" + "="*60)
        print("✓ Basic test completed successfully!")
        print("="*60)
        
        # Cleanup
        robot.disconnect()
        return True
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_custom_parameters():
    """Test gripper with custom width and force parameters."""
    print("\n" + "="*60)
    print("RG2 Gripper - Custom Parameters Test")
    print("="*60)
    
    try:
        # Initialize robot
        print("\n1. Initializing robot controller...")
        robot = RobotController(use_gripper=True)
        
        if not robot.gripper or not robot.gripper.is_connected():
            print("✗ Gripper not available")
            return False
        
        print("✓ Robot initialized")
        
        # Test with custom width values
        test_cases = [
            {"width": 90, "force": 40, "action": "open"},
            {"width": 50, "force": 35, "action": "close"},
            {"width": 80, "force": 30, "action": "open"},
            {"width": 40, "force": 40, "action": "close"},
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n{i+1}. Testing {test['action']} with width={test['width']}mm, force={test['force']}N")
            
            if test['action'] == 'open':
                success = robot.gripper_open(width_mm=test['width'], force_n=test['force'])
                print(f"   Command: RG2({test['width']},{test['force']},0.0,True,False,False)")
            else:
                success = robot.gripper_close(width_mm=test['width'], force_n=test['force'])
                print(f"   Command: RG2({test['width']},{test['force']},0.0,True,False,False)")
            
            if success:
                print(f"   ✓ Gripper {test['action']} successful")
            else:
                print(f"   ✗ Gripper {test['action']} failed")
            
            time.sleep(1.5)
            
            # Show status
            status = robot.gripper_status()
            if status:
                print(f"   Status: width={status['width_mm']}mm, gripped={status['grip_detected']}")
        
        print("\n" + "="*60)
        print("✓ Custom parameters test completed!")
        print("="*60)
        
        # Cleanup
        robot.disconnect()
        return True
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pick_and_place_simulation():
    """Simulate a pick and place sequence with gripper."""
    print("\n" + "="*60)
    print("RG2 Gripper - Pick & Place Simulation")
    print("="*60)
    print("(Only gripper actions, no robot movement)")
    
    try:
        # Initialize robot
        print("\n1. Initializing robot controller...")
        robot = RobotController(use_gripper=True)
        
        if not robot.gripper or not robot.gripper.is_connected():
            print("✗ Gripper not available")
            return False
        
        print("✓ Robot initialized")
        
        # Pick sequence
        print("\n" + "-"*60)
        print("PICK SEQUENCE")
        print("-"*60)
        
        print("\n2. Opening gripper to approach object...")
        robot.gripper_open(width_mm=80, force_n=40)
        print("   Command: RG2(80,40,0.0,True,False,False)")
        time.sleep(1.5)
        
        print("\n3. Moving to pick position (simulated)...")
        time.sleep(1)
        
        print("\n4. Closing gripper to grip object...")
        robot.gripper_close(width_mm=60, force_n=40)
        print("   Command: RG2(60,40,0.0,True,False,False)")
        time.sleep(1.5)
        
        print("\n5. Checking if object gripped...")
        if robot.is_object_gripped():
            print("   ✓ Object gripped successfully!")
        else:
            print("   ⚠ No object detected")
        
        status = robot.gripper_status()
        if status:
            print(f"   Current width: {status['width_mm']}mm")
        
        print("\n6. Lifting object (simulated)...")
        time.sleep(1)
        
        # Place sequence
        print("\n" + "-"*60)
        print("PLACE SEQUENCE")
        print("-"*60)
        
        print("\n7. Moving to place position (simulated)...")
        time.sleep(1)
        
        print("\n8. Opening gripper to release object...")
        robot.gripper_open(width_mm=70, force_n=40)
        print("   Command: RG2(70,40,0.0,True,False,False)")
        time.sleep(1.5)
        
        print("\n9. Object released")
        status = robot.gripper_status()
        if status:
            print(f"   Current width: {status['width_mm']}mm")
            print(f"   Grip detected: {status['grip_detected']}")
        
        print("\n10. Returning to safe position (simulated)...")
        time.sleep(1)
        
        print("\n" + "="*60)
        print("✓ Pick & Place simulation completed!")
        print("="*60)
        
        # Cleanup
        robot.disconnect()
        return True
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test menu."""
    print("\n" + "="*60)
    print("RG2 Gripper Test Suite")
    print("Using URScript: RG2(width, force, payload, set_payload, depth_comp, slave)")
    print("="*60)
    print("\nDefault values:")
    print("  - Close/Grip: RG2(60,40,0.0,True,False,False)")
    print("  - Open/Release: RG2(70,40,0.0,True,False,False)")
    
    while True:
        print("\n" + "="*60)
        print("Select a test:")
        print("  1. Basic open/close test")
        print("  2. Custom parameters test")
        print("  3. Pick & Place simulation")
        print("  4. Run all tests")
        print("  5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            test_basic_gripper()
        elif choice == '2':
            test_custom_parameters()
        elif choice == '3':
            test_pick_and_place_simulation()
        elif choice == '4':
            print("\n" + "="*60)
            print("Running All Tests")
            print("="*60)
            results = []
            results.append(("Basic Test", test_basic_gripper()))
            results.append(("Custom Parameters", test_custom_parameters()))
            results.append(("Pick & Place", test_pick_and_place_simulation()))
            
            print("\n" + "="*60)
            print("Test Results Summary")
            print("="*60)
            for name, result in results:
                status = "✓ PASSED" if result else "✗ FAILED"
                print(f"{name}: {status}")
            print("="*60)
        elif choice == '5':
            print("\nExiting...")
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
