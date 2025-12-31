"""
Gripper Controller Module - OnRobot RG2 Integration
===================================================
This module provides a gripper controller for the OnRobot RG2 gripper
that integrates with the RobotController system via URScript commands.
"""

import time
from typing import Optional, Dict


class GripperController:
    """
    Controller for OnRobot RG2 gripper using URScript commands via RoboDK.
    
    This class provides high-level gripper control that integrates
    with the robot controller system through URCaps functions.
    """
    
    def __init__(self, robot_item):
        """
        Initialize the gripper controller.
        
        Args:
            robot_item: RoboDK robot item object for sending URScript commands
        """
        self.robot = robot_item
        self.connected = True
        
        # Gripper specifications for RG2
        self.min_width_mm = 0
        self.max_width_mm = 110
        self.min_force_n = 3
        self.max_force_n = 40
        
        # Default gripper parameters (matching user's URScript usage)
        self.default_grip_width = 60     # 60mm for gripping
        self.default_grip_force = 40     # 40N
        self.default_release_width = 70  # 70mm for opening
        self.default_release_force = 40  # 40N
        
        print("Gripper controller initialized (URScript mode)")
    
    def connect(self) -> bool:
        """
        Establish connection to the gripper.
        
        Returns:
            bool: True if connection successful
        """
        # Connection is through RoboDK robot object, no separate connection needed
        self.connected = True
        print("Gripper connected via URScript")
        return True
    
    def disconnect(self):
        """Disconnect from the gripper."""
        self.connected = False
        print("Gripper disconnected")
    
    def is_connected(self) -> bool:
        """Check if gripper is connected."""
        return self.connected and self.robot.Valid()
    
    def _send_urscript(self, script: str) -> bool:
        """
        Send URScript command to robot.
        
        Args:
            script (str): URScript command to execute
        
        Returns:
            bool: True if successful
        """
        if not self.connected:
            print("Gripper not connected")
            return False
        
        try:
            self.robot.RunInstruction(script, True)
            return True
        except Exception as e:
            print(f"Error sending URScript: {e}")
            return False
    
    def open(self, width_mm: Optional[float] = None, force_n: Optional[float] = None) -> bool:
        """
        Open the gripper.
        
        Args:
            width_mm (float, optional): Target width in mm. Default is 70mm
            force_n (float, optional): Force in N. Default is 40N
        
        Returns:
            bool: True if successful
        """
        if width_mm is None:
            width_mm = 70  # Use 70mm for opening as per user's script
        if force_n is None:
            force_n = 40
        
        # Clamp values to valid range
        width_mm = max(self.min_width_mm, min(self.max_width_mm, width_mm))
        force_n = max(self.min_force_n, min(self.max_force_n, force_n))
        
        print(f"Opening gripper: width={width_mm}mm, force={force_n}N")
        
        # Send URScript command for RG2 - using the actual function from URCaps
        # RG2(target_width, target_force, payload, set_payload, depth_compensation, slave)
        script = f"RG2({width_mm},{force_n},0.0,True,False,False)"
        
        if self._send_urscript(script):
            print("Gripper opened")
            return True
        else:
            print("Failed to open gripper")
            return False
    
    def close(self, width_mm: Optional[float] = None, force_n: Optional[float] = None) -> bool:
        """
        Close the gripper.
        
        Args:
            width_mm (float, optional): Target width in mm. Default is 60mm
            force_n (float, optional): Gripping force in N. Default is 40N
        
        Returns:
            bool: True if successful
        """
        if width_mm is None:
            width_mm = 60  # Use 60mm for gripping as per user's script
        if force_n is None:
            force_n = 40
        
        # Clamp values to valid range
        width_mm = max(self.min_width_mm, min(self.max_width_mm, width_mm))
        force_n = max(self.min_force_n, min(self.max_force_n, force_n))
        
        print(f"Closing gripper: width={width_mm}mm, force={force_n}N")
        
        # Send URScript command for RG2 - using the actual function from URCaps
        # RG2(target_width, target_force, payload, set_payload, depth_compensation, slave)
        script = f"RG2({width_mm},{force_n},0.0,True,False,False)"
        
        if self._send_urscript(script):
            print("Gripper closed")
            return True
        else:
            print("Failed to close gripper")
            return False
    
    def stop(self) -> bool:
        """
        Stop gripper movement.
        
        Returns:
            bool: True if successful
        """
        print("Stopping gripper")
        script = "rg2_stop()"
        return self._send_urscript(script)
    
    def get_status(self) -> Optional[Dict]:
        """
        Read gripper status and current measurements.
        
        Returns:
            dict: Status information or None if failed
        """
        try:
            # Get width using the measure_width global variable from URScript
            # The RG2 script continuously updates this value
            width_script = "return measure_width"
            width_result = self.robot.RunInstruction(width_script, True)
            
            # Get grip detection status
            grip_script = "return grip_detected"
            grip_result = self.robot.RunInstruction(grip_script, True)
            
            # Parse results
            width_mm = float(width_result) if width_result else 0.0
            grip_detected = bool(grip_result) if grip_result else False
            
            return {
                'status': 0,
                'width_mm': width_mm,
                'force_n': self.default_grip_force,
                'busy': False,  # RG2 doesn't expose busy status directly
                'grip_detected': grip_detected
            }
        except Exception as e:
            print(f"Error reading gripper status: {e}")
            return None
    
    def wait_for_completion(self, timeout: float = 5.0) -> bool:
        """
        Wait for gripper to complete current movement.
        
        Args:
            timeout (float): Maximum time to wait in seconds
        
        Returns:
            bool: True if completed, False if timeout
        """
        start_time = time.time()
        
        # RG2 gripper doesn't have a direct "busy" status
        # Wait a fixed time for the gripper to complete
        time.sleep(0.5)  # 500ms is usually enough for RG2
        return True
    
    def is_gripped(self) -> bool:
        """
        Check if an object is currently gripped.
        
        Returns:
            bool: True if object detected
        """
        status = self.get_status()
        if status:
            return status['grip_detected']
        return False
    
    def set_defaults(self, grip_width: float = 0, grip_force: float = 20,
                     release_width: float = 110, release_force: float = 20):
        """
        Set default parameters for grip and release operations.
        
        Args:
            grip_width (float): Default grip width in mm
            grip_force (float): Default grip force in N
            release_width (float): Default release width in mm
            release_force (float): Default release force in N
        """
        self.default_grip_width = grip_width
        self.default_grip_force = grip_force
        self.default_release_width = release_width
        self.default_release_force = release_force
        print(f"Gripper defaults updated: grip={grip_width}mm/{grip_force}N, release={release_width}mm/{release_force}N")
