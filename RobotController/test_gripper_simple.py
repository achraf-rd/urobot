"""
OnRobot RG2 Gripper Test - URCap Commands via RoboDK
====================================================
This test file controls the OnRobot RG2 gripper using URCap commands through RoboDK.

OnRobot RG2 URCap Command Format:
    RG2(target_width, force, payload, depth_compensation, slave)

Parameters:
    - target_width: Width in mm (0-110mm for RG2)
    - force: Gripping force 0-100 (40 is typical)
    - payload: Mass of payload in kg (0.0 for auto-detect)
    - depth_compensation: True/False (use True for better grip)
    - slave: True/False (False for single gripper)

Examples:
    RG2(110, 40, 0.0, True, False)  # Fully open
    RG2(0, 40, 0.0, True, False)    # Fully closed
    RG2(50, 60, 0.0, True, False)   # 50mm width, high force
"""
from robodk import robolink
import time


def test_onrobot_rg2_basic():
    """Test 1: Basic open and close operations."""
    print("\n" + "="*70)
    print("TEST 1: Basic Open/Close Operations")
    print("="*70)
    print("\nTesting basic OnRobot RG2 commands.")
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    print(f"✓ Connected to: {robot.Name()}")
    
    try:
        print("\n[1/3] Open RG2 gripper (110mm width)")
        cmd = "RG2(110, 40, 0.0, True, False)"
        print(f"  Command: {cmd}")
        robot.RunInstruction(cmd, robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Command sent")
        time.sleep(3)
        
        print("\n[2/3] Close RG2 gripper (0mm = fully closed)")
        cmd = "RG2(0, 40, 0.0, True, False)"
        print(f"  Command: {cmd}")
        robot.RunInstruction(cmd, robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Command sent")
        time.sleep(3)
        
        print("\n[3/3] Open RG2 again (110mm)")
        cmd = "RG2(110, 40, 0.0, True, False)"
        print(f"  Command: {cmd}")
        robot.RunInstruction(cmd, robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Command sent")
        time.sleep(3)
        
        print("\n✓ Basic operations complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_onrobot_rg2_widths():
    """Test 2: Different grip widths."""
    print("\n" + "="*70)
    print("TEST 2: Different Grip Widths")
    print("="*70)
    print("\nTesting various widths (0-110mm range).")
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    widths = [
        (110, "Fully open"),
        (80, "Wide grip"),
        (50, "Medium grip"),
        (20, "Narrow grip"),
        (0, "Fully closed"),
        (110, "Back to open"),
    ]
    
    try:
        for i, (width, description) in enumerate(widths, 1):
            print(f"\n[{i}/{len(widths)}] {description} ({width}mm)")
            cmd = f"RG2({width}, 40, 0.0, True, False)"
            print(f"  Command: {cmd}")
            robot.RunInstruction(cmd, robolink.INSTRUCTION_CALL_PROGRAM)
            print("  ✓ Command sent")
            time.sleep(2)
        
        print("\n✓ Width tests complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_onrobot_rg2_forces():
    """Test 3: Different grip forces."""
    print("\n" + "="*70)
    print("TEST 3: Different Grip Forces")
    print("="*70)
    print("\nTesting various force levels (0-100).")
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    forces = [
        (20, "Light force - delicate objects"),
        (40, "Medium force - standard grip"),
        (60, "Strong force - secure hold"),
        (80, "Very strong force - heavy objects"),
    ]
    
    try:
        # Open first
        print("\n[Setup] Opening gripper...")
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        time.sleep(2)
        
        for i, (force, description) in enumerate(forces, 1):
            print(f"\n[{i}/{len(forces)}] {description} (force={force})")
            cmd = f"RG2(50, {force}, 0.0, True, False)"
            print(f"  Command: {cmd}")
            robot.RunInstruction(cmd, robolink.INSTRUCTION_CALL_PROGRAM)
            print("  ✓ Command sent")
            time.sleep(3)
            
            # Open between tests
            if i < len(forces):
                robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
                time.sleep(2)
        
        print("\n✓ Force tests complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_onrobot_rg2_sequence():
    """Test 4: Complete pick and place sequence."""
    print("\n" + "="*70)
    print("TEST 4: Pick and Place Sequence")
    print("="*70)
    print("\nSimulating a complete pick and place operation.")
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    try:
        print("\n[1/6] Open gripper to approach object")
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Gripper open")
        time.sleep(2)
        
        print("\n[2/6] Close gripper to grip object (30mm width)")
        robot.RunInstruction("RG2(30, 60, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Object gripped")
        time.sleep(3)
        
        print("\n[3/6] Hold object during transport")
        print("  (Gripper maintains grip)")
        time.sleep(2)
        
        print("\n[4/6] Open gripper to release object")
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Object released")
        time.sleep(2)
        
        print("\n[5/6] Close gripper to neutral position (50mm)")
        robot.RunInstruction("RG2(50, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Neutral position")
        time.sleep(2)
        
        print("\n[6/6] Return to fully open")
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  ✓ Ready for next cycle")
        time.sleep(2)
        
        print("\n✓ Pick and place sequence complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Main test menu."""
    print("\n" + "="*70)
    print("  OnRobot RG2 Gripper Test - URCap Commands via RoboDK")
    print("="*70)
    print("\nOnRobot RG2 Command Format:")
    print("  RG2(width, force, payload, depth_comp, slave)")
    print("\nParameters:")
    print("  • width: 0-110mm (0=closed, 110=open)")
    print("  • force: 0-100 (40=standard, 60-80=strong)")
    print("  • payload: 0.0 for auto-detect")
    print("  • depth_comp: True (recommended)")
    print("  • slave: False (single gripper)")
    print("="*70)
    print("\nChoose test:\n")
    print("  1 - Basic Open/Close Test")
    print("  2 - Different Widths Test")
    print("  3 - Different Forces Test")
    print("  4 - Complete Pick & Place Sequence")
    print("  5 - Run ALL Tests")
    print("="*70)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    # Check connection mode
    rdk = robolink.Robolink()
    run_mode = input("\nRun on REAL robot? (y/n): ").strip().lower()
    
    if run_mode == 'y':
        print("\n⚠ REAL ROBOT MODE")
        print("IMPORTANT:")
        print("  1. Ensure OnRobot RG2 URCap is installed on robot")
        print("  2. Robot is connected in RoboDK (right-click → Connect)")
        print("  3. Gripper is properly mounted and powered")
        print("  4. Area around gripper is clear")
        input("\nPress ENTER to continue or Ctrl+C to cancel...")
        rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
        print("✓ Set to REAL ROBOT mode\n")
    else:
        print("✓ Running in SIMULATION mode")
        print("  (Commands will be sent but gripper won't move)\n")
        rdk.setRunMode(robolink.RUNMODE_SIMULATE)
    
    # Run selected test
    if choice == '1':
        test_onrobot_rg2_basic()
    elif choice == '2':
        test_onrobot_rg2_widths()
    elif choice == '3':
        test_onrobot_rg2_forces()
    elif choice == '4':
        test_onrobot_rg2_sequence()
    elif choice == '5':
        print("\nRunning ALL tests...")
        test_onrobot_rg2_basic()
        input("\nPress ENTER for next test...")
        test_onrobot_rg2_widths()
        input("\nPress ENTER for next test...")
        test_onrobot_rg2_forces()
        input("\nPress ENTER for next test...")
        test_onrobot_rg2_sequence()
    else:
        print("Invalid choice")
        return
    
    print("\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70)
    print("\nTroubleshooting:")
    print("  • If gripper didn't move: Check URCap installation")
    print("  • If error 'RG2 not found': Install OnRobot URCap on teach pendant")
    print("  • If movements are jerky: Adjust force parameter")
    print("\nNext tests:")
    print("  • test_gripper_programs.py - Load/run .urp programs")
    print("  • test_gripper_diagnostic.py - Direct TCP communication")


if __name__ == "__main__":
    main()
