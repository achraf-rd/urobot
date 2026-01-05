"""
RobotController Module - Handles robot operations using RoboDK API
"""

from robodk import robolink, robomath
from robodk.robolink import Robolink, Item
import time
from dashboard_gripper import DashboardGripper
from positions_manager import PositionsManager


class RobotController:
    """
    A controller class for managing robot operations through RoboDK API.
    
    This class provides high-level methods for common robot operations such as
    moving to home position, moving to specific poses, and pick-and-place operations.
    """
    
    def __init__(self, robot_name=None, robot_ip=None, use_gripper=True, speed=10, acceleration=10, connect_real_robot=False):
        """
        Initialize the RobotController.
        
        Args:
            robot_name (str, optional): Name of the robot in RoboDK. If None, uses the first available robot.
            robot_ip (str, optional): IP address of the UR robot for real connection.
            use_gripper (bool): Whether to use the gripper. Default is True.
            speed (int): Robot speed percentage (1-100).
            acceleration (int): Robot acceleration percentage (1-100).
            connect_real_robot (bool): If True, connect to real robot instead of simulation.
        """
        self.rdk = Robolink()
        
        # Connect to the robot
        if robot_name:
            self.robot = self.rdk.Item(robot_name, robolink.ITEM_TYPE_ROBOT)
        else:
            self.robot = self.rdk.Item('', robolink.ITEM_TYPE_ROBOT)
        
        if not self.robot.Valid():
            raise Exception("Robot not found. Please ensure RoboDK is running with a robot loaded.")
        
        print(f"Connected to robot: {self.robot.Name()}")
        
        # Initialize positions manager
        self.positions_manager = PositionsManager()
        
        # Connect to real robot if requested
        if connect_real_robot:
            print("\nSetting mode to RUN on REAL ROBOT...")
            print("Make sure you have already connected to the robot in RoboDK:")
            print("  Right-click robot → Connect to robot → Connect")
            
            # Check if robot is already connected in RoboDK
            connection_status = self.robot.ConnectedState()
            if connection_status == robolink.ROBOTCOM_READY:
                print("✓ Robot is already connected in RoboDK")
            elif connection_status == robolink.ROBOTCOM_WORKING:
                print("⚠ Robot is connected but busy")
            else:
                print(f"⚠ Robot connection status: {connection_status}")
                print("  Please connect manually in RoboDK first:")
                print("  Right-click robot → Connect to robot → Select driver → Connect")
            
            # Set RoboDK to run on real robot (not simulation)
            self.rdk.setRunMode(robolink.RUNMODE_RUN_ROBOT)
            print("✓ RoboDK set to RUN mode (real robot)")
        else:
            print("Running in SIMULATION mode")
            self.rdk.setRunMode(robolink.RUNMODE_SIMULATE)
        
        # Store home position (current position on initialization)
        self.home_joints = self.robot.Joints()
       
        self.set_speed(speed)
        self.set_acceleration(acceleration)
        
        # Initialize gripper if requested
        self.gripper = None
        self.robot_ip = robot_ip
        if use_gripper:
            try:
                self.gripper = DashboardGripper(robot_item=self.robot, robot_ip=robot_ip)
                if self.gripper.connect():
                    print("Gripper initialized successfully via RoboDK API")
                else:
                    print("Warning: Gripper connection failed, continuing without gripper")
                    self.gripper = None
            except Exception as e:
                print(f"Warning: Failed to initialize gripper: {e}")
                self.gripper = None
        else:
            print("Gripper disabled")
    
    def set_speed(self, speed_percent):
        """
        Set robot speed.
        
        Args:
            speed_percent: Speed as percentage (0-100)
        """
        if not 0 <= speed_percent <= 100:
            raise ValueError("Speed must be between 0 and 100")
        
        self.robot.setSpeed(speed_percent)
        print(f"Speed set to {speed_percent}%")
    
    def set_acceleration(self, accel_percent):
        """
        Set robot acceleration.
        
        Args:
            accel_percent: Acceleration as percentage (0-100)
        """
        if not 0 <= accel_percent <= 100:
            raise ValueError("Acceleration must be between 0 and 100")
        
        self.robot.setAcceleration(accel_percent)
        print(f"Acceleration set to {accel_percent}%")
    
    def set_rounding(self, radius_mm):
        """
        Set corner rounding radius.
        
        Args:
            radius_mm: Rounding radius in mm (0 = sharp corners)
        """
        self.robot.setRounding(radius_mm)
        print(f"Rounding set to {radius_mm}mm")
    
    def _reconnect_if_needed(self):
        """Check RoboDK connection and reconnect if needed after Dashboard commands."""
        try:
            state = self.robot.ConnectedState()
            
            if state != robolink.ROBOTCOM_READY:
                print(f"     RoboDK disconnected (state: {state}), reconnecting...")
                self.robot.Connect()
                time.sleep(2)
                
                new_state = self.robot.ConnectedState()
                if new_state == robolink.ROBOTCOM_READY:
                    print("     \u2713 RoboDK reconnected successfully")
                else:
                    print(f"     \u26a0 Connection state: {new_state}")
            else:
                print("     \u2713 RoboDK connection OK")
                
        except Exception as e:
            print(f"     \u26a0 Reconnection check: {e}")
            try:
                self.robot.Connect()
                time.sleep(2)
                print("     \u2713 RoboDK reconnected")
            except:
                print("     \u2717 Failed to reconnect")

    def move_to_home(self):
        """
        Move the robot to its home position from positions file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Get home position from positions file
            home_data = self.positions_manager.get_position('home pose')
            
            if home_data:
                # Use position from file
                position = home_data['position']
                orientation = home_data['orientation']
                pose = position + orientation
                target_pose = robomath.TxyzRxyz_2_Pose(pose)
                
                print(f"Moving to home position from file: {position}")
                self.robot.MoveJ(target_pose)
                self.robot.WaitMove()
                print("Reached home position.")
            else:
                # Fallback to stored joints if home not in file
                print("Home position not found in file, using stored joints...")
                self.robot.MoveJ(self.home_joints)
                self.robot.WaitMove()
                print("Reached home position.")
            
            return True
        except Exception as e:
            print(f"Error moving to home: {e}")
            return False
    
    def move_to_pose(self, pose):
        """
        Move the robot to a specific pose.
        
        Args:
            pose (list): Target pose as [x, y, z, rx, ry, rz] where:
                        - x, y, z are position coordinates in mm
                        - rx, ry, rz are orientation angles in degrees
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if len(pose) != 6:
                raise ValueError("Pose must contain 6 elements [x, y, z, rx, ry, rz]")
            
            # Create pose matrix from position and orientation
            target_pose = robomath.TxyzRxyz_2_Pose(pose)
            
            print(f"Moving to pose: {pose}")
            self.robot.MoveJ(target_pose)
            self.robot.WaitMove()
            print("Reached target pose.")
            return True
        except Exception as e:
            print(f"Error moving to pose: {e}")
            return False
    
    def pick_object(self, position, orientation, pick_offset_mm=30):
        """
        Execute a pick operation at the specified position and orientation.
        The received pose is the approach position (above the object).
        
        Sequence:
        1. Move to approach position
        2. Open gripper
        3. Move down by pick_offset_mm
        4. Close gripper
        5. Move back to approach position
        
        Args:
            position (list): [x, y, z] coordinates in mm (approach position)
            orientation (list): [rx, ry, rz] orientation angles in degrees
            pick_offset_mm (float): Distance to move down to grasp object (default: 40mm)
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if len(position) != 3 or len(orientation) != 3:
                raise ValueError("Position and orientation must contain 3 elements each")
            
            # Received pose is the approach position
            approach_pose = position + orientation
            approach_target = robomath.TxyzRxyz_2_Pose(approach_pose)
            
            # Calculate pick position (move down on Z)
            pick_pose = approach_pose.copy()
            pick_pose[2] -= pick_offset_mm  # Move down from approach
            pick_target = robomath.TxyzRxyz_2_Pose(pick_pose)
            
            print(f"Picking object at approach position: {position}")
            
            # Step 1: Move to approach position
            print("  → Moving to approach position...")
            self.robot.MoveJ(approach_target)
            self.robot.WaitMove()
            
            # Step 2: Open gripper
            print("  → Opening gripper...")
            self.gripper.open()
            # Wait for gripper program to complete
            print("  → Waiting for gripper to open...")
            self.gripper.wait_completion(timeout=10)
            # Ensure RoboDK reconnection after Dashboard command
            print("  → Verifying RoboDK connection...")
            self._reconnect_if_needed()
            time.sleep(1)  # Extra delay to ensure robot is ready
            
            # Step 3: Move down to pick position
            print(f"  → Moving down {pick_offset_mm}mm to grasp object...")
            self.robot.MoveL(pick_target)
            self.robot.WaitMove()
            
            # Step 4: Close gripper to grip object
            print("  → Closing gripper...")
            self.gripper.close()
            # Wait for gripper program to complete
            print("  → Waiting for gripper to close...")
            self.gripper.wait_completion(timeout=10)
            # Ensure RoboDK reconnection after Dashboard command
            print("  → Verifying RoboDK connection...")
            self._reconnect_if_needed()
            time.sleep(1)  # Extra delay to ensure robot is ready
            
            # Step 5: Move back to approach position
            print("  → Moving back to approach position...")
            self.robot.MoveL(approach_target)
            self.robot.WaitMove()
            
            print("✓ Pick operation completed.")
            return True
        except Exception as e:
            print(f"Error during pick operation: {e}")
            return False
    
    def place_object(self, position, orientation):
        """
        Execute a place operation at the specified position and orientation.
        
        Sequence:
        1. Move to place position
        2. Open gripper to release object
        
        Args:
            position (list): [x, y, z] coordinates in mm (place position)
            orientation (list): [rx, ry, rz] orientation angles in degrees
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if len(position) != 3 or len(orientation) != 3:
                raise ValueError("Position and orientation must contain 3 elements each")
            
            pose = position + orientation
            target_pose = robomath.TxyzRxyz_2_Pose(pose)
            
            print(f"Placing object at position: {position}")
            
            # Step 1: Move to place position
            print("  → Moving to place position...")
            self.robot.MoveJ(target_pose)
            self.robot.WaitMove()
            
            # Step 2: Open gripper to release object
            print("  → Opening gripper to release object...")
            self.gripper.open()
            # Wait for gripper program to complete
            print("  → Waiting for gripper to open...")
            self.gripper.wait_completion(timeout=10)
            # Ensure RoboDK reconnection after Dashboard command
            print("  → Verifying RoboDK connection...")
            self._reconnect_if_needed()
            time.sleep(1)  # Extra delay to ensure robot is ready
            
            print("✓ Place operation completed.")
            return True
        except Exception as e:
            print(f"Error during place operation: {e}")
            return False
    
    def wait(self, time_sec):
        """
        Wait for a specified amount of time.
        
        Args:
            time_sec (float): Time to wait in seconds.
        
        Returns:
            bool: True when wait is complete.
        """
        print(f"Waiting for {time_sec} seconds...")
        time.sleep(time_sec)
        print("Wait completed.")
        return True
    
    def _activate_gripper(self, close=True):
        """
        Activate or deactivate the gripper.
        
        Args:
            close (bool): True to close gripper, False to open.
        
        Note:
            Uses the OnRobot RG2 gripper if connected, otherwise simulates.
        """
        if self.gripper and self.gripper.is_connected():
            # Use real gripper
            if close:
                success = self.gripper.close()
                if success:
                    self.gripper.wait_for_completion()
            else:
                success = self.gripper.open()
                if success:
                    self.gripper.wait_for_completion()
        else:
            # Simulated gripper
            action = "Closing" if close else "Opening"
            print(f"{action} gripper (simulated)")
            time.sleep(0.5)
    
    def get_current_pose(self):
        """
        Get the current robot pose.
        
        Returns:
            list: Current pose as [x, y, z, rx, ry, rz]
        """
        pose_matrix = self.robot.Pose()
        pose = robomath.Pose_2_TxyzRxyz(pose_matrix)
        return pose
    
    def get_current_joints(self):
        """
        Get the current robot joint angles.
        
        Returns:
            list: Current joint angles in degrees.
        """
        return self.robot.Joints().list()
    
    def disconnect(self):
        """
        Disconnect from the robot and clean up resources.
        """
        print(f"Disconnecting from robot: {self.robot.Name()}")
        
        # Disconnect gripper if connected
        if self.gripper and self.gripper.is_connected():
            self.gripper.disconnect()
        
        # Connection is automatically closed when object is destroyed
        print("Disconnected successfully.")
    
    def gripper_open(self, width_mm=None, force_n=None):
        """
        Open the gripper to specified width.
        
        Args:
            width_mm (float, optional): Target width in mm
            force_n (float, optional): Force in N
        
        Returns:
            bool: True if successful
        """
        if self.gripper and self.gripper.is_connected():
            return self.gripper.open(width_mm, force_n)
        else:
            print("Opening gripper (simulated)")
            time.sleep(0.5)
            return True
    
    def gripper_close(self, width_mm=None, force_n=None):
        """
        Close the gripper to specified width.
        
        Args:
            width_mm (float, optional): Target width in mm
            force_n (float, optional): Gripping force in N
        
        Returns:
            bool: True if successful
        """
        if self.gripper and self.gripper.is_connected():
            return self.gripper.close(width_mm, force_n)
        else:
            print("Closing gripper (simulated)")
            time.sleep(0.5)
            return True
    
    def gripper_status(self):
        """
        Get gripper status.
        
        Returns:
            dict: Gripper status or None if not connected
        """
        if self.gripper and self.gripper.is_connected():
            return self.gripper.get_status()
        return None
    
    def is_object_gripped(self):
        """
        Check if an object is gripped.
        
        Returns:
            bool: True if object detected
        """
        if self.gripper and self.gripper.is_connected():
            return self.gripper.is_object_gripped()
        return False

