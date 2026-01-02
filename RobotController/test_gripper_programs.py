"""
Test RG2 Gripper - Load and run existing programs on robot
===========================================================
Tests the gripper by loading and running the open_gripper and close_gripper
programs that are already on the robot.
"""
import socket
import time

# Configuration
ROBOT_IP = "192.168.0.10"  # CHANGE THIS to your robot's IP
DASHBOARD_PORT = 29999

def dashboard_command(cmd):
    """
    Send a command to the Dashboard Server.
    
    Args:
        cmd (str): Dashboard command to send
    
    Returns:
        str: Response from the robot
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ROBOT_IP, DASHBOARD_PORT))
        
        # Receive welcome message
        welcome = s.recv(1024).decode('utf-8')
        
        # Send command
        s.send((cmd + "\n").encode('utf-8'))
        
        # Receive response
        response = s.recv(1024).decode('utf-8').strip()
        
        s.close()
        return response
        
    except socket.timeout:
        return f"ERROR: Timeout - Robot at {ROBOT_IP}:{DASHBOARD_PORT} not responding"
    except ConnectionRefusedError:
        return f"ERROR: Connection refused - Check robot IP and power"
    except Exception as e:
        return f"ERROR: {e}"

def check_program_state():
    """Get current program state."""
    return dashboard_command("programState")

def is_program_running():
    """Check if a program is currently running."""
    state = check_program_state()
    return "PLAYING" in state or "RUNNING" in state

def wait_for_program_completion(timeout=30):
    """Wait for program to finish."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_program_running():
            return True
        time.sleep(0.5)
    return False

# ===== MAIN TEST =====
print("="*60)
print("RG2 GRIPPER TEST - Program Control")
print("="*60)
print(f"Robot IP: {ROBOT_IP}")
print(f"Dashboard Port: {DASHBOARD_PORT}")
print("="*60)

# Test connection
print("\n[1] Testing connection to Dashboard Server...")
response = dashboard_command("robotmode")
if "ERROR" in response:
    print(f"  ✗ Failed to connect: {response}")
    print("\nTroubleshooting:")
    print(f"  - Check robot IP: {ROBOT_IP}")
    print("  - Ensure robot is powered on")
    print("  - Check network connection")
    exit(1)
else:
    print(f"  ✓ Connected! Robot mode: {response}")

# Check robot status
print("\n[2] Checking robot status...")
prog_state = check_program_state()
print(f"  Program state: {prog_state}")

# Test sequence
print("\n" + "="*60)
print("GRIPPER TEST SEQUENCE")
print("="*60)

# Test 1: Open gripper
print("\n[Test 1/5] Loading 'open_gripper.urp' program...")
response = dashboard_command("load open_gripper.urp")
print(f"  Response: {response}")

if "Loading" in response or "File opened" in response or "open_gripper" in response:
    print("  ✓ Program loaded successfully")
    
    time.sleep(1)
    
    print("  Starting program...")
    response = dashboard_command("play")
    print(f"  Response: {response}")
    
    if "Starting" in response:
        print("  ✓ Program started")
        print("  ⏳ Waiting for gripper to open...")
        if wait_for_program_completion():
            print("  ✓ Gripper opened!")
        else:
            print("  ⚠ Timeout waiting for completion")
    else:
        print(f"  ✗ Failed to start: {response}")
else:
    print(f"  ✗ Failed to load program: {response}")
    print("\n  Make sure 'open_gripper.urp' program exists on the robot")

time.sleep(2)

# Test 2: Close gripper
print("\n[Test 2/5] Loading 'close_gripper.urp' program...")
response = dashboard_command("load close_gripper.urp")
print(f"  Response: {response}")

if "Loading" in response or "File opened" in response or "close_gripper" in response:
    print("  ✓ Program loaded successfully")
    
    time.sleep(1)
    
    print("  Starting program...")
    response = dashboard_command("play")
    print(f"  Response: {response}")
    
    if "Starting" in response:
        print("  ✓ Program started")
        print("  ⏳ Waiting for gripper to close...")
        if wait_for_program_completion():
            print("  ✓ Gripper closed!")
        else:
            print("  ⚠ Timeout waiting for completion")
    else:
        print(f"  ✗ Failed to start: {response}")
else:
    print(f"  ✗ Failed to load program: {response}")
    print("\n  Make sure 'close_gripper.urp' program exists on the robot")

time.sleep(2)

# Test 3: Open again
print("\n[Test 3/5] Opening gripper again...")
response = dashboard_command("load open_gripper.urp")
time.sleep(1)
response = dashboard_command("play")
print(f"  Response: {response}")
if "Starting" in response:
    print("  ⏳ Waiting...")
    wait_for_program_completion()
    print("  ✓ Gripper opened!")

time.sleep(2)

# Test 4: Close again
print("\n[Test 4/5] Closing gripper again...")
response = dashboard_command("load close_gripper.urp")
time.sleep(1)
response = dashboard_command("play")
print(f"  Response: {response}")
if "Starting" in response:
    print("  ⏳ Waiting...")
    wait_for_program_completion()
    print("  ✓ Gripper closed!")

time.sleep(2)

# Test 5: Final open
print("\n[Test 5/5] Final open...")
response = dashboard_command("load open_gripper.urp")
time.sleep(1)
response = dashboard_command("play")
print(f"  Response: {response}")
if "Starting" in response:
    print("  ⏳ Waiting...")
    wait_for_program_completion()
    print("  ✓ Gripper opened!")

print("\n" + "="*60)
print("✓ ALL TESTS COMPLETED!")
print("="*60)

# Ask if gripper moved
print("\nDid the gripper physically move? (y/n): ", end='')
try:
    response = input().strip().lower()
    if response != 'y':
        print("\n" + "="*60)
        print("TROUBLESHOOTING - Gripper not moving:")
        print("="*60)
        print("1. Check program names on robot:")
        print("   - Programs must be named 'open_gripper.urp' and 'close_gripper.urp'")
        print("   - Check in robot teach pendant: Program tab")
        print("")
        print("2. Check programs contain RG2 commands:")
        print("   - open_gripper.urp should have: RG2(70,40,0.0,True,False,False)")
        print("   - close_gripper.urp should have: RG2(60,40,0.0,True,False,False)")
        print("")
        print("3. Check RG2 URCaps installation:")
        print("   - On teach pendant: Program → Installation")
        print("   - OnRobot RG2 must be installed and configured")
        print("")
        print("4. Test programs manually:")
        print("   - Load and run programs from teach pendant")
        print("   - If they don't work there, fix URCaps setup first")
        print("="*60)
    else:
        print("\n✓ Perfect! Gripper is working correctly!")
except KeyboardInterrupt:
    print("\n\nTest interrupted")
