"""
Client Pick and Place Test - Test all positions using network client
=====================================================================
This script tests pick and place operations for all positions defined
in positions.txt by sending commands through the network client.

Make sure the robot server is running before executing this test:
    python main.py
"""

import sys
import os

# Add client_ex directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'client_ex'))

from client_example import RobotClient
import time


def test_all_pick_and_place(server_ip="192.168.1.10", test_mode="simulation"):
    """
    Test pick and place for all piece positions.
    
    Args:
        server_ip (str): IP address of the robot server
        test_mode (str): "simulation" or "real"
    """
    print("\n" + "="*70)
    print("  CLIENT PICK AND PLACE TEST - ALL POSITIONS")
    print("="*70)
    print(f"\nServer IP: {server_ip}")
    print(f"Mode: {test_mode.upper()}")
    
    # Create client and connect
    print("\n[1] Connecting to robot server...")
    client = RobotClient(server_ip)
    
    if not client.connect():
        print("\n✗ Failed to connect to server!")
        print("\nTroubleshooting:")
        print("  1. Make sure server is running: python main.py")
        print(f"  2. Check IP address is correct: {server_ip}")
        print("  3. Check firewall allows port 5000")
        print("  4. Ping server: ping", server_ip)
        return False
    
    print("✓ Connected to server")
    
    try:
        # Get available positions
        print("\n[2] Getting available positions...")
        response = client.list_positions()
        
        if response.get('status') != 'success':
            print(f"✗ Failed to get positions: {response}")
            return False
        
        positions = response.get('positions', [])
        print(f"✓ Found {len(positions)} positions: {positions}")
        
        # Filter pieces and bins
        pieces = [p for p in positions if p.startswith('piece')]
        bins = [p for p in positions if 'bin' in p]
        
        print(f"\nPieces: {pieces}")
        print(f"Bins: {bins}")
        
        if not pieces:
            print("\n✗ No pieces found in positions!")
            return False
        
        if not bins:
            print("\n✗ No bins found in positions!")
            return False
        
        # Move to home first
        print("\n[3] Moving to home position...")
        response = client.move_home()
        if response.get('status') == 'success':
            print("✓ Moved to home")
        else:
            print(f"⚠ Warning: {response}")
        
        # Test each piece to each bin
        total_tests = len(pieces) * len(bins)
        current_test = 0
        successful_tests = 0
        failed_tests = 0
        
        print(f"\n[4] Starting {total_tests} pick and place operations...")
        print("="*70)
        
        for piece in pieces:
            for bin_location in bins:
                current_test += 1
                
                print(f"\n--- Test {current_test}/{total_tests} ---")
                print(f"Pick: {piece} → Place: {bin_location}")
                
                # Pick the piece
                print(f"\n  [A] Picking {piece}...")
                pick_response = client.pick_piece(piece)
                
                if pick_response.get('status') != 'success':
                    print(f"  ✗ Pick failed: {pick_response.get('message', 'Unknown error')}")
                    failed_tests += 1
                    
                    # Try to recover by moving home
                    print("  → Attempting recovery - moving to home...")
                    client.move_home()
                    time.sleep(2)
                    continue
                
                print(f"  ✓ Picked {piece}")
                
                # Wait a bit
                time.sleep(1)
                
                # Place the piece
                print(f"\n  [B] Placing at {bin_location}...")
                place_response = client.place_piece(bin_location)
                
                if place_response.get('status') != 'success':
                    print(f"  ✗ Place failed: {place_response.get('message', 'Unknown error')}")
                    failed_tests += 1
                    
                    # Try to recover
                    print("  → Attempting recovery - moving to home...")
                    client.move_home()
                    time.sleep(2)
                    continue
                
                print(f"  ✓ Placed at {bin_location}")
                successful_tests += 1
                
                # Small delay between operations
                print(f"\n  ✓ Test {current_test} completed successfully!")
                time.sleep(2)
        
        # Return to home at end
        print("\n[5] Returning to home position...")
        client.move_home()
        
        # Print summary
        print("\n" + "="*70)
        print("  TEST SUMMARY")
        print("="*70)
        print(f"Total tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success rate: {(successful_tests/total_tests*100):.1f}%")
        
        if failed_tests == 0:
            print("\n✓ ALL TESTS PASSED!")
        else:
            print(f"\n⚠ {failed_tests} tests failed")
        
        return failed_tests == 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        print("Moving to home position...")
        try:
            client.move_home()
        except:
            pass
        return False
        
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Always disconnect
        print("\n[6] Disconnecting from server...")
        client.disconnect()


