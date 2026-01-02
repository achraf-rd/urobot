"""
Main Module - Example usage of RobotController with CommandServer

This script demonstrates how to:
1. Initialize the RobotController
2. Start the command server
3. Handle incoming commands from network clients
"""

import sys
import signal
from robot_controller import RobotController
from command_server import CommandServer


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nShutting down gracefully...")
    sys.exit(0)


def main():
    """
    Main function demonstrating the robot control system.
    
    This function:
    - Connects to the robot through RoboDK
    - Starts a TCP server on port 5000
    - Listens for commands from remote clients (e.g., Raspberry Pi)
    """
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # ====================================
        # Step 1: Initialize RobotController
        # ====================================
        print("=" * 60)
        print("Initializing Robot Controller")
        print("=" * 60)
        
        # Prompt for robot mode
        mode = input("\nConnect to REAL robot or SIMULATION? (r/s, default: s): ").strip().lower()
        connect_real = (mode == 'r')
        
        robot_ip = None
        if connect_real:
            print("\nIMPORTANT: Make sure you have connected to the robot in RoboDK first!")
            print("  1. Right-click on the robot in RoboDK")
            print("  2. Select 'Connect to robot...'")
            print("  3. Choose 'Universal Robots' driver")
            print("  4. Enter robot IP and click 'Connect'")
            
            # Ask for robot IP for gripper control
            robot_ip = input("\nEnter robot IP address (e.g., 192.168.0.10): ").strip()
            if not robot_ip:
                print("Warning: No robot IP provided, gripper will not be available")
                robot_ip = None
            
            input("\nPress Enter once robot is connected in RoboDK...")
        
        # Initialize the robot controller with gripper enabled by default
        robot = RobotController(
            robot_ip=robot_ip,
            use_gripper=True,
            connect_real_robot=connect_real
        )
        
        print("\nRobot initialized successfully!")
        print(f"Current position: {robot.get_current_pose()}")
        print(f"Current joints: {robot.get_current_joints()}")
        
        # ====================================
        # Step 2: Create Command Server
        # ====================================
        print("\n" + "=" * 60)
        print("Setting up Command Server")
        print("=" * 60)
        
        # Create command server that listens on all interfaces, port 5000
        server = CommandServer(
            host='0.0.0.0',  # Listen on all network interfaces
            port=5000,       # TCP port
            robot_controller=robot
        )
        
        print("\nCommand server configured.")
        print("The server will accept JSON commands in the following format:")
        print("\nExample commands:")
        print('  {"command": "move_home"}')
        print('  {"command": "move_pose", "pose": [x, y, z, rx, ry, rz]}')
        print('  {"command": "pick", "position": [x, y, z], "orientation": [rx, ry, rz]}')
        print('  {"command": "place", "position": [x, y, z], "orientation": [rx, ry, rz]}')
        print('  {"command": "wait", "duration": 2.0}')
        print('  {"command": "get_pose"}')
        print('  {"command": "get_joints"}')
        print('\nNote: Gripper is controlled automatically during pick/place operations')
        
        # ====================================
        # Step 3: Start the Server
        # ====================================
        print("\n" + "=" * 60)
        print("Starting Server")
        print("=" * 60)
        print("\nPress Ctrl+C to stop the server\n")
        
        # Start the server (this will block and listen for connections)
        server.start()
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure:")
        print("1. RoboDK is running")
        print("2. A robot is loaded in the RoboDK station")
        print("3. The RoboDK Python API is installed (pip install robodk)")
        return 1
    
    finally:
        # Cleanup
        try:
            robot.disconnect()
        except:
            pass
    
    return 0


def example_commands():
    """
    Example function showing how to send commands to the server from a client.
    
    This function is not executed in normal operation but serves as documentation
    for how to send commands from a Raspberry Pi or other client device.
    """
    import socket
    import json
    
    # Example: Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.100', 5000))  # Replace with actual server IP
    
    # Example 1: Move to home position
    command = {"command": "move_home"}
    client.send(json.dumps(command).encode('utf-8'))
    response = client.recv(4096)
    print(json.loads(response.decode('utf-8')))
    
    # Example 2: Pick object
    command = {
        "command": "pick",
        "position": [300, 200, 150],
        "orientation": [0, 90, 0]
    }
    client.send(json.dumps(command).encode('utf-8'))
    response = client.recv(4096)
    print(json.loads(response.decode('utf-8')))
    
    # Example 3: Place object
    command = {
        "command": "place",
        "position": [400, 200, 150],
        "orientation": [0, 90, 0]
    }
    client.send(json.dumps(command).encode('utf-8'))
    response = client.recv(4096)
    print(json.loads(response.decode('utf-8')))
    
    # Example 4: Get current pose
    command = {"command": "get_pose"}
    client.send(json.dumps(command).encode('utf-8'))
    response = client.recv(4096)
    print(json.loads(response.decode('utf-8')))
    
    client.close()


if __name__ == "__main__":
    sys.exit(main())
