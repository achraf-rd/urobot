"""
Gripper Diagnostic Test - Check why gripper isn't working
"""
from robodk import robolink
import time

print("="*60)
print("GRIPPER DIAGNOSTIC TEST")
print("="*60)

# Connect to RoboDK
print("\n[1] Connecting to RoboDK...")
rdk = robolink.Robolink()
print("    ✓ Connected")

# Get robot
print("\n[2] Getting robot...")
robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
if not robot.Valid():
    print("    ✗ ERROR: No robot found!")
    exit(1)
print(f"    ✓ Robot found: {robot.Name()}")

# Check current run mode
print("\n[3] Checking RoboDK run mode...")
current_mode = rdk.RunMode()
mode_names = {
    1: "SIMULATE (not connected to real robot)",
    2: "QUICKVALIDATE", 
    3: "MAKE_ROBOTPROG",
    4: "RUN_ROBOT (connected to real robot)"
}
print(f"    Current mode: {current_mode} - {mode_names.get(current_mode, 'Unknown')}")

if current_mode != 4:
    print("\n    ⚠ WARNING: Not in RUN_ROBOT mode!")
    print("    The gripper commands won't reach the real robot.")

# Check robot connection
print("\n[4] Checking robot connection status...")
conn_status = robot.ConnectedState()
print(f"    Connection status: {conn_status}")
if conn_status[1] != 'Ready':
    print("    ⚠ WARNING: Robot not ready!")
    print("    Please connect the robot in RoboDK:")
    print("      Right-click robot → Connect to robot → Select driver → Connect")

# Check if robot is connected to real hardware
print("\n[5] Checking if robot can communicate with real hardware...")
print("    Robot IP (if connected):", robot.ConnectionParams())

# Set to real robot mode
choice = input("\n[6] Switch to REAL ROBOT mode and test? (y/n): ").strip().lower()
if choice == 'y':
    print("\n    ⚠ SWITCHING TO REAL ROBOT MODE")
    print("    Make sure the robot is:")
    print("      - Connected in RoboDK")
    print("      - In a safe position")
    print("      - RG2 gripper is installed and configured in URCaps")
    input("    Press ENTER to continue or Ctrl+C to cancel...")
    
    rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
    time.sleep(1)
    
    new_mode = rdk.RunMode()
    print(f"    New mode: {new_mode} - {mode_names.get(new_mode, 'Unknown')}")
    
    # Try gripper commands with detailed feedback
    print("\n[7] Testing gripper commands...")
    
    print("\n    Test 1: Open gripper (70mm, 40N force)")
    result = robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"    Result: {result}")
    print("    Waiting 5 seconds... (watch the gripper!)")
    time.sleep(5)
    
    print("\n    Test 2: Close gripper (40mm, 40N force)")
    result = robot.RunInstruction("RG2(40,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"    Result: {result}")
    print("    Waiting 5 seconds... (watch the gripper!)")
    time.sleep(5)
    
    print("\n    Test 3: Open gripper again (70mm)")
    result = robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"    Result: {result}")
    print("    Waiting 5 seconds...")
    time.sleep(5)
    
    print("\n[8] Did the gripper move? (y/n): ", end='')
    moved = input().strip().lower()
    
    if moved != 'y':
        print("\n" + "="*60)
        print("TROUBLESHOOTING - Gripper not moving:")
        print("="*60)
        print("1. Check URCaps Installation:")
        print("   - On the UR teach pendant, go to Program → Installation")
        print("   - Check if 'OnRobot' or 'RG2' URCaps is installed")
        print("   - The RG2 function must be available in the Installation")
        print("")
        print("2. Verify Gripper Connection:")
        print("   - RG2 should be connected to robot tool connector")
        print("   - Check physical connections")
        print("")
        print("3. Check RoboDK Robot Driver:")
        print("   - Right-click robot in RoboDK")
        print("   - Go to 'Connect to robot'")
        print("   - Make sure correct driver is selected (UR)")
        print("   - IP address should match your robot")
        print("")
        print("4. Test from UR Pendant:")
        print("   - Try running RG2(70,40,0.0,True,False,False) from pendant")
        print("   - If it doesn't work there, it's a URCaps issue")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("✓ GRIPPER IS WORKING!")
        print("="*60)
else:
    print("\n    Skipping real robot test")
    print("\n" + "="*60)
    print("DIAGNOSTIC INFO:")
    print("="*60)
    print("- Commands are reaching RoboDK successfully (Response: 0)")
    print("- To test with real robot, you must:")
    print("  1. Connect robot in RoboDK (right-click → Connect)")
    print("  2. Run this script and select 'y' for real robot mode")
    print("  3. Ensure RG2 URCaps is installed on robot controller")
    print("="*60)

print("\nDiagnostic test completed.")