def test_single_pick_place_cycle(server_ip="192.168.1.10"):
    """
    Test a single pick and place cycle for quick verification.
    
    Args:
        server_ip (str): IP address of the robot server
    """
    print("\n" + "="*70)
    print("  QUICK TEST - Single Pick and Place Cycle")
    print("="*70)
    
    client = RobotClient(server_ip)
    
    if not client.connect():
        print("✗ Failed to connect to server")
        return False
    
    try:
        print("\n[1] Moving to home...")
        client.move_home()
        time.sleep(2)
        
        print("\n[2] Picking piece 1...")
        response = client.pick_piece('piece 1')
        print(f"Response: {response}")
        
        if response.get('status') != 'success':
            print("✗ Pick failed!")
            return False
        
        time.sleep(2)
        
        print("\n[3] Placing at bad bin...")
        response = client.place_piece('bad bin')
        print(f"Response: {response}")
        
        if response.get('status') != 'success':
            print("✗ Place failed!")
            return False
        
        time.sleep(2)
        
        print("\n[4] Returning to home...")
        client.move_home()
        
        print("\n✓ Single cycle completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
        
    finally:
        client.disconnect()


def test_specific_positions(server_ip="192.168.1.10", pieces=None, bins=None):
    """
    Test specific pieces and bins.
    
    Args:
        server_ip (str): IP address of the robot server
        pieces (list): List of piece names to test
        bins (list): List of bin names to test
    """
    if pieces is None:
        pieces = ['piece 1', 'piece 2']
    if bins is None:
        bins = ['bad bin']
    
    print("\n" + "="*70)
    print("  SPECIFIC POSITIONS TEST")
    print("="*70)
    print(f"\nPieces to test: {pieces}")
    print(f"Bins to test: {bins}")
    
    client = RobotClient(server_ip)
    
    if not client.connect():
        print("✗ Failed to connect to server")
        return False
    
    try:
        client.move_home()
        time.sleep(2)
        
        for i, piece in enumerate(pieces, 1):
            for j, bin_loc in enumerate(bins, 1):
                print(f"\n[{i}.{j}] {piece} → {bin_loc}")
                
                print(f"  → Picking {piece}...")
                response = client.pick_piece(piece)
                if response.get('status') != 'success':
                    print(f"  ✗ Failed: {response}")
                    continue
                
                time.sleep(1)
                
                print(f"  → Placing at {bin_loc}...")
                response = client.place_piece(bin_loc)
                if response.get('status') != 'success':
                    print(f"  ✗ Failed: {response}")
                    continue
                
                print(f"  ✓ Completed")
                time.sleep(2)
        
        client.move_home()
        print("\n✓ Test completed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
        
    finally:
        client.disconnect()


def main():
    """Main menu for testing."""
    print("\n" + "="*70)
    print("  ROBOT CLIENT PICK AND PLACE TEST SUITE")
    print("="*70)
    print("\nTest Options:\n")
    print("  1 - Quick Test (1 piece, 1 bin)")
    print("  2 - All Positions Test (all pieces, all bins)")
    print("  3 - Specific Positions Test (piece 1-3, bad bin)")
    print("  4 - Custom Test (enter piece and bin names)")
    print("="*70)
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    # Get server IP
    default_ip = "192.168.1.10"
    server_ip = input(f"\nEnter server IP (default: {default_ip}): ").strip()
    if not server_ip:
        server_ip = default_ip
    
    print(f"\nUsing server IP: {server_ip}")
    print("\nIMPORTANT: Make sure robot server is running:")
    print("  python main.py")
    
    input("\nPress ENTER to continue or Ctrl+C to cancel...")
    
    if choice == '1':
        test_single_pick_place_cycle(server_ip)
        
    elif choice == '2':
        confirm = input("\n⚠ This will test ALL positions (may take a while). Continue? (y/n): ")
        if confirm.lower() == 'y':
            test_all_pick_and_place(server_ip)
        
    elif choice == '3':
        pieces = ['piece 1', 'piece 2', 'piece 3']
        bins = ['bad bin']
        test_specific_positions(server_ip, pieces, bins)
        
    elif choice == '4':
        pieces_input = input("\nEnter piece names (comma-separated, e.g., piece 1,piece 2): ")
        bins_input = input("Enter bin names (comma-separated, e.g., bad bin,good bin): ")
        
        pieces = [p.strip() for p in pieces_input.split(',')]
        bins = [b.strip() for b in bins_input.split(',')]
        
        test_specific_positions(server_ip, pieces, bins)
        
    else:
        print("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Test cancelled by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
