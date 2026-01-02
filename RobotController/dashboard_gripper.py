"""
Dashboard Gripper Helper - Simple gripper control via Dashboard Server
"""
import socket
import time

class DashboardGripper:
    """Simple gripper control using Dashboard Server to load/run programs."""
    
    def __init__(self, robot_ip, dashboard_port=29999):
        """
        Initialize the gripper helper.
        
        Args:
            robot_ip (str): IP address of the UR robot
            dashboard_port (int): Dashboard server port (default: 29999)
        """
        self.robot_ip = robot_ip
        self.dashboard_port = dashboard_port
        self.timeout = 5
        self.connected = False
    
    def _send_command(self, cmd):
        """Send a command to the Dashboard Server."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.robot_ip, self.dashboard_port))
            
            # Receive welcome message
            s.recv(1024)
            
            # Send command
            s.send((cmd + "\n").encode('utf-8'))
            
            # Receive response
            response = s.recv(1024).decode('utf-8').strip()
            
            s.close()
            return response
            
        except Exception as e:
            print(f"Dashboard command error: {e}")
            return f"ERROR: {e}"
    
    def connect(self):
        """Test connection to Dashboard Server."""
        try:
            response = self._send_command("robotmode")
            if "ERROR" not in response:
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
    
    def open(self, program_name="open-gripper.urp"):
        """Open the gripper by loading and running a program."""
        if not self.connected:
            print("ERROR: Not connected to Dashboard Server")
            return False
        
        # Load program
        print(f"Loading program: {program_name}")
        response = self._send_command(f"load {program_name}")
        print(f"Load response: {response}")
        
        if "ERROR" in response and "Loading" not in response and "File opened" not in response:
            print(f"Failed to load {program_name}: {response}")
            return False
        
        time.sleep(1)
        
        # Play program
        print("Starting program...")
        response = self._send_command("play")
        print(f"Play response: {response}")
        
        if "Starting" in response or "STARTING" in response:
            return True
        else:
            print(f"Failed to start program: {response}")
            return False
    
    def close(self, program_name="close-gripper.urp"):
        """Close the gripper by loading and running a program."""
        if not self.connected:
            print("ERROR: Not connected to Dashboard Server")
            return False
        
        # Load program
        print(f"Loading program: {program_name}")
        response = self._send_command(f"load {program_name}")
        print(f"Load response: {response}")
        
        if "ERROR" in response and "Loading" not in response and "File opened" not in response:
            print(f"Failed to load {program_name}: {response}")
            return False
        
        time.sleep(1)
        
        # Play program
        print("Starting program...")
        response = self._send_command("play")
        print(f"Play response: {response}")
        
        if "Starting" in response or "STARTING" in response:
            return True
        else:
            print(f"Failed to start program: {response}")
            return False
    
    def wait_completion(self, timeout=30):
        """Wait for program to complete."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            state = self._send_command("programState")
            if "STOPPED" in state or "PAUSED" in state:
                return True
            time.sleep(0.3)
        return False
