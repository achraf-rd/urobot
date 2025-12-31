"""
Command Server Module - TCP server for receiving robot commands via network
"""

import socket
import json
import threading
from typing import Callable, Dict, Any


class CommandServer:
    """
    A TCP server that listens for JSON commands from remote clients (e.g., Raspberry Pi).
    
    The server receives JSON commands and executes them using a provided RobotController instance.
    """
    
    def __init__(self, host='0.0.0.0', port=5000, robot_controller=None):
        """
        Initialize the command server.
        
        Args:
            host (str): IP address to bind the server to. Default is '0.0.0.0' (all interfaces).
            port (int): Port number to listen on. Default is 5000.
            robot_controller: Instance of RobotController to execute commands.
        """
        self.host = host
        self.port = port
        self.robot_controller = robot_controller
        self.server_socket = None
        self.running = False
        self.command_handlers = self._setup_command_handlers()
    
    def _setup_command_handlers(self) -> Dict[str, Callable]:
        """
        Set up the mapping between command names and handler methods.
        
        Returns:
            dict: Dictionary mapping command names to handler functions.
        """
        return {
            'move_home': self._handle_move_home,
            'move_pose': self._handle_move_pose,
            'pick': self._handle_pick,
            'place': self._handle_place,
            'wait': self._handle_wait,
            'get_pose': self._handle_get_pose,
            'get_joints': self._handle_get_joints,
        }
    
    def _handle_move_home(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle move_home command."""
        success = self.robot_controller.move_to_home()
        return {'status': 'success' if success else 'error', 'command': 'move_home'}
    
    def _handle_move_pose(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle move_pose command."""
        pose = data.get('pose', [])
        success = self.robot_controller.move_to_pose(pose)
        return {'status': 'success' if success else 'error', 'command': 'move_pose'}
    
    def _handle_pick(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pick command."""
        position = data.get('position', [])
        orientation = data.get('orientation', [])
        success = self.robot_controller.pick_object(position, orientation)
        return {'status': 'success' if success else 'error', 'command': 'pick'}
    
    def _handle_place(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle place command."""
        position = data.get('position', [])
        orientation = data.get('orientation', [])
        success = self.robot_controller.place_object(position, orientation)
        return {'status': 'success' if success else 'error', 'command': 'place'}
    
    def _handle_wait(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle wait command."""
        duration = data.get('duration', 1.0)
        success = self.robot_controller.wait(duration)
        return {'status': 'success' if success else 'error', 'command': 'wait'}
    
    def _handle_get_pose(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_pose command."""
        pose = self.robot_controller.get_current_pose()
        return {'status': 'success', 'command': 'get_pose', 'pose': pose}
    
    def _handle_get_joints(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_joints command."""
        joints = self.robot_controller.get_current_joints()
        return {'status': 'success', 'command': 'get_joints', 'joints': joints}
    
    def _process_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a received command and execute the appropriate handler.
        
        Args:
            command_data (dict): Parsed JSON command data.
        
        Returns:
            dict: Response dictionary with execution result.
        """
        command = command_data.get('command', '')
        
        if not command:
            return {'status': 'error', 'message': 'No command specified'}
        
        if command not in self.command_handlers:
            return {'status': 'error', 'message': f'Unknown command: {command}'}
        
        try:
            handler = self.command_handlers[command]
            response = handler(command_data)
            return response
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'command': command}
    
    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """
        Handle communication with a connected client.
        
        Args:
            client_socket: Socket object for the client connection.
            address: Client address tuple (host, port).
        """
        print(f"Client connected from {address}")
        
        try:
            while self.running:
                # Receive data from client
                data = client_socket.recv(4096)
                
                if not data:
                    break
                
                try:
                    # Parse JSON command
                    command_data = json.loads(data.decode('utf-8'))
                    print(f"Received command: {command_data}")
                    
                    # Process the command
                    response = self._process_command(command_data)
                    
                    # Send response back to client
                    response_json = json.dumps(response) + '\n'
                    client_socket.send(response_json.encode('utf-8'))
                    print(f"Sent response: {response}")
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        'status': 'error',
                        'message': f'Invalid JSON: {str(e)}'
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    print(f"JSON decode error: {e}")
                
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Client disconnected: {address}")
    
    def start(self):
        """
        Start the command server and begin listening for connections.
        """
        if not self.robot_controller:
            raise ValueError("Robot controller not set. Cannot start server.")
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Command server started on {self.host}:{self.port}")
            print("Waiting for connections...")
            
            while self.running:
                try:
                    # Set timeout to allow periodic checking of self.running
                    self.server_socket.settimeout(1.0)
                    
                    try:
                        client_socket, address = self.server_socket.accept()
                        
                        # Handle each client in a separate thread
                        client_thread = threading.Thread(
                            target=self._handle_client,
                            args=(client_socket, address)
                        )
                        client_thread.daemon = True
                        client_thread.start()
                        
                    except socket.timeout:
                        continue
                        
                except KeyboardInterrupt:
                    print("\nShutting down server...")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """
        Stop the command server and close all connections.
        """
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Command server stopped.")
    
    def set_robot_controller(self, robot_controller):
        """
        Set or update the robot controller instance.
        
        Args:
            robot_controller: Instance of RobotController to use for command execution.
        """
        self.robot_controller = robot_controller
