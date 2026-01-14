# Changelog

All notable changes to the UR5 Robotic Sorting System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-14

### Added
- **Robot Controller Server**
  - RoboDK API integration for UR5 control
  - TCP/IP network server on port 5000
  - JSON command protocol
  - OnRobot RG2 gripper control via Dashboard Server
  - Automatic RoboDK reconnection after Dashboard commands
  - Position management system (positions.txt)
  - Pick and place operations with approach positions
  - Command handlers: pick_piece, place_piece, move_home, get_pose, get_joints
  
- **AI Vision Client**
  - YOLO object detection integration
  - Real-time camera feed processing
  - Quality classification (good/bad pieces)
  - Live dashboard with statistics
  - Automatic robot control integration
  - Configurable piece regions
  
- **Testing Suite**
  - Local robot tests (no network)
  - Network client tests
  - Gripper control tests (3 methods)
  - Camera verification tests
  
- **Documentation**
  - Main README with quick start guide
  - Robot controller detailed documentation
  - UR5 connection guide
  - Orientation and speed control guide
  - API command examples
  - Contributing guidelines
  - MIT License

### Features
- Multi-client support via threading
- Error recovery and reconnection handling
- Predefined positions with easy configuration
- Dashboard Server integration for gripper control
- Comprehensive test coverage
- Modular architecture for easy extension

### Technical Details
- Python 3.8+ compatible
- RoboDK 5.6.0+ support
- Ultralytics YOLO for detection
- OpenCV for image processing
- Socket-based networking
- JSON message protocol

---

## [Unreleased]

### Planned Features
- [ ] Web-based control dashboard
- [ ] Database logging for operations
- [ ] Multi-camera support
- [ ] Additional gripper types
- [ ] Advanced motion planning
- [ ] REST API interface
- [ ] Docker containerization
- [ ] Performance metrics dashboard

### Known Issues
- Robot may report "busy" status immediately after Dashboard commands (mitigated with WaitMove)
- YOLO model file (yolo.pt) not included in repository (must be provided separately)
- Camera resolution affects detection FPS on Raspberry Pi

---

## Version History

### [1.0.0] - 2026-01-14
Initial release with full robot control and AI vision integration.

---

**Note:** This changelog will be updated with each significant release.
