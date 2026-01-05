"""
Method 3: Direct TCP Communication to Robot
============================================
This method sends URScript commands directly to the robot via TCP socket
on port 30002 (real-time interface) or port 30001 (primary interface).

Approaches:
1. Primary Interface (port 30001) - Script execution
2. Real-time Interface (port 30002) - URScript commands
3. Dashboard Server (port 29999) - Robot control commands
"""
import socket
import time
import struct


# ============================================================================
# TCP Interface Classes
# ============================================================================

class URPrimaryInterface:
    """Primary interface for URScript execution (port 30001)."""
    
    def __init__(self, robot_ip, port=30001):
        """Initialize primary interface."""
        self.robot_ip = robot_ip
        self.port = port
        self.sock = None
    
    def connect(self):
        """Connect to robot."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.robot_ip, self.port))
            print(f"  ✓ Connected to {self.robot_ip}:{self.port}")
            return True
        except Exception as e:
            print(f"  ✗ Connection failed: {e}")
            return False
    
    def send_script(self, script):
        """Send URScript to robot."""
        try:
            if not self.sock:
                if not self.connect():
                    return False
            
            script_with_end = script + "\n"
            self.sock.send(script_with_end.encode('utf-8'))
            print(f"  ✓ Script sent: {script}")
            return True
        except Exception as e:
            print(f"  ✗ Error sending script: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from robot."""
        if self.sock:
            self.sock.close()
            self.sock = None


class URRealtimeInterface:
    """Real-time interface for URScript (port 30002)."""
    
    def __init__(self, robot_ip, port=30002):
        """Initialize real-time interface."""
        self.robot_ip = robot_ip
        self.port = port
        self.sock = None
    
    def connect(self):
        """Connect to robot."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.robot_ip, self.port))
            print(f"  ✓ Connected to {self.robot_ip}:{self.port}")
            return True
        except Exception as e:
            print(f"  ✗ Connection failed: {e}")
            return False
    
    def send_command(self, command):
        """Send real-time command to robot."""
        try:
            if not self.sock:
                if not self.connect():
                    return False
            
            command_with_end = command + "\n"
            self.sock.send(command_with_end.encode('utf-8'))
            print(f"  ✓ Command sent: {command}")
            return True
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from robot."""
        if self.sock:
            self.sock.close()
            self.sock = None


# ============================================================================
# Test Functions
# ============================================================================

def test_primary_interface():
    """Test gripper control via Primary Interface (port 30001)."""
    print("\n" + "="*70)
    print("APPROACH 1: Primary Interface (Port 30001)")
    print("="*70)
    print("\nThis sends URScript programs to the robot's primary interface.")
    print("Best for: Complex scripts, programs with logic")
    
    robot_ip = input("\nEnter robot IP (default: 192.168.0.10): ").strip() or "192.168.0.10"
    
    interface = URPrimaryInterface(robot_ip)
    
    try:
        print("\n[Step 1] Connecting to primary interface...")
        if not interface.connect():
            return False
        
        print("\n[Step 2] Testing gripper commands...")
        
        # Test 1: Digital output control
        print("\n  [Test 1] Digital output - Open gripper")
        script = "set_digital_out(0, True)"
        interface.send_script(script)
        time.sleep(2)
        
        print("\n  [Test 2] Digital output - Close gripper")
        script = "set_digital_out(0, False)"
        interface.send_script(script)
        time.sleep(2)
        
        # Test 3: OnRobot RG2 command
        print("\n  [Test 3] OnRobot RG2 - Open")
        script = "RG2(110, 40, 0.0, True, False)"
        interface.send_script(script)
        time.sleep(3)
        
        print("\n  [Test 4] OnRobot RG2 - Close")
        script = "RG2(40, 40, 0.0, True, False)"
        interface.send_script(script)
        time.sleep(3)
        
        # Test 5: Robotiq gripper
        print("\n  [Test 5] Robotiq - Open")
        script = "rq_open()"
        interface.send_script(script)
        time.sleep(2)
        
        print("\n  [Test 6] Robotiq - Close")
        script = "rq_close()"
        interface.send_script(script)
        time.sleep(2)
        
        print("\n✓ Primary interface tests complete!")
        interface.disconnect()
        return True
        
    except KeyboardInterrupt:
        print("\n  Test interrupted")
        interface.disconnect()
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        interface.disconnect()
        return False


