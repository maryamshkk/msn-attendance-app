import sys, os, cv2, json, pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
import face_recognition
import time
import uuid

class SimpleFaceApp(QWidget):
    def __init__(self):
        super().__init__()

        # Setup
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.shared_dir = os.path.join(self.base_dir, "shared")
        self.emp_csv_path = os.path.join(self.shared_dir, "employees_data.csv")
        self.json_file = os.path.join(self.shared_dir, "recognized_id.json")

        os.makedirs(self.shared_dir, exist_ok=True)

        # Load employees and faces
        self.employees = self.load_employees()
        self.known_faces = []
        self.known_ids = []
        self.last_known_face_files = set()
        self.known_faces, self.known_ids = self.load_faces()
        self.last_known_face_files = set(f for f in os.listdir(os.path.join(self.base_dir, "shared", "known_face")) if f.lower().endswith(('.jpg', '.jpeg')))
        # Track file/folder modification times
        self.last_csv_mtime = os.path.getmtime(self.emp_csv_path) if os.path.exists(self.emp_csv_path) else 0
        self.known_dir = os.path.join(self.base_dir, "..", "known_face")
        self.last_known_dir_mtime = self.get_known_dir_mtime()
        # Recognition tracking - improved duplicate prevention
        self.last_recognition_time = 0
        self.recognition_cooldown = 5.0  # Increased to 5 seconds
        self.last_recognized_id = None
        self.recognition_count = {}  # Track recognition count per person
        self.max_recognition_per_person = 3  # Max recognitions per person per session

        # UI
        self.setWindowTitle("Simple Face Recognition")
        self.setFixedSize(600, 400)
        self.init_ui()

        # Camera
        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        # Timer for checking updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(5000)  # Check every 5 seconds
        # Frame skip for optimization
        self.frame_count = 0
        self.process_every_n_frames = 2  # Only process every 2nd frame

        self.watch_timer = QTimer()
        self.watch_timer.timeout.connect(self.watch_known_face_folder)
        self.watch_timer.start(3000)  # Check every 3 seconds

    def load_employees(self):
        employees = {}
        try:
            if os.path.exists(self.emp_csv_path):
                df = pd.read_csv(self.emp_csv_path)
                for _, row in df.iterrows():
                    emp_id = str(row['Employee ID']).strip().upper()
                    name = str(row['Name']).strip()
                    employees[emp_id] = name
        except:
            employees = {"MSN001": "Ramsha Tariq", "MSN002": "Tehreem Siddiqui"}
        return employees

    def load_faces(self):
        faces, ids = [], []
        known_dir = os.path.join(self.base_dir, "shared", "known_face")
        for fname in os.listdir(known_dir):
            if fname.lower().endswith(('.jpg', '.jpeg')):
                emp_id = os.path.splitext(fname)[0].strip().upper()
                face_path = os.path.join(known_dir, fname)
                try:
                    image = face_recognition.load_image_file(face_path)
                    encodings = face_recognition.face_encodings(image)
                    num_faces = len(encodings)
                    if num_faces == 1:
                        faces.append(encodings[0])
                        ids.append(emp_id)
                    elif num_faces > 1:
                        faces.append(encodings[0])
                        ids.append(emp_id)
                    # else: do nothing if no face
                except Exception as e:
                    pass
        return faces, ids

    def get_known_dir_mtime(self):
        try:
            return max(os.path.getmtime(os.path.join(self.known_dir, f)) for f in os.listdir(self.known_dir) if f.endswith('.jpg'))
        except:
            return 0

    def check_for_updates(self):
        # Check if CSV or known_face folder has changed
        csv_mtime = os.path.getmtime(self.emp_csv_path) if os.path.exists(self.emp_csv_path) else 0
        known_dir_mtime = self.get_known_dir_mtime()
        if csv_mtime != self.last_csv_mtime or known_dir_mtime != self.last_known_dir_mtime:
            self.last_csv_mtime = csv_mtime
            self.last_known_dir_mtime = known_dir_mtime
            self.employees = self.load_employees()
            self.known_faces, self.known_ids = self.load_faces()
            self.status_label.setText("🔄 Employees/faces reloaded!")

    def encode_and_add_face(self, face_path, emp_id):
        try:
            image = face_recognition.load_image_file(face_path)
            encodings = face_recognition.face_encodings(image)
            num_faces = len(encodings)
            if num_faces >= 1:
                self.known_faces.append(encodings[0])
                self.known_ids.append(emp_id)
                self.status_label.setText(f"✅ New encoding added for {emp_id}")
            # else: do nothing if no face
        except Exception as e:
            pass

    def watch_known_face_folder(self):
        # Watch for new images in known_face and encode only new ones
        known_dir = os.path.join(self.base_dir, "shared", "known_face")
        current_files = set(f for f in os.listdir(known_dir) if f.lower().endswith(('.jpg', '.jpeg')))
        if not hasattr(self, 'last_known_face_files'):
            self.last_known_face_files = set()
        new_files = current_files - self.last_known_face_files
        if new_files:
            for fname in new_files:
                emp_id = os.path.splitext(fname)[0].strip().upper()
                face_path = os.path.join(known_dir, fname)
                self.encode_and_add_face(face_path, emp_id)
            self.last_known_face_files = current_files
        # Also handle removed files (optional: clear encodings if file is deleted)
        removed_files = self.last_known_face_files - current_files
        if removed_files:
            self.last_known_face_files = current_files

    def init_ui(self):
        # Title
        title = QLabel("SIMPLE FACE RECOGNITION", alignment=Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: red; background-color: black; padding: 10px; border: 2px solid red;")

        # Image display
        self.image_label = QLabel()
        self.image_label.setFixedSize(500, 300)
        self.image_label.setStyleSheet("border: 2px solid red; background-color: black;")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Status
        self.status_label = QLabel("Ready to start...", alignment=Qt.AlignCenter)
        self.status_label.setStyleSheet("color: white; background-color: #111; padding: 8px; border: 1px solid red;")

        # Buttons
        self.start_btn = QPushButton("📹 Start Camera")
        self.stop_btn = QPushButton("⏹️ Stop Camera")

        button_style = """
            QPushButton {
                background-color: #DC143C; color: white; border: 2px solid #DC143C;
                border-radius: 8px; padding: 10px; font-weight: bold; font-size: 12px;
                min-width: 120px; min-height: 40px;
            }
            QPushButton:hover { background-color: #B22222; border-color: #B22222; }
        """
        self.start_btn.setStyleSheet(button_style)
        self.stop_btn.setStyleSheet(button_style)

        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn.clicked.connect(self.stop_camera)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.setStyleSheet("QWidget { background-color: #000000; color: white; }")

    def start_camera(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened():
            self.timer.start(30)
            self.status_label.setText("Camera started")
        else:
            self.status_label.setText("❌ Cannot open camera!")

    def stop_camera(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.capture:
            self.capture.release()
            self.capture = None
        self.image_label.clear()
        self.status_label.setText("Camera stopped")

    def update_frame(self):
        if not self.capture:
            return
        ret, frame = self.capture.read()
        if not ret or frame is None:
            return
        self.frame_count += 1
        if self.frame_count % self.process_every_n_frames != 0:
            qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            return
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations and self.known_faces:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            current_time = time.time()
            for face_encoding in face_encodings:
                face_distances = face_recognition.face_distance(self.known_faces, face_encoding)
                best_match_index = face_distances.argmin()
                best_distance = face_distances[best_match_index]
                best_id = self.known_ids[best_match_index]
                if best_distance < 0.6 and (current_time - self.last_recognition_time) > self.recognition_cooldown:
                    emp_id = best_id
                    name = self.employees.get(emp_id, "Unknown")
                    if self.is_attendance_already_marked(emp_id):
                        self.status_label.setText(f"⚠️ {emp_id} ({name}) - Already marked today! (Distance: {best_distance:.3f})")
                        self.last_recognition_time = current_time
                        break
                    if emp_id not in self.recognition_count:
                        self.recognition_count[emp_id] = 0
                    if self.recognition_count[emp_id] < self.max_recognition_per_person:
                        success = self.save_recognition(emp_id, name)
                        if success:
                            self.last_recognized_id = emp_id
                            self.last_recognition_time = current_time
                            self.recognition_count[emp_id] += 1
                            self.status_label.setText(f"✅ ATTENDANCE MARKED: {emp_id} ({name}) - {datetime.now().strftime('%H:%M')} (Distance: {best_distance:.3f})")
                        else:
                            self.status_label.setText(f"❌ Failed to mark attendance for {emp_id} (Distance: {best_distance:.3f})")
                        break
                    else:
                        self.status_label.setText(f"⚠️ {emp_id} already recognized {self.max_recognition_per_person} times (Distance: {best_distance:.3f})")
                else:
                    self.status_label.setText(f"👤 Face detected - Best match: {best_id}, Distance: {best_distance:.3f} (not recognized)")
        else:
            self.status_label.setText("Live detection active")
        qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def is_attendance_already_marked(self, emp_id):
        """Check if attendance is already marked for this employee today"""
        try:
            # Check if JSON file exists and has entries for today
            if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        today = datetime.now().strftime('%Y-%m-%d')
                        for entry in data:
                            if entry.get('employee_id') == emp_id:
                                entry_timestamp = entry.get('timestamp', '')
                                if entry_timestamp:
                                    try:
                                        entry_date = datetime.fromisoformat(entry_timestamp).strftime('%Y-%m-%d')
                                        if entry_date == today:
                                            return True
                                    except:
                                        pass
            return False
        except Exception as e:
            return False

    def save_recognition(self, emp_id, name):
        try:
            # Generate unique ID with timestamp and UUID
            timestamp = datetime.now()
            unique_id = f"{emp_id}_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}_{str(uuid.uuid4())[:8]}"
            data = {
                "employee_id": emp_id,
                "name": name,
                "timestamp": timestamp.isoformat(),
                "status": "recognized",
                "unique_id": unique_id
            }
            existing = []
            if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                try:
                    with open(self.json_file, 'r') as f:
                        existing = json.load(f)
                        if not isinstance(existing, list):
                            existing = [existing]
                except:
                    existing = []
            existing.append(data)
            with open(self.json_file, 'w') as f:
                json.dump(existing, f, indent=2)
            return True
        except Exception as e:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleFaceApp()
    window.show()
    sys.exit(app.exec_())