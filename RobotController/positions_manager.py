"""
Positions Manager - Loads and manages robot positions from file
"""

import os


class PositionsManager:
    """
    Manages robot positions loaded from positions.txt file.
    """
    
    def __init__(self, positions_file='positions.txt'):
        """
        Initialize the positions manager.
        
        Args:
            positions_file (str): Path to positions file
        """
        self.positions_file = positions_file
        self.positions = {}
        self.load_positions()
    
    def load_positions(self):
        """
        Load positions from the positions file.
        
        Format expected:
        name : [x, y, z, rx, ry, rz]
        or
        name : [x, y, z] with orientation: [rx, ry, rz]
        """
        if not os.path.exists(self.positions_file):
            print(f"Warning: Positions file '{self.positions_file}' not found")
            return
        
        print(f"Loading positions from {self.positions_file}...")
        
        with open(self.positions_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Parse line
                if ':' in line:
                    # Split by colon
                    parts = line.split(':', 1)
                    name = parts[0].strip().lower()
                    value_part = parts[1].strip()
                    
                    try:
                        # Check if it has "with orientation" format
                        if 'with orientation:' in value_part:
                            # Format: [x, y, z] with orientation: [rx, ry, rz]
                            pos_part, orient_part = value_part.split('with orientation:')
                            position = eval(pos_part.strip())  # [x, y, z]
                            orientation = eval(orient_part.strip())  # [rx, ry, rz]
                            pose = position + orientation  # [x, y, z, rx, ry, rz]
                        else:
                            # Format: [x, y, z, rx, ry, rz]
                            pose = eval(value_part)
                        
                        # Store as [position, orientation] for pick/place commands
                        if len(pose) == 6:
                            self.positions[name] = {
                                'position': pose[:3],  # [x, y, z]
                                'orientation': pose[3:]  # [rx, ry, rz]
                            }
                            print(f"  Loaded '{name}': {pose}")
                        else:
                            print(f"  Warning: Invalid pose format for '{name}': {pose}")
                    
                    except Exception as e:
                        print(f"  Error parsing line '{line}': {e}")
        
        print(f"✓ Loaded {len(self.positions)} positions")
    
    def get_position(self, name):
        """
        Get position and orientation by name.
        
        Args:
            name (str): Position name (e.g., 'piece 1', 'bad bin')
        
        Returns:
            dict: {'position': [x, y, z], 'orientation': [rx, ry, rz]} or None
        """
        name = name.lower().strip()
        return self.positions.get(name)
    
    def get_all_positions(self):
        """
        Get all available position names.
        
        Returns:
            list: List of position names
        """
        return list(self.positions.keys())
    
    def reload_positions(self):
        """
        Reload positions from file.
        """
        self.positions = {}
        self.load_positions()


if __name__ == "__main__":
    # Test the positions manager
    pm = PositionsManager()
    print("\nAvailable positions:")
    for name in pm.get_all_positions():
        pos = pm.get_position(name)
        print(f"  {name}: {pos}")
