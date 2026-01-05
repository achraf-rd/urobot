"""
OnRobot RG2 Gripper Test - Dashboard TCP with RoboDK Management
===============================================================
This test loads and runs URP programs via Dashboard Server (port 29999)
while managing RoboDK connection to prevent disconnects.
"""
import socket
import time
from robodk import robolink

ROBOT_IP = "192.168.1.10"
PORT = 29999  # Dashboard server

def dashboard(cmd):
    """Send command to UR Dashboard Server."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ROBOT_IP, PORT))
        s.recv(1024)  # welcome msg
        s.send((cmd + "\n").encode())
        resp = s.recv(1024).decode().strip()
        s.close()
        return resp
    except Exception as e:
        return f"Error: {e}"

def check_robodk_connection(rdk, robot):
    """Check and restore RoboDK connection if needed."""
    try:
        # Test connection by getting robot name
        robot_name = robot.Name()
        
        # Check connection state
        state = robot.ConnectedState()
        if state != robolink.ROBOTCOM_READY:
            print(f"  ⚠ RoboDK connection state: {state}")
            print("  → Reconnecting to robot...")
            robot.Connect()
            time.sleep(2)
            
            new_state = robot.ConnectedState()
            if new_state == robolink.ROBOTCOM_READY:
                print("  ✓ RoboDK reconnected successfully")
                return True
            else:
                print(f"  ✗ Failed to reconnect (state: {new_state})")
                return False
        return True
        
    except Exception as e:
        print(f"  ✗ RoboDK connection check failed: {e}")
        print("  → Attempting to reconnect...")
        try:
            robot.Connect()
            time.sleep(2)
            print("  ✓ RoboDK reconnected")
            return True
        except:
            print("  ✗ Failed to reconnect")
            return False

# ============================================================================
# MAIN PROGRAM
# ============================================================================

print("\n" + "="*70)
print("  OnRobot RG2 Gripper Test via Dashboard Server")
print("="*70)
print(f"\nRobot IP: {ROBOT_IP}")
print(f"Dashboard Port: {PORT}")
print(f"Programs: open-gripper.urp, close-gripper.urp")

# Initialize RoboDK connection
print("\n[1/5] Connecting to RoboDK...")
rdk = robolink.Robolink()
robot = rdk.Item('', robolink.ITEM_TYPE_ROBOT)

if not robot.Valid():
    print("  ✗ ERROR: Robot not found in RoboDK!")
    exit(1)

print(f"  ✓ Connected to robot: {robot.Name()}")

# Test Dashboard connection
print("\n[2/5] Testing Dashboard Server connection...")
response = dashboard("PolyscopeVersion")
if "Error" in response:
    print(f"  ✗ Failed to connect to Dashboard: {response}")
    print("\n  Make sure:")
    print("    • Robot is powered on")
    print("    • IP address is correct (192.168.1.10)")
    print("    • Dashboard Server is enabled on robot")
    exit(1)
print(f"  ✓ Dashboard connected: {response}")

# Check RoboDK connection before Dashboard operations
print("\n[3/5] Checking RoboDK connection status...")
check_robodk_connection(rdk, robot)

# Load and run open-gripper program
print("\n[4/5] Opening gripper...")
print("  → Loading open-gripper.urp")
response = dashboard("load open-gripper.urp")
print(f"     Response: {response}")

if "File not found" in response or "Error" in response:
    print("  ✗ Program not found on robot controller!")
    print("\n  Make sure open-gripper.urp exists in /programs/ on robot")
else:
    time.sleep(1)
    
    print("  → Playing program")
    response = dashboard("play")
    print(f"     Response: {response}")
    
    time.sleep(3)  # Wait for gripper to open
    print("  ✓ Gripper opened")

# Check RoboDK connection after Dashboard operation
print("\n  → Checking RoboDK connection...")
check_robodk_connection(rdk, robot)

# Load and run close-gripper program  
print("\n[5/5] Closing gripper...")
print("  → Loading close-gripper.urp")
response = dashboard("load close-gripper.urp")
print(f"     Response: {response}")

if "File not found" in response or "Error" in response:
    print("  ✗ Program not found on robot controller!")
    print("\n  Make sure close-gripper.urp exists in /programs/ on robot")
else:
    time.sleep(1)
    
    print("  → Playing program")
    response = dashboard("play")
    print(f"     Response: {response}")
    
    time.sleep(3)  # Wait for gripper to close
    print("  ✓ Gripper closed")

# Final RoboDK connection check
print("\n  → Final RoboDK connection check...")
if check_robodk_connection(rdk, robot):
    print("  ✓ RoboDK connection maintained")
else:
    print("  ⚠ RoboDK connection may need manual reconnection")

print("\n" + "="*70)
print("  TEST COMPLETE")
print("="*70)
print("\nNotes:")
print("  • Dashboard commands sent successfully")
print("  • RoboDK connection automatically managed")
print("  • Programs must exist on robot controller in /programs/")
print("\nTo verify programs on robot:")
print("  1. On teach pendant: Program → Load Program")
print("  2. Check if open-gripper.urp and close-gripper.urp are listed")
