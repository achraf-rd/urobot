"""
Method 2: Load and Execute URP Programs on Robot Controller
============================================================
This method loads and runs .urp program files that are saved on the robot
controller or transfers them from RoboDK to the robot.

Three approaches:
1. Load existing .urp file from robot controller via TCP Dashboard
2. Generate and upload .urp program from RoboDK
3. Run program directly from RoboDK (transfers automatically)
"""
import socket
import time
from robodk import robolink
import os


# ============================================================================
# APPROACH 1: Dashboard Server - Load/Run Programs via TCP
# ============================================================================

class URDashboardClient:
    """Client for UR robot Dashboard Server (port 29999)."""
    
    def __init__(self, robot_ip, port=29999):
        """Initialize dashboard client."""
        self.robot_ip = robot_ip
        self.port = port
        self.timeout = 5
    
    def send_command(self, command):
        """Send command to Dashboard Server."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.robot_ip, self.port))
            
            # Receive welcome message
            welcome = sock.recv(1024).decode('utf-8')
            
            # Send command
            sock.send((command + "\n").encode('utf-8'))
            
            # Receive response
            response = sock.recv(1024).decode('utf-8').strip()
            
            sock.close()
            return response
            
        except socket.timeout:
            return f"ERROR: Timeout connecting to {self.robot_ip}:{self.port}"
        except ConnectionRefusedError:
            return f"ERROR: Connection refused - Check robot IP and power"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def load_program(self, program_path):
        """Load a .urp program file."""
        return self.send_command(f"load {program_path}")
    
    def play_program(self):
        """Start/play the loaded program."""
        return self.send_command("play")
    
    def stop_program(self):
        """Stop the running program."""
        return self.send_command("stop")
    
    def get_program_state(self):
        """Get current program state."""
        return self.send_command("programState")
    
    def get_loaded_program(self):
        """Get currently loaded program."""
        return self.send_command("get loaded program")


def test_dashboard_load_program():
    """Test loading and running program via Dashboard Server."""
    print("\n" + "="*70)
    print("APPROACH 1: Load/Run Program via TCP Dashboard Server")
    print("="*70)
    print("\nThis loads and runs a .urp program that exists on the robot.")
    print("Program must be located in: /programs/ on robot controller")
    
    robot_ip = input("\nEnter robot IP (default: 192.168.0.10): ").strip() or "192.168.0.10"
    dashboard = URDashboardClient(robot_ip)
    
    try:
        print(f"\n[Step 1] Connecting to robot at {robot_ip}...")
        mode = dashboard.send_command("robotmode")
        print(f"  Robot mode: {mode}")
        
        if "ERROR" in mode:
            print("  ✗ Cannot connect - check IP and power")
            return False
        
        print("\n[Step 2] Common gripper program names:")
        print("  • open_gripper.urp")
        print("  • close_gripper.urp")
        print("  • gripper_test.urp")
        
        program_name = input("\n  Enter program name: ").strip() or "open_gripper.urp"
        
        print(f"\n[Step 3] Loading program: {program_name}")
        result = dashboard.load_program(program_name)
        print(f"  Response: {result}")
        
        if "File not found" in result or "ERROR" in result:
            print(f"  ✗ Program not found on robot!")
            return False
        
        time.sleep(1)
        
        print("\n[Step 4] Starting program...")
        input("  Press ENTER to run (Ctrl+C to cancel)...")
        
        result = dashboard.play_program()
        print(f"  Response: {result}")
        
        print("\n[Step 5] Monitoring execution...")
        for i in range(10):
            state = dashboard.get_program_state()
            print(f"  State: {state}")
            if "STOPPED" in state:
                print("  ✓ Program finished!")
                break
            time.sleep(1)
        
        print("\n✓ Dashboard program test complete!")
        return True
        
    except KeyboardInterrupt:
        dashboard.stop_program()
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


# ============================================================================
# APPROACH 2: RoboDK - Generate and Upload Program
# ============================================================================

def test_robodk_generate_program():
    """Test generating URP program from RoboDK."""
    print("\n" + "="*70)
    print("APPROACH 2: Generate URP Program from RoboDK")
    print("="*70)
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    print(f"✓ Connected to: {robot.Name()}")
    
    try:
        print("\n[Step 1] Creating gripper program...")
        prog = rdk.AddProgram("gripper_test_generated")
        
        print("\n[Step 2] Adding gripper commands...")
        # Open gripper
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  Added: Open gripper")
        
        # Close gripper
        robot.RunInstruction("RG2(40, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        print("  Added: Close gripper")
        
        print("\n[Step 3] Generating .urp file...")
        urp_file = os.path.join(os.path.expanduser("~"), "Desktop", "gripper_test.urp")
        
        # Generate robot program
        robot.setParam("Driver", "UR5")
        status = robot.MakeProgram(urp_file)
        
        if os.path.exists(urp_file):
            print(f"  ✓ Program generated: {urp_file}")
        else:
            print("  ✗ Failed to generate program")
            return False
        
        print("\n✓ Program generation complete!")
        print(f"Upload '{os.path.basename(urp_file)}' to robot /programs/ folder")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


# ============================================================================
# APPROACH 3: RoboDK Direct Execution
# ============================================================================

def test_robodk_direct_execution():
    """Test running programs directly from RoboDK."""
    print("\n" + "="*70)
    print("APPROACH 3: RoboDK Direct Execution")
    print("="*70)
    print("\nRoboDK automatically transfers and executes on robot if connected.")
    
    rdk = robolink.Robolink()
    robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)
    
    if not robot.Valid():
        print("✗ ERROR: Robot not found!")
        return False
    
    print(f"✓ Connected to: {robot.Name()}")
    
    run_mode = input("\n  Connect to REAL robot? (y/n): ").strip().lower()
    
    if run_mode == 'y':
        print("  ⚠ REAL ROBOT MODE")
        input("  Press ENTER to continue...")
        rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
    else:
        print("  ✓ SIMULATION mode")
        rdk.setRunMode(robolink.RUNMODE_SIMULATE)
    
    try:
        print("\n[Test 1] Execute single commands...")
        print("  Opening gripper...")
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        time.sleep(2)
        
        print("  Closing gripper...")
        robot.RunInstruction("RG2(40, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        time.sleep(2)
        print("  ✓ Commands executed")
        
        print("\n[Test 2] Create and run program...")
        home_joints = robot.Joints().list()
        
        prog = rdk.AddProgram("gripper_sequence")
        robot.MoveJ(home_joints)
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        robot.RunInstruction("RG2(60, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        robot.RunInstruction("RG2(40, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        robot.RunInstruction("RG2(110, 40, 0.0, True, False)", robolink.INSTRUCTION_CALL_PROGRAM)
        
        print("  ✓ Program built")
        
        input("\n  Press ENTER to run program...")
        prog.RunProgram()
        print("  ✓ Program started")
        
        time.sleep(10)
        print("\n✓ Direct execution complete!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Main test menu."""
    print("\n" + "="*70)
    print("  GRIPPER METHOD 2: Load/Execute URP Programs")
    print("="*70)
    print("\nChoose approach:\n")
    print("  1 - Dashboard TCP: Load/run .urp from robot (requires existing program)")
    print("  2 - RoboDK Generate: Create and save .urp file")
    print("  3 - RoboDK Direct: Execute immediately (auto-transfer)")
    print("  4 - Run ALL tests")
    print("="*70)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        test_dashboard_load_program()
    elif choice == '2':
        test_robodk_generate_program()
    elif choice == '3':
        test_robodk_direct_execution()
    elif choice == '4':
        print("\nRunning ALL tests...")
        test_dashboard_load_program()
        input("\nPress ENTER for next test...")
        test_robodk_generate_program()
        input("\nPress ENTER for next test...")
        test_robodk_direct_execution()
    else:
        print("Invalid choice")
        return
    
    print("\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
