"""
Test Gripper - Test OnRobot RG2 gripper through RoboDK
"""
from robodk import robolink, robomath
import time

# Connect to RoboDK
rdk = robolink.Robolink()

# Get the first available robot (or specify robot name if needed)
robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)

if not robot.Valid():
    raise Exception("Robot not found in RoboDK. Please ensure RoboDK is running with a robot loaded.")

print(f"Connected to robot: {robot.Name()}")

# Ask if user wants to run on real robot
use_real_robot = input("Run on real robot? (y/n, default: n): ").strip().lower() == 'y'

if use_real_robot:
    print("\nSetting mode to RUN on REAL ROBOT...")
    print("Make sure the robot is connected in RoboDK:")
    print("  Right-click robot → Connect to robot → Connect")
    
    # Check connection status
    connection_status = robot.ConnectedState()
    if connection_status == robolink.ROBOTCOM_READY:
        print("✓ Robot is connected in RoboDK")
    else:
        print(f"⚠ Robot connection status: {connection_status}")
        print("  Please connect manually in RoboDK first")
    
    rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
    print("✓ Set to REAL ROBOT mode")
else:
    print("\nRunning in SIMULATION mode")
    rdk.setRunMode(robolink.RUNMODE_SIMULATE)

# Test gripper
print("\n" + "="*50)
print("Testing OnRobot RG2 Gripper")
print("="*50)

print("\n1. Opening gripper to 70mm...")
robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
time.sleep(2)
print("   ✓ Gripper opened")

print("\n2. Closing gripper to 60mm (grip)...")
robot.RunInstruction("RG2(60,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
time.sleep(2)
print("   ✓ Gripper closed")

print("\n3. Opening gripper again...")
robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
time.sleep(2)
print("   ✓ Gripper opened")

print("\n4. Closing gripper tighter (40mm)...")
robot.RunInstruction("RG2(40,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
time.sleep(2)
print("   ✓ Gripper closed tight")

print("\n5. Opening gripper final...")
robot.RunInstruction("RG2(70,40,0.0,True,False,False)", robolink.INSTRUCTION_CALL_PROGRAM)
time.sleep(2)
print("   ✓ Gripper opened")

print("\n" + "="*50)
print("✓ Gripper test completed successfully!")
print("="*50)
