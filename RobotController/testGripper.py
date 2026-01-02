"""
RG2 Gripper Test - Direct URScript connection to UR robot
"""
import socket
import time

# ===== CONFIGURATION =====
ROBOT_IP = "192.168.1.10"   # CHANGE THIS to your robot's IP
PORT = 30002                # URScript port (default for UR robots)
TIMEOUT = 5                 # Connection timeout in seconds

def send_urscript(cmd, verbose=True):
    """
    Send URScript command directly to the robot.
    
    Args:
        cmd (str): URScript command to send
        verbose (bool): Print detailed info
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if verbose:
            print(f"  → Connecting to {ROBOT_IP}:{PORT}...")
        
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        
        # Connect to robot
        s.connect((ROBOT_IP, PORT))
        
        if verbose:
            print(f"  ✓ Connected!")
            print(f"  → Sending command: {cmd}")
        
        # Send command (must end with newline)
        s.send((cmd + "\n").encode('utf-8'))
        
        if verbose:
            print(f"  ✓ Command sent!")
        
        # Close connection
        s.close()
        
        return True
        
    except socket.timeout:
        print(f"  ✗ ERROR: Connection timeout!")
        print(f"     Robot at {ROBOT_IP}:{PORT} did not respond within {TIMEOUT} seconds")
        print(f"     Check if robot IP is correct and robot is powered on")
        return False
        
    except ConnectionRefusedError:
        print(f"  ✗ ERROR: Connection refused!")
        print(f"     Robot at {ROBOT_IP}:{PORT} refused the connection")
        print(f"     Possible reasons:")
        print(f"       - Robot IP is incorrect")
        print(f"       - Robot is not powered on")
        print(f"       - URScript port (30002) is not accessible")
        print(f"       - Robot firewall is blocking the connection")
        return False
        
    except socket.gaierror:
        print(f"  ✗ ERROR: Invalid IP address!")
        print(f"     Cannot resolve {ROBOT_IP}")
        print(f"     Please check the ROBOT_IP configuration")
        return False
        
    except OSError as e:
        print(f"  ✗ ERROR: Network error!")
        print(f"     {e}")
        print(f"     Check network connection between PC and robot")
        return False
        
    except Exception as e:
        print(f"  ✗ ERROR: Unexpected error!")
        print(f"     {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection():
    """Test if we can connect to the robot."""
    print("\n[TEST] Checking connection to robot...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((ROBOT_IP, PORT))
        s.close()
        print("  ✓ Connection successful!")
        return True
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")
        return False

# ===== MAIN TEST =====
if __name__ == "__main__":
    print("="*60)
    print("RG2 GRIPPER TEST - Direct URScript Connection")
    print("="*60)
    print(f"Robot IP: {ROBOT_IP}")
    print(f"Port: {PORT}")
    print("="*60)
    
    # Test connection first
    if not test_connection():
        print("\n" + "="*60)
        print("TROUBLESHOOTING:")
        print("="*60)
        print("1. Check robot IP address:")
        print(f"   Current: {ROBOT_IP}")
        print("   Update ROBOT_IP in this script if incorrect")
        print("")
        print("2. Check robot is powered on and in remote control mode")
        print("")
        print("3. Check network connection:")
        print("   - Can you ping the robot? Run: ping " + ROBOT_IP)
        print("   - Is robot on same network as this PC?")
        print("")
        print("4. Check URScript port is accessible:")
        print("   - Port 30002 should be open on the robot")
        print("="*60)
        exit(1)
    
    print("\n" + "="*60)
    print("GRIPPER TEST SEQUENCE")
    print("="*60)
    
    # Test 1: Open gripper
    print("\n[1/5] Opening gripper to 70mm...")
    if send_urscript("RG2(70,40,0.0,True,False,False)"):
        print("  ⏳ Waiting 3 seconds for gripper to move...")
        time.sleep(3)
        print("  ✓ Command completed")
    else:
        print("  ✗ Failed to send command")
        exit(1)
    
    # Test 2: Close gripper
    print("\n[2/5] Closing gripper to 60mm (normal grip)...")
    if send_urscript("RG2(60,40,0.0,True,False,False)"):
        print("  ⏳ Waiting 3 seconds for gripper to move...")
        time.sleep(3)
        print("  ✓ Command completed")
    else:
        print("  ✗ Failed to send command")
        exit(1)
    
    # Test 3: Open again
    print("\n[3/5] Opening gripper again...")
    if send_urscript("RG2(70,40,0.0,True,False,False)"):
        print("  ⏳ Waiting 3 seconds...")
        time.sleep(3)
        print("  ✓ Command completed")
    else:
        print("  ✗ Failed to send command")
        exit(1)
    
    # Test 4: Close tight
    print("\n[4/5] Closing gripper tight (40mm)...")
    if send_urscript("RG2(40,40,0.0,True,False,False)"):
        print("  ⏳ Waiting 3 seconds...")
        time.sleep(3)
        print("  ✓ Command completed")
    else:
        print("  ✗ Failed to send command")
        exit(1)
    
    # Test 5: Final open
    print("\n[5/5] Opening gripper final position...")
    if send_urscript("RG2(70,40,0.0,True,False,False)"):
        print("  ⏳ Waiting 3 seconds...")
        time.sleep(3)
        print("  ✓ Command completed")
    else:
        print("  ✗ Failed to send command")
        exit(1)
    
    print("\n" + "="*60)
    print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    # Ask user if gripper actually moved
    print("\nDid the gripper physically move? (y/n): ", end='')
    try:
        response = input().strip().lower()
        if response != 'y':
            print("\n" + "="*60)
            print("GRIPPER NOT MOVING - CHECK THESE:")
            print("="*60)
            print("1. RG2 URCaps Installation:")
            print("   - On UR teach pendant: Program → Installation")
            print("   - Check if OnRobot RG2 URCaps is installed")
            print("   - RG2() function must be available")
            print("")
            print("2. Gripper Physical Connection:")
            print("   - RG2 connected to robot tool flange connector?")
            print("   - Check cable connections")
            print("")
            print("3. Test from UR Pendant:")
            print("   - Try running: RG2(70,40,0.0,True,False,False)")
            print("   - If it doesn't work from pendant, URCaps issue")
            print("")
            print("4. Check Robot Mode:")
            print("   - Robot must be in remote control mode")
            print("   - Check safety configuration allows gripper control")
            print("="*60)
        else:
            print("\n✓ Great! Gripper is working correctly!")
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
