"""
Run Sorting System - Dashboard with Live Camera Feed

Launch this file to start the complete sorting system with:
- Live camera feed with YOLO detection
- Robot connection and control
- Automated sorting workflow
"""

from sorting_dashboard import main

if __name__ == "__main__":
    print("=" * 70)
    print("  🤖 ROBOT SORTING DASHBOARD - LIVE VISION SYSTEM")
    print("=" * 70)
    print("\nStarting dashboard with embedded camera feed...")
    print("\nFeatures:")
    print("  📹 Live camera with YOLO detection")
    print("  🔗 Robot connection management")
    print("  🎯 Real-time piece detection")
    print("  ▶️  Automated sorting workflow")
    print("  📊 Progress tracking")
    print("\nInstructions:")
    print("  1. Click 'Start Camera' to begin detection")
    print("  2. Connect to the robot")
    print("  3. Click 'Capture & Detect' to finalize detections")
    print("  4. Click 'START SORTING' for automated sorting")
    print("\n" + "=" * 70 + "\n")
    
    main()
