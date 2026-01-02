"""
Simple Gripper Test - Minimal test for OnRobot RG2 gripper
"""
from robodk import robolink
import time

print("Connecting to RoboDK...")
rdk = robolink.Robolink()

print("Getting robot...")
robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)

if not robot.Valid():
    print("ERROR: Robot not found!")
    print("Please make sure:")
    print("  1. RoboDK is running")
    print("  2. A UR robot is loaded in the workspace")
    exit(1)

print(f"✓ Connected to robot: {robot.Name()}")

# Ask about real robot
run_real = input("\nConnect to REAL robot? (y/n): ").strip().lower()

if run_real == 'y':
    print("\n⚠ REAL ROBOT MODE")
    print("Make sure:")
    print("  1. Robot is connected in RoboDK (right-click robot → Connect)")
    print("  2. Robot is in a safe position")
    input("Press ENTER to continue or Ctrl+C to cancel...")
    
    rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
    print("✓ Set to REAL ROBOT mode\n")
else:
    print("✓ Running in SIMULATION mode\n")
    rdk.setRunMode(robolink.RUNMODE_SIMULATE)

# Simple gripper test
print("="*60)
print("GRIPPER TEST")
print("="*60)

try:
    print("\n[1/3] Opening gripper (70mm)...")
    result = robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"      Response: {result}")
    print(f"      Type: {type(result)}")
    time.sleep(3)
    
    print("\n[2/3] Closing gripper (60mm)...")
    result = robot.RunInstruction("RG2(60,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"      Response: {result}")
    print(f"      Type: {type(result)}")
    time.sleep(3)
    
    print("\n[3/3] Opening gripper again (70mm)...")
    result = robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
    print(f"      Response: {result}")
    print(f"      Type: {type(result)}")
    time.sleep(3)
    
    # Get robot status
    print("\n[INFO] Checking robot status...")
    print(f"      Robot busy: {robot.Busy()}")
    print(f"      Connection status: {robot.ConnectedState()}")
    
    print("\n" + "="*60)
    print("✓ TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
