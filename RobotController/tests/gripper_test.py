"""
OnRobot RG2 Gripper Test Script
================================
This script tests the OnRobot RG2 gripper communication and control.

The RG2 gripper typically communicates via:
1. Modbus TCP/RTU protocol
2. Digital I/O signals from the robot controller
3. URScript commands (for UR robots)

For UR5 robot, the gripper is usually controlled through:
- Tool digital outputs
- URScript functions
- Direct Modbus communication
"""

import socket
import time
import struct


class OnRobotRG2:
    """
    Controller for OnRobot RG2 gripper using Modbus TCP.
    
    The RG2 gripper uses Modbus TCP for communication. Default settings:
    - IP: Robot IP (gripper is connected through robot)
    - Port: 502 (Modbus TCP default)
    - Slave ID: 65 (default for OnRobot)
    """
    
    # Modbus Register Addresses for RG2
    REG_CONTROL = 0x0000      # Control register
    REG_TARGET_WIDTH = 0x0001 # Target gripper width (0.1mm units)
    REG_TARGET_FORCE = 0x0002 # Target force (0.1N units)
    REG_STATUS = 0x0003       # Status register
    REG_ACTUAL_WIDTH = 0x0004 # Current width (0.1mm units)
    REG_ACTUAL_FORCE = 0x0005 # Current force (0.1N units)
    
    # Control commands
    CMD_GRIP_INTERNAL = 0x0001  # Close gripper (internal grip)
    CMD_GRIP_EXTERNAL = 0x0002  # Open gripper (external grip)
    CMD_STOP = 0x0000           # Stop gripper
    
    def __init__(self, robot_ip='192.168.1.100', port=502, slave_id=65):
        """
        Initialize the RG2 gripper controller.
        
        Args:
            robot_ip (str): IP address of the UR robot (gripper connects through it)
            port (int): Modbus TCP port (default 502)
            slave_id (int): Modbus slave ID (default 65 for OnRobot)
        """
        self.robot_ip = robot_ip
        self.port = port
        self.slave_id = slave_id
        self.socket = None
        self.connected = False
        
        # Gripper specifications for RG2
        self.min_width = 0      # 0mm
        self.max_width = 1100   # 110mm (stored as 0.1mm units)
        self.min_force = 30     # 3N (stored as 0.1N units)
        self.max_force = 400    # 40N (stored as 0.1N units)
    
    def connect(self):
        """
        Establish connection to the gripper via Modbus TCP.
        
        Returns:
            bool: True if connection successful
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.robot_ip, self.port))
            self.connected = True
            print(f"✓ Connected to RG2 gripper at {self.robot_ip}:{self.port}")
            return True
        except socket.error as e:
            print(f"✗ Failed to connect to gripper: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the gripper."""
        if self.socket:
            self.socket.close()
            self.connected = False
            print("✓ Disconnected from gripper")
    
    def _build_modbus_write_request(self, register, value):
        """
        Build a Modbus TCP write single register request.
        
        Args:
            register (int): Register address
            value (int): Value to write
        
        Returns:
            bytes: Modbus TCP frame
        """
        # Modbus TCP header (MBAP Header)
        transaction_id = 0x0001
        protocol_id = 0x0000
        length = 6  # Bytes following
        
        # Modbus PDU for function code 0x06 (Write Single Register)
        function_code = 0x06
        
        frame = struct.pack(
            '>HHHBBHH',
            transaction_id,
            protocol_id,
            length,
            self.slave_id,
            function_code,
            register,
            value
        )
        return frame
    
    def _build_modbus_read_request(self, register, count=1):
        """
        Build a Modbus TCP read holding registers request.
        
        Args:
            register (int): Starting register address
            count (int): Number of registers to read
        
        Returns:
            bytes: Modbus TCP frame
        """
        transaction_id = 0x0001
        protocol_id = 0x0000
        length = 6
        function_code = 0x03
        
        frame = struct.pack(
            '>HHHBBHH',
            transaction_id,
            protocol_id,
            length,
            self.slave_id,
            function_code,
            register,
            count
        )
        return frame
    
    def _send_command(self, frame):
        """
        Send a Modbus command and receive response.
        
        Args:
            frame (bytes): Modbus TCP frame
        
        Returns:
            bytes: Response data or None if failed
        """
        if not self.connected:
            print("✗ Not connected to gripper")
            return None
        
        try:
            self.socket.send(frame)
            response = self.socket.recv(1024)
            return response
        except socket.error as e:
            print(f"✗ Communication error: {e}")
            return None
    
    def set_target_width(self, width_mm):
        """
        Set target gripper width.
        
        Args:
            width_mm (float): Target width in mm (0-110mm for RG2)
        
        Returns:
            bool: True if successful
        """
        # Clamp width to valid range
        width_mm = max(0, min(110, width_mm))
        
        # Convert to 0.1mm units
        width_units = int(width_mm * 10)
        
        print(f"Setting target width: {width_mm}mm ({width_units} units)")
        frame = self._build_modbus_write_request(self.REG_TARGET_WIDTH, width_units)
        response = self._send_command(frame)
        
        return response is not None
    
    def set_target_force(self, force_n):
        """
        Set target gripping force.
        
        Args:
            force_n (float): Target force in Newtons (3-40N for RG2)
        
        Returns:
            bool: True if successful
        """
        # Clamp force to valid range
        force_n = max(3, min(40, force_n))
        
        # Convert to 0.1N units
        force_units = int(force_n * 10)
        
        print(f"Setting target force: {force_n}N ({force_units} units)")
        frame = self._build_modbus_write_request(self.REG_TARGET_FORCE, force_units)
        response = self._send_command(frame)
        
        return response is not None
    
    def grip(self, width_mm=0, force_n=20):
        """
        Close the gripper (internal grip).
        
        Args:
            width_mm (float): Target width in mm (0 = fully closed)
            force_n (float): Gripping force in N (default 20N)
        
        Returns:
            bool: True if successful
        """
        print(f"🔒 Gripping: width={width_mm}mm, force={force_n}N")
        
        # Set target parameters
        self.set_target_width(width_mm)
        self.set_target_force(force_n)
        
        # Send grip command
        frame = self._build_modbus_write_request(self.REG_CONTROL, self.CMD_GRIP_INTERNAL)
        response = self._send_command(frame)
        
        if response:
            print("✓ Grip command sent")
            return True
        else:
            print("✗ Grip command failed")
            return False
    
    def release(self, width_mm=110, force_n=20):
        """
        Open the gripper (external grip/release).
        
        Args:
            width_mm (float): Target width in mm (110 = fully open)
            force_n (float): Force in N
        
        Returns:
            bool: True if successful
        """
        print(f"🔓 Releasing: width={width_mm}mm, force={force_n}N")
        
        # Set target parameters
        self.set_target_width(width_mm)
        self.set_target_force(force_n)
        
        # Send release command
        frame = self._build_modbus_write_request(self.REG_CONTROL, self.CMD_GRIP_EXTERNAL)
        response = self._send_command(frame)
        
        if response:
            print("✓ Release command sent")
            return True
        else:
            print("✗ Release command failed")
            return False
    
    def stop(self):
        """
        Stop gripper movement.
        
        Returns:
            bool: True if successful
        """
        print("⏹ Stopping gripper")
        frame = self._build_modbus_write_request(self.REG_CONTROL, self.CMD_STOP)
        response = self._send_command(frame)
        
        return response is not None
    
    def get_status(self):
        """
        Read gripper status and current measurements.
        
        Returns:
            dict: Status information including width and force
        """
        # Read status registers (status, width, force)
        frame = self._build_modbus_read_request(self.REG_STATUS, 3)
        response = self._send_command(frame)
        
        if response and len(response) >= 15:
            # Parse response (skip MBAP header and function code)
            status = struct.unpack('>H', response[9:11])[0]
            width = struct.unpack('>H', response[11:13])[0] / 10.0  # Convert to mm
            force = struct.unpack('>H', response[13:15])[0] / 10.0  # Convert to N
            
            return {
                'status': status,
                'width_mm': width,
                'force_n': force,
                'busy': bool(status & 0x0001),
                'grip_detected': bool(status & 0x0002)
            }
        
        return None
    
    def wait_for_completion(self, timeout=5.0):
        """
        Wait for gripper to complete current movement.
        
        Args:
            timeout (float): Maximum time to wait in seconds
        
        Returns:
            bool: True if completed, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_status()
            if status and not status['busy']:
                print("✓ Gripper movement completed")
                return True
            time.sleep(0.1)
        
        print("⚠ Gripper movement timeout")
        return False


def test_gripper_basic():
    """Test basic gripper operations."""
    print("\n" + "="*60)
    print("OnRobot RG2 Gripper - Basic Test")
    print("="*60 + "\n")
    
    # Configure your robot IP address here
    ROBOT_IP = input("Enter UR5 robot IP address (default: 192.168.1.100): ").strip()
    if not ROBOT_IP:
        ROBOT_IP = "192.168.1.100"
    
    print(f"\nConnecting to robot at {ROBOT_IP}...\n")
    
    # Create gripper instance
    gripper = OnRobotRG2(robot_ip=ROBOT_IP)
    
    # Connect
    if not gripper.connect():
        print("\n⚠ Connection failed! Please check:")
        print("  1. Robot is powered on")
        print("  2. Robot IP address is correct")
        print("  3. Gripper is properly connected to robot")
        print("  4. Network connection is working")
        return
    
    try:
        # Test 1: Get initial status
        print("\n--- Test 1: Read Initial Status ---")
        status = gripper.get_status()
        if status:
            print(f"Width: {status['width_mm']:.1f}mm")
            print(f"Force: {status['force_n']:.1f}N")
            print(f"Busy: {status['busy']}")
            print(f"Grip Detected: {status['grip_detected']}")
        
        input("\nPress Enter to test gripper opening...")
        
        # Test 2: Open gripper
        print("\n--- Test 2: Open Gripper ---")
        gripper.release(width_mm=110, force_n=20)
        gripper.wait_for_completion()
        time.sleep(1)
        
        status = gripper.get_status()
        if status:
            print(f"Current width: {status['width_mm']:.1f}mm")
        
        input("\nPress Enter to test gripper closing...")
        
        # Test 3: Close gripper
        print("\n--- Test 3: Close Gripper ---")
        gripper.grip(width_mm=0, force_n=20)
        gripper.wait_for_completion()
        time.sleep(1)
        
        status = gripper.get_status()
        if status:
            print(f"Current width: {status['width_mm']:.1f}mm")
            if status['grip_detected']:
                print("✓ Object detected!")
        
        input("\nPress Enter to test partial opening...")
        
        # Test 4: Partial open (50mm)
        print("\n--- Test 4: Partial Open (50mm) ---")
        gripper.release(width_mm=50, force_n=20)
        gripper.wait_for_completion()
        time.sleep(1)
        
        status = gripper.get_status()
        if status:
            print(f"Current width: {status['width_mm']:.1f}mm")
        
        input("\nPress Enter to test partial close (20mm)...")
        
        # Test 5: Partial close (20mm grip)
        print("\n--- Test 5: Partial Close (20mm) ---")
        gripper.grip(width_mm=20, force_n=15)
        gripper.wait_for_completion()
        time.sleep(1)
        
        status = gripper.get_status()
        if status:
            print(f"Current width: {status['width_mm']:.1f}mm")
        
        input("\nPress Enter to test different force levels...")
        
        # Test 6: Different force levels
        print("\n--- Test 6: Force Control Test ---")
        for force in [10, 20, 30]:
            print(f"\nGripping with {force}N force...")
            gripper.grip(width_mm=0, force_n=force)
            gripper.wait_for_completion()
            time.sleep(1)
            
            status = gripper.get_status()
            if status:
                print(f"  Current force: {status['force_n']:.1f}N")
        
        # Return to open position
        print("\n--- Returning to Open Position ---")
        gripper.release(width_mm=110, force_n=20)
        gripper.wait_for_completion()
        
        print("\n✓ All tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
    finally:
        # Always disconnect
        gripper.disconnect()
        print("\n" + "="*60)


def test_gripper_pick_place():
    """Test gripper in pick and place scenario."""
    print("\n" + "="*60)
    print("OnRobot RG2 Gripper - Pick & Place Test")
    print("="*60 + "\n")
    
    ROBOT_IP = input("Enter UR5 robot IP address (default: 192.168.1.100): ").strip()
    if not ROBOT_IP:
        ROBOT_IP = "192.168.1.100"
    
    gripper = OnRobotRG2(robot_ip=ROBOT_IP)
    
    if not gripper.connect():
        print("Connection failed!")
        return
    
    try:
        print("\n--- Pick & Place Simulation ---")
        print("(This tests gripper only, robot motion not included)")
        
        # Initial position - open
        print("\n1. Opening gripper to approach object...")
        gripper.release(width_mm=110, force_n=20)
        gripper.wait_for_completion()
        time.sleep(1)
        
        input("Press Enter to simulate picking object...")
        
        # Pick object
        print("\n2. Closing gripper to pick object...")
        gripper.grip(width_mm=30, force_n=25)  # Grip with 30mm width, 25N force
        gripper.wait_for_completion()
        time.sleep(1)
        
        status = gripper.get_status()
        if status and status['grip_detected']:
            print("✓ Object gripped successfully!")
        else:
            print("⚠ No object detected")
        
        print("\n3. Holding object for 3 seconds...")
        time.sleep(3)
        
        input("Press Enter to release object...")
        
        # Release object
        print("\n4. Opening gripper to release object...")
        gripper.release(width_mm=110, force_n=20)
        gripper.wait_for_completion()
        time.sleep(1)
        
        print("✓ Pick and place cycle completed!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        gripper.disconnect()
        print("\n" + "="*60)


def main():
    """Main test menu."""
    while True:
        print("\n" + "="*60)
        print("OnRobot RG2 Gripper Test Suite")
        print("="*60)
        print("\nSelect a test:")
        print("  1. Basic gripper operations test")
        print("  2. Pick & Place simulation test")
        print("  3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            test_gripper_basic()
        elif choice == '2':
            test_gripper_pick_place()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
