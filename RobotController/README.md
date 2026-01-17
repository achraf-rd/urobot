# Robot Controller with Network Interface

A modular Python robot controller using the RoboDK API with TCP/IP network interface for remote control.

## Features

- **RobotController Class**: High-level interface for robot operations
  - Move to home position
  - Move to specific poses
  - Pick and place operations
  - Wait commands
  - Query current pose and joint positions

- **Network Command Server**: TCP server (port 5000) for receiving JSON commands
  - Supports commands from Raspberry Pi or other network clients
  - JSON-based command protocol
  - Multi-threaded client handling

## Installation

1. Install RoboDK and the Python API:
```bash
pip install robodk
```

2. Ensure RoboDK is running with a robot loaded in the station.

## Usage

### Starting the Server

Run the main script to start the robot controller and command server:

```bash
python main.py
```

The server will listen on `0.0.0.0:5000` (all network interfaces, port 5000).

### Command Format

Commands are sent as JSON messages over TCP. Each command should be a valid JSON object.

#### Available Commands

1. **Move to Home**
```json
{"command": "move_home"}
```

2. **Move to Pose**
```json
{
    "command": "move_pose",
    "pose": [x, y, z, rx, ry, rz]
}
```
- `x, y, z`: Position in mm
- `rx, ry, rz`: Orientation in degrees

3. **Pick Object**
```json
{
    "command": "pick",
    "position": [x, y, z],
    "orientation": [rx, ry, rz]
}
```

4. **Place Object**
```json
{
    "command": "place",
    "position": [x, y, z],
    "orientation": [rx, ry, rz]
}
```

5. **Wait**
```json
{
    "command": "wait",
    "duration": 2.0
}
```
....
6. **Get Current Pose**
```json
{"command": "get_pose"}
```

7. **Get Current Joint Angles**
```json
{"command": "get_joints"}
```

### Response Format

All commands return a JSON response:

**Success:**
```json
{
    "status": "success",
    "command": "move_home"
}
```

**Error:**
```json
{
    "status": "error",
    "message": "Error description",
    "command": "move_home"
}
```

**Query responses** (e.g., get_pose):
```json
{
    "status": "success",
    "command": "get_pose",
    "pose": [x, y, z, rx, ry, rz]
}
```

## Client Example (Raspberry Pi)

Here's how to send commands from a Raspberry Pi or any Python client:

```python
import socket
import json

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.100', 5000))  # Replace with server IP

# Send a command
command = {
    "command": "pick",
    "position": [300, 200, 150],
    "orientation": [0, 90, 0]
}
client.send(json.dumps(command).encode('utf-8'))

# Receive response
response = client.recv(4096)
result = json.loads(response.decode('utf-8'))
print(result)

client.close()
```

## Module Structure

```
RobotController/
├── robot_controller.py    # RobotController class with robot operations
├── command_server.py       # TCP server for network commands
├── main.py                 # Main entry point and example usage
└── README.md               # This file
```

## Architecture

### RobotController Class
- Manages connection to RoboDK
- Provides high-level robot operation methods
- Handles error checking and validation

### CommandServer Class
- TCP server listening on port 5000
- Parses JSON commands
- Routes commands to appropriate RobotController methods
- Returns JSON responses
- Supports multiple simultaneous clients

## Configuration

### Changing Port or Host

Edit the `main.py` file:

```python
server = CommandServer(
    host='0.0.0.0',  # Change to specific IP if needed
    port=5000,        # Change port if needed
    robot_controller=robot
)
```

### Specifying Robot Name

If you have multiple robots in RoboDK:

```python
robot = RobotController("UR5")  # Specify robot name
```

## Error Handling

The system includes comprehensive error handling:
- Connection errors are caught and reported
- Invalid commands return error responses
- Robot operation failures are logged and returned to client
- Server continues running even if individual commands fail

## Safety Notes

⚠️ **Important Safety Considerations:**

1. Always test in simulation mode first
2. Ensure the workspace is clear before executing commands
3. Have emergency stop accessible
4. Verify position and orientation values before sending commands
5. Start with slow movements and test pick/place positions carefully

## Troubleshooting

**"Robot not found" error:**
- Ensure RoboDK is running
- Verify a robot is loaded in the station
- Check robot name if specified

**Cannot connect to server:**
- Check firewall settings
- Verify server IP address and port
- Ensure server is running (`python main.py`)

**Commands not executing:**
- Check RoboDK simulation/connection status
- Verify command JSON format
- Check server console for error messages

## License

This code is provided as-is for educational and development purposes.
