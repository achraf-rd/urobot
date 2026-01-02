"""
Client Example - Demonstrates how to send commands to the robot from a remote device

This script can be run from a Raspberry Pi or any other computer to control
the robot by sending commands over the network.
"""

import socket
import json
import time


class RobotClient:
    """
    Client class for sending commands to the RobotController server.
    """
    
    def __init__(self, host, port=5000):
        """
        Initialize the robot client.
        
        Args:
            host (str): IP address of the server running the robot controller.
            port (int): Port number (default: 5000).
        """
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Connect to the robot server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to robot server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the robot server."""
        if self.socket:
            self.socket.close()
            print("Disconnected from robot server")
    
    def send_command(self, command_dict):
        """
        Send a command to the robot and receive the response.
        
        Args:
            command_dict (dict): Command dictionary to send.
        
        Returns:
            dict: Response from the server, or None if error.
        """
        try:
            # Send command as JSON
            command_json = json.dumps(command_dict)
            self.socket.send(command_json.encode('utf-8'))
            
            # Receive response
            response = self.socket.recv(4096)
            response_dict = json.loads(response.decode('utf-8'))
            
            return response_dict
        except Exception as e:
            print(f"Error sending command: {e}")
            return None
    
    def move_home(self):
        """Move robot to home position."""
        command = {"command": "move_home"}
        return self.send_command(command)
    
    def move_to_pose(self, pose):
        """
        Move robot to specified pose.
        
        Args:
            pose (list): [x, y, z, rx, ry, rz]
        """
        command = {
            "command": "move_pose",
            "pose": pose
        }
        return self.send_command(command)
    
    def pick_object(self, position, orientation):
        """
        Pick object at specified position and orientation.
        
        Args:
            position (list): [x, y, z]
            orientation (list): [rx, ry, rz]
        """
        command = {
            "command": "pick",
            "position": position,
            "orientation": orientation
        }
        return self.send_command(command)
    
    def pick_piece(self, piece_name):
        """
        Pick a piece using predefined position from server.
        
        Args:
            piece_name (str): Name of piece (e.g., 'piece 1', 'piece 2')
        
        Returns:
            dict: Response from server
        """
        command = {
            "command": "pick_piece",
            "piece": piece_name
        }
        return self.send_command(command)
    
    def place_object(self, position, orientation):
        """
        Place object at specified position and orientation.
        
        Args:
            position (list): [x, y, z]
            orientation (list): [rx, ry, rz]
        """
        command = {
            "command": "place",
            "position": position,
            "orientation": orientation
        }
        return self.send_command(command)
    
    def place_piece(self, location_name):
        """
        Place a piece at predefined location from server.
        
        Args:
            location_name (str): Name of location (e.g., 'bad bin', 'good bin')
        
        Returns:
            dict: Response from server
        """
        command = {
            "command": "place_piece",
            "location": location_name
        }
        return self.send_command(command)
    
    def wait(self, duration):
        """
        Wait for specified duration.
        
        Args:
            duration (float): Wait time in seconds.
        """
        command = {
            "command": "wait",
            "duration": duration
        }
        return self.send_command(command)
    
    def list_positions(self):
        """
        Get list of all available predefined positions on server.
        
        Returns:
            dict: Response with list of position names
        """
        command = {"command": "list_positions"}
        return self.send_command(command)
    
    def get_pose(self):
        """Get current robot pose."""
        command = {"command": "get_pose"}
        return self.send_command(command)
    
    def get_joints(self):
        """Get current robot joint angles."""
        command = {"command": "get_joints"}
        return self.send_command(command)


def example_pick_and_place():
    """
    Example: Pick and place operation using predefined positions.
    """
    # Replace with your server's IP address
    SERVER_IP = "192.168.137.1"  # Change this to your server's IP
    
    # Create client and connect
    client = RobotClient(SERVER_IP)
    
    if not client.connect():
        print("Failed to connect to server. Make sure:")
        print("1. The server is running (python main.py)")
        print(f"2. The IP address {SERVER_IP} is correct")
        print("3. Port 5000 is not blocked by firewall")
        return
    
    try:
        # List available positions
        print("\n1. Getting available positions...")
        response = client.list_positions()
        print(f"Response: {response}")
        if response.get('status') == 'success':
            print(f"Available positions: {response.get('positions')}")
        
        # Pick piece 1
        print("\n2. Picking piece 1...")
        response = client.pick_piece('piece 1')
        print(f"Response: {response}")
        
        if response.get('status') != 'success':
            print("Failed to pick piece!")
            return
        
        # Wait a bit
        print("\n3. Waiting 1 second...")
        client.wait(1.0)
        
        # Place in bad bin
        print("\n4. Placing in bad bin...")
        response = client.place_piece('bad bin')
        print(f"Response: {response}")
        
        if response.get('status') != 'success':
            print("Failed to place piece!")
            return
        
        print("\n✓ Pick and place sequence completed successfully!")
        
    except Exception as e:
        print(f"\nError during operation: {e}")
    
    finally:
        # Always disconnect
        client.disconnect()


def example_pick_and_place_old():
    """
    Example: Pick and place operation.
    """
    # Replace with your server's IP address
    SERVER_IP = "192.168.137.1"  # Change this to your server's IP
    
    # Create client and connect
    client = RobotClient(SERVER_IP)
    
    if not client.connect():
        print("Failed to connect to server. Make sure:")
        print("1. The server is running (python main.py)")
        print(f"2. The IP address {SERVER_IP} is correct")
        print("3. Port 5000 is not blocked by firewall")
        return
    
    try:
        # Get current pose
        print("\n1. Getting current pose...")
        response = client.get_pose()
        print(f"Response: {response}")
        
        # Move to home position
        print("\n2. Moving to home position...")
        response = client.move_home()
        print(f"Response: {response}")
        
        # Wait a bit
        print("\n3. Waiting 1 second...")
        response = client.wait(1.0)
        print(f"Response: {response}")
        
        # Pick object
        print("\n4. Picking object...")
        pick_position = [300, 200, 150]
        pick_orientation = [0, 90, 0]
        response = client.pick_object(pick_position, pick_orientation)
        print(f"Response: {response}")
        
        # Wait a bit
        print("\n5. Waiting 1 second...")
        response = client.wait(1.0)
        print(f"Response: {response}")
        
        # Place object
        print("\n6. Placing object...")
        place_position = [400, 200, 150]
        place_orientation = [0, 90, 0]
        response = client.place_object(place_position, place_orientation)
        print(f"Response: {response}")
        
        # Move back to home
        print("\n7. Returning to home...")
        response = client.move_home()
        print(f"Response: {response}")
        
        print("\n✓ Pick and place sequence completed successfully!")
        
    except Exception as e:
        print(f"\nError during operation: {e}")
    
    finally:
        # Always disconnect
        client.disconnect()


def test_place_by_name():
    """
    Test placing at named locations (bad bin, good bin).
    """
    print("\n" + "="*60)
    print("Test: Place at Named Locations")
    print("="*60)
    
    # Get server IP
    SERVER_IP = input("Enter server IP address (default: 192.168.137.1): ") or "192.168.137.1"
    
    # Create client and connect
    client = RobotClient(SERVER_IP)
    
    if not client.connect():
        print("Failed to connect to server!")
        return
    
    try:
        # List available positions first
        print("\n1. Getting available positions...")
        response = client.list_positions()
        if response.get('status') == 'success':
            positions = response.get('positions', [])
            print(f"   Available positions: {positions}")
            
            # Filter for bin locations
            bins = [p for p in positions if 'bin' in p.lower()]
            print(f"   Available bins: {bins}")
        
        # Test placing at bad bin
        print("\n2. Testing place at 'bad bin'...")
        response = client.place_piece('bad bin')
        print(f"   Response: {response}")
        
        if response.get('status') == 'success':
            print("   ✓ Successfully placed at bad bin!")
            print(f"   Position used: {response.get('position')}")
            print(f"   Orientation used: {response.get('orientation')}")
        else:
            print(f"   ✗ Failed: {response.get('message')}")
        
        # Wait between movements
        print("\n3. Waiting 2 seconds...")
        client.wait(2.0)
        
        # Test placing at good bin
        print("\n4. Testing place at 'good bin'...")
        response = client.place_piece('good bin')
        print(f"   Response: {response}")
        
        if response.get('status') == 'success':
            print("   ✓ Successfully placed at good bin!")
            print(f"   Position used: {response.get('position')}")
            print(f"   Orientation used: {response.get('orientation')}")
        else:
            print(f"   ✗ Failed: {response.get('message')}")
        
        print("\n✓ Place test completed!")
        
    except Exception as e:
        print(f"\nError during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.disconnect()


def example_pick_and_place_old_manual():
    """
    Example: Pick and place operation.
    """
    # Replace with your server's IP address
    SERVER_IP = "0.0.0.0"  # Change this to your server's IP
    
    # Create client and connect
    client = RobotClient(SERVER_IP)
    
    if not client.connect():
        print("Failed to connect to server. Make sure:")
        print("1. The server is running (python main.py)")
        print(f"2. The IP address {SERVER_IP} is correct")
        print("3. Port 5000 is not blocked by firewall")
        return
    
    try:
        # Get current pose
        print("\n1. Getting current pose...")
        response = client.get_pose()
        print(f"Response: {response}")
        
        # Move to home position
        print("\n2. Moving to home position...")
        response = client.move_home()
        print(f"Response: {response}")
        
        # Wait a bit
        print("\n3. Waiting 1 second...")
        response = client.wait(1.0)
        print(f"Response: {response}")
        
        # Pick object
        print("\n4. Picking object...")
        pick_position = [300, 200, 150]
        pick_orientation = [0, 90, 0]
        response = client.pick_object(pick_position, pick_orientation)
        print(f"Response: {response}")
        
        # Wait a bit
        print("\n5. Waiting 1 second...")
        response = client.wait(1.0)
        print(f"Response: {response}")
        
        # Place object
        print("\n6. Placing object...")
        place_position = [400, 200, 150]
        place_orientation = [0, 90, 0]
        response = client.place_object(place_position, place_orientation)
        print(f"Response: {response}")
        
        # Move back to home
        print("\n7. Returning to home...")
        response = client.move_home()
        print(f"Response: {response}")
        
        print("\n✓ Pick and place sequence completed successfully!")
        
    except Exception as e:
        print(f"\nError during operation: {e}")
    
    finally:
        # Always disconnect
        client.disconnect()


def interactive_mode():
    """
    Interactive mode for manually sending commands.
    """
    SERVER_IP = input("Enter server IP address (default: 192.168.1.100): ") or "192.168.1.100"
    
    client = RobotClient(SERVER_IP)
    
    if not client.connect():
        return
    
    print("\nInteractive Robot Control Mode")
    print("=" * 50)
    print("Commands:")
    print("  1 - Move to home")
    print("  2 - Pick object")
    print("  3 - Place object")
    print("  4 - Get current pose")
    print("  5 - Get joint angles")
    print("  q - Quit")
    print("=" * 50)
    
    try:
        while True:
            choice = input("\nEnter command: ").strip()
            
            if choice == 'q':
                break
            elif choice == '1':
                response = client.move_home()
                print(f"Response: {response}")
            elif choice == '2':
                # Enter values like: 5.667981, 7.786667, 170.027672, -126.455691, 126.455690, -1.803552
                values = input("Enter position and orientation [x, y, z, rx, ry, rz]: ").strip()
                values = [float(v.strip()) for v in values.replace('[', '').replace(']', '').split(',')]
                x, y, z, rx, ry, rz = values
                print(f"Picking at position: {[x, y, z]} with orientation: {[rx, ry, rz]}")
                response = client.pick_object([x, y, z], [rx, ry, rz])
                print(f"Response: {response}")
            elif choice == '3':
                x = float(input("Enter X position (mm): "))
                y = float(input("Enter Y position (mm): "))
                z = float(input("Enter Z position (mm): "))
                rx = float(input("Enter RX orientation (deg): "))
                ry = float(input("Enter RY orientation (deg): "))
                rz = float(input("Enter RZ orientation (deg): "))
                response = client.place_object([x, y, z], [rx, ry, rz])
                print(f"Response: {response}")
            elif choice == '4':
                response = client.get_pose()
                print(f"Response: {response}")
            elif choice == '5':
                response = client.get_joints()
                print(f"Response: {response}")
            else:
                print("Invalid command")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        client.disconnect()


if __name__ == "__main__":
    import sys
    
    print("Robot Client Example")
    print("=" * 50)
    print("1 - Run pick and place example (with named positions)")
    print("2 - Test place by location name")
    print("3 - Interactive mode")
    print("=" * 50)
    
    choice = input("Select mode (1, 2, or 3): ").strip()
    
    if choice == '1':
        example_pick_and_place()
    elif choice == '2':
        test_place_by_name()
    elif choice == '3':
        interactive_mode()
    else:
        print("Invalid choice")
