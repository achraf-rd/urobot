# Contributing to UR5 Robotic Sorting System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

1. **Check existing issues** - Search for similar issues first
2. **Provide details** - Include:
   - System information (OS, Python version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs
   - Screenshots if applicable

### Suggesting Enhancements

1. Open an issue with tag `enhancement`
2. Describe the feature and use case
3. Explain why it would be useful
4. Provide examples if possible

### Code Contributions

#### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd urobot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
cd RobotController
pip install robodk

cd ../Client_Ai_detector
pip install -r requirement.txt
```

#### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments and docstrings
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Test robot controller
   cd RobotController/tests
   python test_local.py
   
   # Test client
   cd Client_Ai_detector
   python camera_raspberry_test.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```
   
   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what you changed and why
   - Reference related issues
   - Include test results

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where applicable

### Example:
```python
def pick_object(self, position: list, orientation: list, pick_offset_mm: float = 30) -> bool:
    """
    Execute a pick operation at the specified position and orientation.
    
    Args:
        position (list): [x, y, z] coordinates in mm
        orientation (list): [rx, ry, rz] orientation angles
        pick_offset_mm (float): Distance to move down to grasp object
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Implementation
    pass
```

### Documentation
- Update README.md if adding features
- Add comments for complex logic
- Include usage examples
- Keep documentation in sync with code

### Testing
- Test on both simulation and real robot if possible
- Verify network communication
- Test error handling
- Document test results in PR

## Project Structure Guidelines

### Adding New Files
```
RobotController/
  - Core functionality goes here
  - Tests in tests/ subdirectory
  - Client examples in client_ex/
  - Documentation in docs/

Client_Ai_detector/
  - Vision and AI functionality
  - Keep robot_client.py interface stable
  - Document any YOLO model changes
```

### Naming Conventions
- Files: `lowercase_with_underscores.py`
- Classes: `CamelCase`
- Functions: `lowercase_with_underscores`
- Constants: `UPPERCASE_WITH_UNDERSCORES`

## Areas for Contribution

### High Priority
- [ ] Add support for more gripper types
- [ ] Improve error recovery mechanisms
- [ ] Add more detection models (besides YOLO)
- [ ] Performance optimization
- [ ] Additional safety checks

### Medium Priority
- [ ] Web-based dashboard
- [ ] Database for logging operations
- [ ] Multi-camera support
- [ ] Advanced motion planning
- [ ] Configuration GUI

### Documentation
- [ ] Video tutorials
- [ ] More code examples
- [ ] Troubleshooting guides
- [ ] Translation to other languages

## Questions?

Feel free to:
- Open an issue with tag `question`
- Check existing documentation
- Review example code

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
