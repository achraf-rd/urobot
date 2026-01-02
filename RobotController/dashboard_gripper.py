"""
Dashboard Gripper Helper - Gripper control via RoboDK API
"""
import time
from robodk import robolink

class DashboardGripper:
    """Simple gripper control using RoboDK API to load/run programs."""
    
    def __init__(self, robot_item, robot_ip=None):
        """
        Initialize the gripper helper.
        
        Args:
            robot_item: RoboDK robot item object
            robot_ip (str): IP address of the UR robot (kept for compatibility, not used)
        """
        self.robot = robot_item
        self.robot_ip = robot_ip
        self.connected = False
    
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
    
    def open(self, program_name="open-gripper.urp"):
        """Open the gripper by loading and running a .urp program on the robot."""
        if not self.connected:
            print("ERROR: Not connected to robot")
            return False
        
        try:
            print(f"Loading and running program: {program_name}")
            
            # Send Dashboard Server commands through RoboDK
            # Load the program from robot's /programs/ directory
            load_cmd = f"load /programs/{program_name}"
            self.robot.RunCodeCustom(load_cmd, True)
            time.sleep(0.5)
            
            # Start the program
            play_cmd = "play"
            self.robot.RunCodeCustom(play_cmd, True)
            
            print(f"Program {program_name} started")
            return True
            
        except Exception as e:
            print(f"Error running program {program_name}: {e}")
            return False
    
    def close(self, program_name="close-gripper.urp"):
        """Close the gripper by loading and running a .urp program on the robot."""
        if not self.connected:
            print("ERROR: Not connected to robot")
            return False
        
        try:
            print(f"Loading and running program: {program_name}")
            
            # Send Dashboard Server commands through RoboDK
            # Load the program from robot's /programs/ directory
            load_cmd = f"load /programs/{program_name}"
            self.robot.RunCodeCustom(load_cmd, True)
            time.sleep(0.5)
            
            # Start the program
            play_cmd = "play"
            self.robot.RunCodeCustom(play_cmd, True)
            
            print(f"Program {program_name} started")
            return True
            
        except Exception as e:
            print(f"Error running program {program_name}: {e}")
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
