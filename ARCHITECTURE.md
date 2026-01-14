# System Architecture - UR5 Robotic Sorting System

This document describes the architecture, components, and communication protocols of the UR5 Robotic Sorting System.

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Details](#component-details)
4. [Communication Protocol](#communication-protocol)
5. [Data Flow](#data-flow)
6. [Sequence Diagrams](#sequence-diagrams)
7. [Technology Stack](#technology-stack)

---

## Overview

The system consists of two main components that communicate over TCP/IP:

1. **Robot Controller (Server)** - Controls UR5 robot via RoboDK
2. **AI Vision Client** - Detects and classifies objects using YOLO

```
┌─────────────────────┐         Network          ┌──────────────────────┐
│   AI Vision Client  │◄──────  TCP/IP  ────────►│  Robot Controller    │
│   (Raspberry Pi)    │      (Port 5000)         │      (PC/RoboDK)     │
└─────────────────────┘                          └──────────────────────┘
         │                                                  │
         ▼                                                  ▼
    ┌────────┐                                      ┌─────────────┐
    │ Camera │                                      │   UR5 Robot │
    └────────┘                                      │   + Gripper │
                                                    └─────────────┘
```

---

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Robot Controller (Server)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │   Command   │───►│    Robot     │───►│     RoboDK       │   │
│  │   Server    │    │  Controller  │    │     API          │   │
│  │  (TCP 5000) │    │              │    │                  │   │
│  └─────────────┘    └──────────────┘    └──────────────────┘   │
│         │                   │                       │            │
│         │                   ▼                       │            │
│         │           ┌──────────────┐                │            │
│         │           │  Dashboard   │                │            │
│         │           │   Gripper    │────────────────┘            │
│         │           └──────────────┘                             │
│         │                   │                                    │
│         │                   │ Dashboard Server                   │
│         │                   ▼          (Port 29999)              │
│         │           ┌──────────────┐                             │
│         └──────────►│  Positions   │                             │
│                     │   Manager    │                             │
│                     └──────────────┘                             │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ Network (JSON Commands)
                              │
┌──────────────────────────────────────────────────────────────────┐
│                    AI Vision Client                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  Sorting    │───►│    Robot     │───►│   TCP Socket     │   │
│  │  Dashboard  │    │   Client     │    │  Communication   │   │
│  │   (GUI)     │    │              │    │                  │   │
│  └─────────────┘    └──────────────┘    └──────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────┐    ┌──────────────┐                           │
│  │   Camera    │───►│     YOLO     │                           │
│  │  Capture    │    │  Detection   │                           │
│  └─────────────┘    └──────────────┘                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Robot Controller (Server)

#### CommandServer (`command_server.py`)
**Purpose:** TCP server that listens for JSON commands from clients

**Responsibilities:**
- Accept TCP connections on port 5000
- Parse JSON command messages
- Route commands to appropriate handlers
- Return JSON responses
- Support multiple concurrent clients (threading)

**Key Methods:**
```python
start()                          # Start server
_handle_client(client_socket)    # Handle individual client
_process_command(command_dict)   # Parse and route commands
```

#### RobotController (`robot_controller.py`)
**Purpose:** High-level robot control abstraction

**Responsibilities:**
- Interface with RoboDK API
- Execute robot movements
- Manage gripper operations
- Handle approach positions for pick operations
- Reconnect RoboDK after Dashboard commands

**Key Methods:**
```python
move_to_home()                                    # Move to home position
move_to_pose(pose)                               # Move to specific pose
pick_object(position, orientation, offset)       # Pick sequence
place_object(position, orientation)              # Place sequence
get_current_pose()                               # Query robot state
get_current_joints()                             # Query joint angles
```

#### DashboardGripper (`dashboard_gripper.py`)
**Purpose:** Control OnRobot RG2 gripper via Dashboard Server

**Responsibilities:**
- Send Dashboard Server commands (TCP port 29999)
- Load and execute .urp programs (open-gripper, close-gripper)
- Reconnect RoboDK after Dashboard operations
- Handle connection errors

**Key Methods:**
```python
open(program_name)                    # Open gripper
close(program_name)                   # Close gripper
_send_dashboard_command(command)      # Send TCP command
_check_and_reconnect_robodk()        # Reconnect RoboDK
```

#### PositionsManager (`positions_manager.py`)
**Purpose:** Load and manage robot positions from file

**Responsibilities:**
- Parse positions.txt file
- Store positions as dictionaries
- Provide position lookup by name
- List all available positions

**Key Methods:**
```python
load_positions()                    # Load from file
get_position(name)                  # Get position by name
get_all_positions()                 # List all position names
```

---

### 2. AI Vision Client

#### SortingDashboard (`sorting_dashboard.py`)
**Purpose:** GUI application for vision-based sorting

**Responsibilities:**
- Display live camera feed
- Run YOLO object detection
- Visualize detection results (bounding boxes)
- Classify pieces (good/bad)
- Send robot commands automatically or manually
- Display statistics and status

**Key Components:**
```python
__init__()                          # Initialize GUI and components
setup_ui()                          # Create interface
process_frame()                     # Process camera frame
detect_objects()                    # Run YOLO detection
classify_piece()                    # Determine good/bad
send_robot_command()                # Send pick/place commands
```

#### RobotClient (`robot_client.py`)
**Purpose:** Network client for robot communication

**Responsibilities:**
- Establish TCP connection to robot server
- Send JSON commands
- Receive and parse responses
- Handle connection errors
- Provide high-level command methods

**Key Methods:**
```python
connect()                           # Connect to server
disconnect()                        # Close connection
send_command(command_dict)          # Send JSON command
pick_piece(piece_name)              # Pick by name
place_piece(location_name)          # Place by name
move_home()                         # Move to home
get_pose()                          # Query pose
list_positions()                    # Get available positions
```

---

## Communication Protocol

### Message Format

**JSON-based protocol over TCP/IP**

#### Command Structure
```json
{
  "command": "command_name",
  "param1": "value1",
  "param2": "value2"
}
```

#### Response Structure
```json
{
  "status": "success|error",
  "command": "command_name",
  "data": {},
  "message": "optional message"
}
```

### Available Commands

#### 1. Pick Piece by Name
```json
Request:
{
  "command": "pick_piece",
  "piece": "piece 1"
}

Response:
{
  "status": "success",
  "command": "pick_piece",
  "piece": "piece 1",
  "position": [103.43, -46.61, 123.26],
  "orientation": [3.06, 0.002, 2.24]
}
```

#### 2. Place Piece at Location
```json
Request:
{
  "command": "place_piece",
  "location": "bad bin"
}

Response:
{
  "status": "success",
  "command": "place_piece",
  "location": "bad bin",
  "position": [-68.18, -59.93, 203.93],
  "orientation": [-3.14, 0.086, 2.34]
}
```

#### 3. Move to Home
```json
Request:
{
  "command": "move_home"
}

Response:
{
  "status": "success",
  "command": "move_home"
}
```

#### 4. Get Current Pose
```json
Request:
{
  "command": "get_pose"
}

Response:
{
  "status": "success",
  "command": "get_pose",
  "pose": [58.22, 13.90, 353.84, -3.07, 0.046, 1.98]
}
```

#### 5. List Available Positions
```json
Request:
{
  "command": "list_positions"
}

Response:
{
  "status": "success",
  "command": "list_positions",
  "positions": ["home pose", "piece 1", "piece 2", "bad bin", "good bin"]
}
```

---

## Data Flow

### Complete Pick and Place Cycle

```
1. AI Vision Client                                    2. Robot Controller
┌────────────────────┐                                 ┌──────────────────┐
│ Camera captures    │                                 │                  │
│ frame              │                                 │                  │
└─────────┬──────────┘                                 │                  │
          │                                            │                  │
          ▼                                            │                  │
┌────────────────────┐                                 │                  │
│ YOLO detects piece │                                 │                  │
│ Classifies: GOOD   │                                 │                  │
└─────────┬──────────┘                                 │                  │
          │                                            │                  │
          ▼                                            │                  │
┌────────────────────┐                                 │                  │
│ User clicks "Pick" │                                 │                  │
│ or Auto-trigger    │                                 │                  │
└─────────┬──────────┘                                 │                  │
          │                                            │                  │
          ▼                                            ▼                  │
┌────────────────────┐     pick_piece command    ┌──────────────────┐   │
│ RobotClient sends  │────────────────────────►  │ CommandServer    │   │
│ JSON command       │                           │ receives         │   │
└────────────────────┘                           └─────────┬────────┘   │
                                                           │            │
                                                           ▼            │
                                                  ┌──────────────────┐  │
                                                  │ PositionsManager │  │
                                                  │ looks up piece 1 │  │
                                                  └─────────┬────────┘  │
                                                           │            │
                                                           ▼            │
                                                  ┌──────────────────┐  │
                                                  │ RobotController  │  │
                                                  │ pick_object()    │  │
                                                  └─────────┬────────┘  │
                                                           │            │
           ┌───────────────────────────────────────────────┤            │
           │                                               │            │
           ▼                                               ▼            │
    1. Move to approach position                   2. Open gripper     │
       │                                               │                │
       ▼                                               ▼                │
    RoboDK moves robot                         DashboardGripper        │
                                                   │                    │
                                                   ▼                    │
                                              Dashboard Server          │
                                              load open-gripper.urp     │
                                              play                      │
                                                   │                    │
                                                   ▼                    │
                                              Reconnect RoboDK          │
           │                                               │            │
           ▼                                               ▼            │
    3. Move down to pick                           4. Close gripper    │
       │                                               │                │
       ▼                                               ▼                │
    RoboDK moves robot                         DashboardGripper        │
                                              load close-gripper.urp    │
                                              play                      │
                                                   │                    │
                                                   ▼                    │
                                              Reconnect RoboDK          │
           │                                                            │
           ▼                                                            │
    5. Move back to approach                                           │
       │                                                                │
       ▼                                                                │
    Return success ──────────────────────────────────────────────────►┘
           │
           ▼
┌────────────────────┐     success response      ┌────────────────────┐
│ RobotClient        │◄──────────────────────────│ CommandServer      │
│ receives response  │                           │ sends response     │
└─────────┬──────────┘                           └────────────────────┘
          │
          ▼
┌────────────────────┐
│ Dashboard updates  │
│ status and stats   │
└────────────────────┘
```

---

## Sequence Diagrams

### Pick Piece Sequence

```
Client          RobotClient    CommandServer   PositionsManager   RobotController   DashboardGripper   Robot
  │                  │               │                 │                  │                │            │
  │─Click "Pick"────>│               │                 │                  │                │            │
  │                  │               │                 │                  │                │            │
  │                  │─pick_piece───>│                 │                  │                │            │
  │                  │  {piece:1}    │                 │                  │                │            │
  │                  │               │                 │                  │                │            │
  │                  │               │─get_position───>│                  │                │            │
  │                  │               │  "piece 1"      │                  │                │            │
  │                  │               │<─position data──│                  │                │            │
  │                  │               │                 │                  │                │            │
  │                  │               │─pick_object────────────────────────>│                │            │
  │                  │               │  (pos, orient)                     │                │            │
  │                  │               │                                    │                │            │
  │                  │               │                                    │─Move approach─────────────>│
  │                  │               │                                    │                │            │
  │                  │               │                                    │─Open gripper──>│            │
  │                  │               │                                    │                │            │
  │                  │               │                                    │                │─Dashboard─>│
  │                  │               │                                    │                │ commands   │
  │                  │               │                                    │<─Reconnect RDK─│            │
  │                  │               │                                    │                │            │
  │                  │               │                                    │─Move down─────────────────>│
  │                  │               │                                    │                │            │
  │                  │               │                                    │─Close gripper─>│            │
  │                  │               │                                    │                │            │
  │                  │               │                                    │                │─Dashboard─>│
  │                  │               │                                    │<─Reconnect RDK─│            │
  │                  │               │                                    │                │            │
  │                  │               │                                    │─Move up───────────────────>│
  │                  │               │                                    │                │            │
  │                  │               │<─success───────────────────────────│                │            │
  │                  │               │                                                     │            │
  │                  │<─response─────│                                                     │            │
  │                  │  {status:ok}  │                                                     │            │
  │<─Update UI───────│               │                                                     │            │
  │                  │               │                                                     │            │
```

---

## Technology Stack

### Robot Controller
- **Language:** Python 3.8+
- **Framework:** RoboDK API
- **Networking:** Python socket library
- **Data Format:** JSON
- **Threading:** Python threading module

### AI Vision Client
- **Language:** Python 3.8+
- **GUI:** Tkinter
- **AI/ML:** Ultralytics YOLO
- **Vision:** OpenCV
- **Image Processing:** Pillow, NumPy
- **Networking:** Python socket library

### Robot Hardware
- **Robot:** Universal Robots UR5
- **Gripper:** OnRobot RG2
- **Protocol:** UR Dashboard Server (TCP port 29999)
- **URCap:** OnRobot RG2 URCap

### Communication
- **Protocol:** TCP/IP
- **Port:** 5000 (Command Server)
- **Port:** 29999 (Dashboard Server)
- **Format:** JSON over TCP

---

## Design Patterns

### Server Side
- **Command Pattern:** Command handlers mapped to operations
- **Singleton:** Single RobotController instance per server
- **Strategy:** Different gripper control strategies
- **Observer:** Position manager notifies on updates

### Client Side
- **Facade:** RobotClient simplifies network communication
- **MVC:** Dashboard separates UI, logic, and data
- **State:** Detection state management
- **Observer:** GUI updates on detection events

---

## Security Considerations

1. **No Authentication:** Currently no auth on TCP server
   - Suitable for closed networks only
   - Add authentication for open networks

2. **No Encryption:** Messages sent in plain JSON
   - Use TLS/SSL for sensitive environments

3. **Input Validation:** Commands validated before execution
   - Position bounds checking
   - Command format verification

4. **Network Isolation:** Recommended setup
   - Isolated network for robot system
   - Firewall rules for port access

---

## Performance Considerations

### Latency
- **Network:** <10ms on local network
- **Command Processing:** <50ms
- **Robot Movement:** Depends on distance/speed
- **Vision Processing:** 10-30 FPS (Raspberry Pi 4)

### Bottlenecks
- YOLO inference on Raspberry Pi
- Camera frame rate
- Network bandwidth (video streaming if implemented)

### Optimization Strategies
- Reduce image resolution for detection
- Use threading for concurrent operations
- Cache position lookups
- Connection pooling for multiple clients

---

**Document Version:** 1.0
**Last Updated:** January 2026
