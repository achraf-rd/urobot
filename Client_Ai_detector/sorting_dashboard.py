"""
Sorting Dashboard - Complete Interface with Embedded Camera & YOLO Detection

Features:
1. Live camera feed with YOLO detection
2. Robot connection management
3. Automated sorting using pick_piece() and place_piece()
4. Real-time progress tracking
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
import threading
import time
import platform
from ultralytics import YOLO
from robot_client import RobotClient


class SortingDashboard:
    """
    Main dashboard with embedded camera and YOLO detection.
    """
    
    def __init__(self):
        """Initialize the dashboard."""
        self.root = tk.Tk()
        self.root.title("🤖 Robot Sorting Dashboard - Live Vision System")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)  # Allow window resizing and maximize button
        self.root.minsize(900, 550)  # Set minimum window size
        
        # Theme colors
        self.dark_bg = "#1e1e1e"
        self.dark_fg = "#ffffff"
        self.dark_secondary = "#2d2d2d"
        self.dark_accent = "#0d7377"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"
        self.warning_color = "#ff9800"
        
        self.root.configure(bg=self.dark_bg)
        
        # YOLO model configuration
        self.model_path = "yolo.pt"
        self.conf_thresh = 0.3  # Lower threshold to detect BAD pieces better
        self.camera_id = 0  # Default camera (0=first camera, 1=second camera)
        self.contrast = 1.5
        self.brightness = -30
        
        # Fixed piece positions (x1, y1, x2, y2) - calibrated to actual camera view
        # These represent the 6 fixed positions where pieces are located
        # Visual IDs on screen (will be remapped for robot)
        self.piece_regions = {
            1: (300, 280, 500, 480),   # Bottom middle
            2: (240, 80, 440, 280),    # Top middle
            3: (40, 80, 240, 280),     # Top left
            4: (440, 80, 640, 280),    # Top right
            5: (500, 280, 700, 480),   # Bottom right
            6: (100, 280, 300, 480),   # Bottom left
        }
        
        # ID remapping: Visual ID → Robot ID
        # This maps what we show on screen to what the robot expects
        self.robot_id_map = {
            5: 1,  # Visual piece 5 → Robot piece 1
            4: 2,  # Visual piece 4 → Robot piece 2
            2: 3,  # Visual piece 2 → Robot piece 3
            3: 4,  # Visual piece 3 → Robot piece 4
            6: 5,  # Visual piece 6 → Robot piece 5
            1: 6,  # Visual piece 1 → Robot piece 6
        }
        
        # Camera and model
        self.cap = None
        self.model = None
        self.camera_running = False
        
        # Robot client
        self.robot_client = None
        self.robot_ip = "192.168.137.1"
        self.is_connected = False
        
        # Detection tracking
        self.piece_tracker = {}  # {centroid: piece_id}
        self.next_piece_id = 1
        self.detected_pieces = {}  # {piece_id: {"status": "GOOD"/"BAD", "centroid": (x,y)}}
        
        # Sorting state
        self.is_sorting = False
        self.good_pieces = []
        self.bad_pieces = []
        self.processed_pieces = 0
        self.total_pieces = 0
        
        # Build UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container with grid layout
        main_container = tk.Frame(self.root, bg=self.dark_bg)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights
        main_container.grid_columnconfigure(0, weight=3)  # Camera side
        main_container.grid_columnconfigure(1, weight=1)  # Control side
        main_container.grid_rowconfigure(0, weight=0)     # Header
        main_container.grid_rowconfigure(1, weight=1)     # Main content
        
        # ===== HEADER =====
        header_frame = tk.Frame(main_container, bg=self.dark_bg)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Robot Sorting Dashboard",
            font=("Arial", 18, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        )
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(
            header_frame,
            text="Live Vision & Automated Sorting",
            font=("Arial", 10),
            bg=self.dark_bg,
            fg="#888888"
        )
        subtitle_label.pack(side="left", padx=(15, 0))
        
        # ===== LEFT SIDE: CAMERA VIEW =====
        camera_container = tk.Frame(main_container, bg=self.dark_secondary, relief=tk.RIDGE, borderwidth=2)
        camera_container.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        camera_header = tk.Label(
            camera_container,
            text="📹 LIVE CAMERA - YOLO DETECTION",
            font=("Arial", 12, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            pady=8
        )
        camera_header.pack()
        
        # Canvas for camera feed
        self.camera_canvas = tk.Canvas(
            camera_container,
            width=640,
            height=480,
            bg="black",
            highlightthickness=0
        )
        self.camera_canvas.pack(padx=5, pady=(0, 5))
        
        # Camera controls
        camera_controls = tk.Frame(camera_container, bg=self.dark_secondary)
        camera_controls.pack(fill="x", padx=10, pady=(0, 10))
        
        self.start_camera_btn = tk.Button(
            camera_controls,
            text="📹 Start Camera",
            command=self.start_camera,
            bg=self.success_color,
            fg=self.dark_fg,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.start_camera_btn.pack(side="left", padx=5)
        
        self.stop_camera_btn = tk.Button(
            camera_controls,
            text="⏸ Stop Camera",
            command=self.stop_camera,
            bg=self.error_color,
            fg=self.dark_fg,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_camera_btn.pack(side="left", padx=5)
        
        self.detect_btn = tk.Button(
            camera_controls,
            text="🎯 Capture & Detect",
            command=self.capture_and_detect,
            bg=self.dark_accent,
            fg=self.dark_fg,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.detect_btn.pack(side="left", padx=5)
        
        # ===== RIGHT SIDE: CONTROL PANEL =====
        control_panel = tk.Frame(main_container, bg=self.dark_bg)
        control_panel.grid(row=1, column=1, sticky="nsew")
        
        # Connection Section
        connection_frame = tk.LabelFrame(
            control_panel,
            text=" Robot Connection ",
            font=("Arial", 11, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        connection_frame.pack(fill="x", pady=(0, 10))
        
        ip_frame = tk.Frame(connection_frame, bg=self.dark_secondary)
        ip_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            ip_frame,
            text="IP Address:",
            font=("Arial", 9),
            bg=self.dark_secondary,
            fg=self.dark_fg
        ).pack(anchor="w")
        
        self.ip_entry = tk.Entry(
            ip_frame,
            font=("Arial", 10),
            bg=self.dark_bg,
            fg=self.dark_fg,
            insertbackground=self.dark_fg,
            relief=tk.FLAT,
            width=25
        )
        self.ip_entry.pack(fill="x", pady=(5, 10))
        self.ip_entry.insert(0, self.robot_ip)
        
        self.connect_btn = tk.Button(
            connection_frame,
            text="🔗 Connect Robot",
            command=self.connect_robot,
            bg=self.dark_accent,
            fg=self.dark_fg,
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.connect_btn.pack(padx=10, pady=(0, 5))
        
        self.connection_status = tk.Label(
            connection_frame,
            text="● Not Connected",
            font=("Arial", 9, "bold"),
            bg=self.dark_secondary,
            fg=self.error_color
        )
        self.connection_status.pack(pady=(0, 10))
        
        # Detection Results Section
        results_frame = tk.LabelFrame(
            control_panel,
            text=" Detection Results ",
            font=("Arial", 11, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        results_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Good pieces
        good_frame = tk.Frame(results_frame, bg=self.dark_bg, relief=tk.RAISED, borderwidth=1)
        good_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            good_frame,
            text="🟢 GOOD Pieces",
            font=("Arial", 10, "bold"),
            bg=self.dark_bg,
            fg=self.success_color
        ).pack(pady=5)
        
        self.good_count_label = tk.Label(
            good_frame,
            text="0",
            font=("Arial", 32, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        )
        self.good_count_label.pack()
        
        self.good_list_label = tk.Label(
            good_frame,
            text="None detected",
            font=("Arial", 8),
            bg=self.dark_bg,
            fg="#888888",
            wraplength=300
        )
        self.good_list_label.pack(pady=(0, 10))
        
        # Bad pieces
        bad_frame = tk.Frame(results_frame, bg=self.dark_bg, relief=tk.RAISED, borderwidth=1)
        bad_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            bad_frame,
            text="🔴 BAD Pieces",
            font=("Arial", 10, "bold"),
            bg=self.dark_bg,
            fg=self.error_color
        ).pack(pady=5)
        
        self.bad_count_label = tk.Label(
            bad_frame,
            text="0",
            font=("Arial", 32, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        )
        self.bad_count_label.pack()
        
        self.bad_list_label = tk.Label(
            bad_frame,
            text="None detected",
            font=("Arial", 8),
            bg=self.dark_bg,
            fg="#888888",
            wraplength=300
        )
        self.bad_list_label.pack(pady=(0, 10))
        
        # Sorting Section
        sorting_frame = tk.LabelFrame(
            control_panel,
            text=" Sorting Control ",
            font=("Arial", 11, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        sorting_frame.pack(fill="x", pady=(0, 10))
        
        self.sort_btn = tk.Button(
            sorting_frame,
            text="▶️ START SORTING",
            command=self.start_sorting,
            bg=self.success_color,
            fg=self.dark_fg,
            font=("Arial", 12, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.sort_btn.pack(padx=10, pady=10)
        
        # Progress
        self.progress_label = tk.Label(
            sorting_frame,
            text="0/0 pieces sorted",
            font=("Arial", 9),
            bg=self.dark_secondary,
            fg="#888888"
        )
        self.progress_label.pack(pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            sorting_frame,
            mode='determinate',
            length=300,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(padx=10, pady=(0, 10))
        
        # Activity Log
        log_frame = tk.LabelFrame(
            control_panel,
            text=" Activity Log ",
            font=("Arial", 9, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        log_frame.pack(fill="both", expand=True)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=self.dark_bg,
            fg=self.dark_fg,
            font=("Courier New", 8),
            relief=tk.FLAT,
            yscrollcommand=log_scroll.set,
            state=tk.DISABLED
        )
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        log_scroll.config(command=self.log_text.yview)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.dark_bg,
            background=self.dark_accent,
            thickness=15
        )
    
    def log_message(self, message, level="INFO"):
        """Add message to activity log."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        
        if level == "SUCCESS":
            prefix = "✅"
        elif level == "ERROR":
            prefix = "❌"
        elif level == "WARNING":
            prefix = "⚠️"
        else:
            prefix = "ℹ️"
        
        log_entry = f"[{timestamp}] {prefix} {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def adjust_brightness_contrast(self, frame):
        """Adjust brightness and contrast of frame."""
        return cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)
    
    def find_camera(self):
        """Find available camera - handles both Windows and Linux."""
        # Detect operating system
        os_name = platform.system()
        self.log_message(f"Detected OS: {os_name}")
        
        # Set camera backend based on OS
        if os_name == "Windows":
            backend = cv2.CAP_DSHOW  # DirectShow for Windows
            camera_order = [1, 0, 2, 3]  # Try USB first on Windows
            self.log_message("Using DirectShow backend (Windows)")
        else:  # Linux, Darwin (macOS), etc.
            backend = cv2.CAP_V4L2 if os_name == "Linux" else cv2.CAP_ANY
            camera_order = [0, 1, 2, 3]  # Try index 0 first on Linux
            self.log_message(f"Using {'V4L2' if os_name == 'Linux' else 'default'} backend (Linux/Unix)")
        
        # Try to open camera with detected backend
        for i in camera_order:
            try:
                self.log_message(f"Trying camera index {i}...")
                cap = cv2.VideoCapture(i, backend)
                if cap.isOpened():
                    # Test if we can actually read a frame
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        self.log_message(f"Camera found at index {i}", "SUCCESS")
                        return cap, i
                cap.release()
            except Exception as e:
                self.log_message(f"Error testing camera {i}: {e}", "WARNING")
                continue
        
        self.log_message("No camera found", "ERROR")
        return None, -1
    
    def start_camera(self):
        """Start camera feed with YOLO detection."""
        if self.camera_running:
            return
        
        self.log_message("Starting camera...")
        
        # Load YOLO model
        try:
            self.model = YOLO(self.model_path)
            self.log_message("YOLO model loaded", "SUCCESS")
        except Exception as e:
            self.log_message(f"Failed to load YOLO model: {e}", "ERROR")
            messagebox.showerror("Error", f"Failed to load YOLO model:\n{e}")
            return
        
        # Find and open camera
        self.cap, camera_id = self.find_camera()
        
        if self.cap is None:
            self.log_message("No camera found", "ERROR")
            messagebox.showerror("Error", "No camera detected")
            return
        
        self.camera_running = True
        self.start_camera_btn.config(state=tk.DISABLED)
        self.stop_camera_btn.config(state=tk.NORMAL)
        self.detect_btn.config(state=tk.NORMAL)
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_camera(self):
        """Stop camera feed."""
        self.camera_running = False
        if self.cap:
            self.cap.release()
        self.start_camera_btn.config(state=tk.NORMAL)
        self.stop_camera_btn.config(state=tk.DISABLED)
        self.detect_btn.config(state=tk.DISABLED)
        self.log_message("Camera stopped")
    
    def get_centroid(self, box):
        """Calculate centroid of detection box."""
        x1, y1, x2, y2 = box.xyxy[0]
        return (float((x1 + x2) / 2), float((y1 + y2) / 2))
    
    def match_detection(self, centroid, threshold=50):
        """Match detection to existing piece or create new one."""
        best_match = None
        best_distance = threshold
        
        for tracked_centroid, piece_id in self.piece_tracker.items():
            dist = ((centroid[0] - tracked_centroid[0])**2 + 
                   (centroid[1] - tracked_centroid[1])**2) ** 0.5
            
            if dist < best_distance:
                best_distance = dist
                best_match = (tracked_centroid, piece_id)
        
        if best_match:
            old_centroid, piece_id = best_match
            del self.piece_tracker[old_centroid]
            self.piece_tracker[centroid] = piece_id
            return piece_id
        
        new_piece_id = self.next_piece_id
        self.next_piece_id += 1
        self.piece_tracker[centroid] = new_piece_id
        return new_piece_id
    
    def camera_loop(self):
        """Main camera loop with YOLO detection using fixed regions."""
        while self.camera_running:
            ret, frame = self.cap.read()
            if not ret:
                self.log_message("Failed to read frame", "ERROR")
                break
            
            # Adjust image
            frame = self.adjust_brightness_contrast(frame)
            
            # Run YOLO detection on full frame
            results = self.model(frame, conf=self.conf_thresh, verbose=False)
            
            # For each fixed piece region, check if there's a BAD detection inside
            for piece_id, (rx1, ry1, rx2, ry2) in self.piece_regions.items():
                # Default status is GOOD
                status = "GOOD"
                piece_centroid = ((rx1 + rx2) / 2, (ry1 + ry2) / 2)
                
                # Check if any YOLO detection (BAD class) falls within this region
                if results and len(results) > 0:
                    boxes = results[0].boxes
                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            bx1, by1, bx2, by2 = box.xyxy[0]
                            box_center_x = (float(bx1) + float(bx2)) / 2
                            box_center_y = (float(by1) + float(by2)) / 2
                            
                            # Check if detection center is inside this piece region
                            if rx1 <= box_center_x <= rx2 and ry1 <= box_center_y <= ry2:
                                cls_id = int(box.cls[0])
                                if cls_id == 0:  # BAD class
                                    status = "BAD"
                                    break
                
                # Store piece status
                self.detected_pieces[piece_id] = {
                    "status": status,
                    "centroid": piece_centroid
                }
                
                # Draw region box
                color = (0, 0, 255) if status == "BAD" else (0, 255, 0)
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), color, 3)
                
                # Draw label
                label = f"Piece {piece_id}: {status}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.rectangle(frame, (rx1, ry1 - label_size[1] - 10), 
                            (rx1 + label_size[0], ry1), color, -1)
                cv2.putText(frame, label, (rx1, ry1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Convert frame for tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (640, 480))
            img = Image.fromarray(frame_resized)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update canvas
            self.camera_canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.camera_canvas.image = imgtk
            
            time.sleep(0.03)  # ~30 FPS
    
    def capture_and_detect(self):
        """Capture current frame and finalize detection."""
        if not self.detected_pieces:
            messagebox.showwarning("No Detection", "No pieces detected yet. Wait for detections to appear.")
            return
        
        # Separate good and bad pieces
        self.good_pieces = [pid for pid, data in self.detected_pieces.items() if data["status"] == "GOOD"]
        self.bad_pieces = [pid for pid, data in self.detected_pieces.items() if data["status"] == "BAD"]
        
        # Sort IDs numerically to maintain spatial order (critical for server positioning)
        self.good_pieces.sort()
        self.bad_pieces.sort()
        
        # Update UI
        self.good_count_label.config(text=str(len(self.good_pieces)))
        self.bad_count_label.config(text=str(len(self.bad_pieces)))
        
        if self.good_pieces:
            good_list = ", ".join([str(p) for p in self.good_pieces])
            self.good_list_label.config(text=f"Pieces: {good_list}")
        else:
            self.good_list_label.config(text="None detected")
        
        if self.bad_pieces:
            bad_list = ", ".join([str(p) for p in self.bad_pieces])
            self.bad_list_label.config(text=f"Pieces: {bad_list}")
        else:
            self.bad_list_label.config(text="None detected")
        
        self.log_message(f"Detected: {len(self.good_pieces)} good, {len(self.bad_pieces)} bad", "SUCCESS")
        
        # Enable sorting if robot is connected
        if self.is_connected:
            self.sort_btn.config(state=tk.NORMAL)
    
    def connect_robot(self):
        """Connect to robot server."""
        self.robot_ip = self.ip_entry.get().strip()
        
        if not self.robot_ip:
            messagebox.showerror("Error", "Please enter IP address")
            return
        
        self.log_message(f"Connecting to robot at {self.robot_ip}...")
        self.connect_btn.config(state=tk.DISABLED, text="Connecting...")
        
        def connect_thread():
            try:
                self.robot_client = RobotClient(self.robot_ip)
                
                if self.robot_client.connect():
                    self.is_connected = True
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, self.on_connection_failed)
            except Exception as e:
                self.root.after(0, lambda: self.on_connection_error(str(e)))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connection_success(self):
        """Handle successful connection."""
        self.log_message("Connected to robot!", "SUCCESS")
        self.connection_status.config(text="● Connected", fg=self.success_color)
        self.connect_btn.config(text="Disconnect", state=tk.NORMAL, command=self.disconnect_robot)
        
        # Move to home
        try:
            response = self.robot_client.move_home()
            if response and response.get("status") == "success":
                self.log_message("Robot at home position", "SUCCESS")
        except Exception as e:
            self.log_message(f"Error moving home: {e}", "ERROR")
        
        # Enable sorting if pieces detected
        if self.good_pieces or self.bad_pieces:
            self.sort_btn.config(state=tk.NORMAL)
    
    def on_connection_failed(self):
        """Handle connection failure."""
        self.log_message("Connection failed", "ERROR")
        self.connect_btn.config(state=tk.NORMAL, text="🔗 Connect Robot")
        messagebox.showerror("Error", "Could not connect to robot")
    
    def on_connection_error(self, error):
        """Handle connection error."""
        self.log_message(f"Connection error: {error}", "ERROR")
        self.connect_btn.config(state=tk.NORMAL, text="🔗 Connect Robot")
        messagebox.showerror("Error", f"Connection error:\n{error}")
    
    def disconnect_robot(self):
        """Disconnect from robot."""
        if self.robot_client:
            self.robot_client.disconnect()
        self.is_connected = False
        self.log_message("Disconnected from robot")
        self.connection_status.config(text="● Not Connected", fg=self.error_color)
        self.connect_btn.config(text="🔗 Connect Robot", command=self.connect_robot)
        self.sort_btn.config(state=tk.DISABLED)
    
    def start_sorting(self):
        """Start automated sorting process."""
        if not self.is_connected:
            messagebox.showerror("Error", "Robot not connected")
            return
        
        if not self.good_pieces and not self.bad_pieces:
            messagebox.showwarning("No Pieces", "No pieces to sort")
            return
        
        self.is_sorting = True
        self.sort_btn.config(state=tk.DISABLED)
        self.total_pieces = len(self.good_pieces) + len(self.bad_pieces)
        self.processed_pieces = 0
        self.progress_bar['maximum'] = self.total_pieces
        self.progress_bar['value'] = 0
        
        self.log_message(f"Starting sorting of {self.total_pieces} pieces...")
        self.log_message(f"BAD pieces (in order): {self.bad_pieces}")
        self.log_message(f"GOOD pieces (in order): {self.good_pieces}")
        
        def sorting_thread():
            try:
                # Sort BAD pieces one by one (in numerical ID order)
                for piece_id in self.bad_pieces:
                    success = self.pick_and_place(piece_id, "bad bin", "BAD")
                    if success:
                        # Return to home after each piece
                        self.return_to_home()
                    time.sleep(0.5)
                
                # Sort GOOD pieces one by one
                for piece_id in self.good_pieces:
                    success = self.pick_and_place(piece_id, "good bin", "GOOD")
                    if success:
                        # Return to home after each piece
                        self.return_to_home()
                    time.sleep(0.5)
                
                self.root.after(0, self.on_sorting_complete)
            except Exception as e:
                self.root.after(0, lambda: self.on_sorting_error(str(e)))
        
        threading.Thread(target=sorting_thread, daemon=True).start()
    
    def pick_and_place(self, piece_id, bin_name, status_type):
        """Pick and place a single piece using exact functions from client_example."""
        # Map visual ID to robot ID
        robot_piece_id = self.robot_id_map.get(piece_id, piece_id)
        piece_name = f"piece {robot_piece_id}"
        
        # PICK PIECE - Using exact function from client_example
        self.root.after(0, lambda: self.log_message(f"Picking {status_type} piece {piece_id} (robot ID: {robot_piece_id})..."))
        try:
            response = self.robot_client.pick_piece(piece_name)
            
            if response is None or response.get("status") != "success":
                self.root.after(0, lambda: self.log_message(f"Failed to pick piece {piece_id}", "ERROR"))
                self.processed_pieces += 1
                self.root.after(0, self.update_progress)
                return False
            
            time.sleep(0.5)
            
            # PLACE PIECE - Using exact function from client_example
            self.root.after(0, lambda: self.log_message(f"Placing piece {piece_id} in {bin_name}..."))
            response = self.robot_client.place_piece(bin_name)
            
            if response is None or response.get("status") != "success":
                self.root.after(0, lambda: self.log_message(f"Failed to place piece {piece_id}", "ERROR"))
                self.processed_pieces += 1
                self.root.after(0, self.update_progress)
                return False
            else:
                self.root.after(0, lambda: self.log_message(f"Piece {piece_id} sorted successfully!", "SUCCESS"))
            
            self.processed_pieces += 1
            self.root.after(0, self.update_progress)
            return True
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error processing piece {piece_id}: {e}", "ERROR"))
            self.processed_pieces += 1
            self.root.after(0, self.update_progress)
            return False
    
    def return_to_home(self):
        """Return robot to home position."""
        self.root.after(0, lambda: self.log_message("Returning to home..."))
        try:
            response = self.robot_client.move_home()
            if response and response.get("status") == "success":
                self.root.after(0, lambda: self.log_message("Returned to home", "SUCCESS"))
            else:
                self.root.after(0, lambda: self.log_message("Failed to return home", "WARNING"))
            time.sleep(0.5)
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Error returning home: {e}", "ERROR"))
    
    def update_progress(self):
        """Update progress bar."""
        self.progress_bar['value'] = self.processed_pieces
        self.progress_label.config(text=f"{self.processed_pieces}/{self.total_pieces} pieces sorted")
        self.root.update()
    
    def on_sorting_complete(self):
        """Handle sorting completion."""
        self.is_sorting = False
        self.log_message("Sorting complete! All pieces processed.", "SUCCESS")
        
        self.sort_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Complete", f"Successfully sorted {self.processed_pieces} of {self.total_pieces} pieces!")
    
    def on_sorting_error(self, error):
        """Handle sorting error."""
        self.is_sorting = False
        self.sort_btn.config(state=tk.NORMAL)
        self.log_message(f"Sorting error: {error}", "ERROR")
        messagebox.showerror("Error", f"Sorting error:\n{error}")
    
    def run(self):
        """Start the dashboard."""
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (550)
        y = (self.root.winfo_screenheight() // 2) - (325)
        self.root.geometry(f"+{x}+{y}")
        
        self.log_message("Dashboard initialized")
        self.log_message("Start camera to begin detection")
        
        self.root.mainloop()
        
        # Cleanup
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


def main():
    """Main entry point."""
    dashboard = SortingDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
