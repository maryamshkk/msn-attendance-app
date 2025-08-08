#!/usr/bin/env python3
import os
import sys
import subprocess

def launch_face_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    face_app_path = os.path.join(current_dir, "face_recognition_app", "face_recognition_app.py")
    
    if os.path.exists(face_app_path):
        print("🚀 Launching Face Recognition App...")
        subprocess.Popen([sys.executable, face_app_path])
        print("✅ Face Recognition App launched!")
    else:
        print("❌ Face recognition app not found!")

if __name__ == "__main__":
    launch_face_app() 