def test_realtime_interface():
    """Test gripper control via Real-time Interface (port 30002)."""
    print("\n" + "="*70)
    print("APPROACH 2: Real-time Interface (Port 30002)")
    print("="*70)
    print("\nThis sends real-time URScript commands.")
    print("Best for: Quick commands, real-time control")
    
    robot_ip = input("\nEnter robot IP (default: 192.168.0.10): ").strip() or "192.168.0.10"
    
    interface = URRealtimeInterface(robot_ip)
    
    try:
        print("\n[Step 1] Connecting to real-time interface...")
        if not interface.connect():
            return False
        
        print("\n[Step 2] Testing gripper commands...")
        
        # Test sequence
        commands = [
            ("Open gripper (digital out)", "set_digital_out(0, True)"),
            ("Close gripper (digital out)", "set_digital_out(0, False)"),
            ("Open RG2", "RG2(110, 40, 0.0, True, False)"),
            ("Close RG2", "RG2(40, 40, 0.0, True, False)"),
            ("Partial close RG2", "RG2(60, 40, 0.0, True, False)"),
        ]
        
        for i, (desc, cmd) in enumerate(commands, 1):
            print(f"\n  [Test {i}] {desc}")
            interface.send_command(cmd)
            time.sleep(2)
        
        print("\n✓ Real-time interface tests complete!")
        interface.disconnect()
        return True
        
    except KeyboardInterrupt:
        print("\n  Test interrupted")
        interface.disconnect()
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        interface.disconnect()
        return False


def test_combined_script():
    """Test sending complete URScript program via TCP."""
    print("\n" + "="*70)
    print("APPROACH 3: Complete URScript Program")
    print("="*70)
    print("\nThis sends a complete multi-line URScript program.")
    
    robot_ip = input("\nEnter robot IP (default: 192.168.0.10): ").strip() or "192.168.0.10"
    
    interface = URPrimaryInterface(robot_ip)
    
    try:
        print("\n[Step 1] Connecting...")
        if not interface.connect():
            return False
        
        print("\n[Step 2] Creating gripper test program...")
        
        # Complete URScript program
        script = """def gripper_test():
  # Open gripper
  RG2(110, 40, 0.0, True, False)
  sleep(2.0)
  
  # Close gripper
  RG2(40, 40, 0.0, True, False)
  sleep(2.0)
  
  # Partial close
  RG2(60, 40, 0.0, True, False)
  sleep(2.0)
  
  # Open again
  RG2(110, 40, 0.0, True, False)
end

gripper_test()
"""
        
        print("  Program:")
        for line in script.split('\n')[:10]:
            print(f"    {line}")
        print("    ...")
        
        print("\n[Step 3] Sending program to robot...")
        input("  Press ENTER to execute (Ctrl+C to cancel)...")
        
        interface.send_script(script)
        
        print("\n  ✓ Program sent!")
        print("  ⏳ Executing (watch robot)...")
        time.sleep(10)
        
        print("\n✓ Program execution complete!")
        interface.disconnect()
        return True
        
    except KeyboardInterrupt:
        print("\n  Test cancelled")
        interface.disconnect()
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        interface.disconnect()
        return False


def test_diagnostic():
    """Run diagnostic on TCP connection."""
    print("\n" + "="*70)
    print("APPROACH 4: Connection Diagnostic")
    print("="*70)
    print("\nTest all TCP ports and connection methods.")
    
    robot_ip = input("\nEnter robot IP (default: 192.168.0.10): ").strip() or "192.168.0.10"
    
    ports_to_test = [
        (29999, "Dashboard Server"),
        (30001, "Primary Interface"),
        (30002, "Real-time Interface"),
        (30003, "Real-time Data"),
        (30004, "RTDE Interface"),
    ]
    
    print(f"\n[Testing connectivity to {robot_ip}]")
    
    for port, name in ports_to_test:
        print(f"\n  Port {port} ({name})...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((robot_ip, port))
            
            # Try to receive data
            try:
                data = sock.recv(1024, socket.MSG_DONTWAIT)
                print(f"    ✓ Connected - Received: {data[:50]}")
            except:
                print(f"    ✓ Connected (no immediate data)")
            
            sock.close()
            
        except socket.timeout:
            print(f"    ✗ Timeout")
        except ConnectionRefusedError:
            print(f"    ✗ Connection refused")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print("\n✓ Diagnostic complete!")
    return True


def main():
    """Main test menu."""
    print("\n" + "="*70)
    print("  GRIPPER METHOD 3: Direct TCP Communication")
    print("="*70)
    print("\nChoose approach:\n")
    print("  1 - Primary Interface (30001) - URScript programs")
    print("  2 - Real-time Interface (30002) - Quick commands")
    print("  3 - Complete Script - Multi-line program")
    print("  4 - Connection Diagnostic - Test all ports")
    print("  5 - Run ALL tests")
    print("="*70)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        test_primary_interface()
    elif choice == '2':
        test_realtime_interface()
    elif choice == '3':
        test_combined_script()
    elif choice == '4':
        test_diagnostic()
    elif choice == '5':
        print("\nRunning ALL tests...")
        test_diagnostic()
        input("\nPress ENTER for next test...")
        test_primary_interface()
        input("\nPress ENTER for next test...")
        test_realtime_interface()
        input("\nPress ENTER for next test...")
        test_combined_script()
    else:
        print("Invalid choice")
        return
    
    print("\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

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
