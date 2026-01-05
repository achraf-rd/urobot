"""
Dashboard Gripper Helper - Gripper control via Dashboard Server with RoboDK reconnection
"""
import time
import socket
from robodk import robolink

class DashboardGripper:
    """Gripper control using Dashboard Server TCP with RoboDK connection management."""
    
    def __init__(self, robot_item, robot_ip=None):
        """
        Initialize the gripper helper.
        
        Args:
            robot_item: RoboDK robot item object
            robot_ip (str): IP address of the UR robot (required for Dashboard Server)
        """
        self.robot = robot_item
        self.robot_ip = robot_ip if robot_ip else "192.168.1.10"
        self.dashboard_port = 29999
        self.connected = False
        self.socket_timeout = 5
    
    def connect(self):
        """Test connection to robot."""
        try:
            if self.robot and self.robot.Valid():
                self.connected = True
                return True
            return False
        except:
            return False
    
    def is_connected(self):
        """Check if connected."""
        return self.connected
    
    def disconnect(self):
        """Disconnect."""
        self.connected = False
    
    def _send_dashboard_command(self, command):
        """Send command to Dashboard Server via TCP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.socket_timeout)
            sock.connect((self.robot_ip, self.dashboard_port))
            
            # Receive welcome message
            sock.recv(1024)
            
            # Send command
            sock.send((command + "\n").encode('utf-8'))
            
            # Receive response
            response = sock.recv(1024).decode('utf-8').strip()
            
            sock.close()
            return response
            
        except socket.timeout:
            return "Error: Connection timeout"
        except Exception as e:
            return f"Error: {e}"
    
    def _check_and_reconnect_robodk(self):
        """Check RoboDK connection and reconnect if needed."""
        try:
            # Check connection state
            state = self.robot.ConnectedState()
            
            if state != robolink.ROBOTCOM_READY:
                print(f"  ⚠ RoboDK connection state: {state}, reconnecting...")
                self.robot.Connect()
                time.sleep(2)
                
                new_state = self.robot.ConnectedState()
                if new_state == robolink.ROBOTCOM_READY:
                    print("  ✓ RoboDK reconnected successfully")
                    return True
                else:
                    print(f"  ⚠ Reconnection state: {new_state}")
                    return False
            return True
            
        except Exception as e:
            print(f"  ⚠ Reconnection attempt: {e}")
            try:
                self.robot.Connect()
                time.sleep(2)
                print("  ✓ RoboDK reconnected")
                return True
            except:
                print("  ✗ Failed to reconnect")
                return False
    
    def open(self, program_name="open-gripper.urp"):
        """Open the gripper by loading and running a .urp program via Dashboard Server."""
        if not self.connected:
            print("ERROR: Not connected to robot")
            return False
        
        try:
            print(f"  → Loading program: {program_name}")
            
            # Send load command via Dashboard Server
            load_response = self._send_dashboard_command(f"load {program_name}")
            print(f"     Dashboard response: {load_response}")
            
            if "Error" in load_response or "File not found" in load_response:
                print(f"  ✗ Failed to load program: {load_response}")
                return False
            
            time.sleep(1)
            
            # Send play command via Dashboard Server
            print(f"  → Playing program: {program_name}")
            play_response = self._send_dashboard_command("play")
            print(f"     Dashboard response: {play_response}")
            
            # Reconnect RoboDK after Dashboard interaction
            print("  → Checking RoboDK connection...")
            self._check_and_reconnect_robodk()
            
            print(f"  ✓ Program {program_name} started")
            return True
            
        except Exception as e:
            print(f"  ✗ Error running program {program_name}: {e}")
            # Try to reconnect even on error
            self._check_and_reconnect_robodk()
            return False
    
    def close(self, program_name="close-gripper.urp"):
        """Close the gripper by loading and running a .urp program via Dashboard Server."""
        if not self.connected:
            print("ERROR: Not connected to robot")
            return False
        
        try:
            print(f"  → Loading program: {program_name}")
            
            # Send load command via Dashboard Server
            load_response = self._send_dashboard_command(f"load {program_name}")
            print(f"     Dashboard response: {load_response}")
            
            if "Error" in load_response or "File not found" in load_response:
                print(f"  ✗ Failed to load program: {load_response}")
                return False
            
            time.sleep(1)
            
            # Send play command via Dashboard Server
            print(f"  → Playing program: {program_name}")
            play_response = self._send_dashboard_command("play")
            print(f"     Dashboard response: {play_response}")
            
            # Reconnect RoboDK after Dashboard interaction
            print("  → Checking RoboDK connection...")
            self._check_and_reconnect_robodk()
            
            print(f"  ✓ Program {program_name} started")
            return True
            
        except Exception as e:
            print(f"  ✗ Error running program {program_name}: {e}")
            # Try to reconnect even on error
            self._check_and_reconnect_robodk()
            return False
    
    def wait_completion(self, timeout=30):
        """Wait for robot to finish current operation."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check if robot is busy
            if not self.robot.Busy():
                return True
            time.sleep(0.3)
        return False
