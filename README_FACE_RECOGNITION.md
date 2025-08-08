# MSN Global IT - Face Recognition Attendance System

## 🎯 Overview

This system integrates face recognition with attendance management. The face recognition app detects employees and saves recognition data to JSON, which is then processed by the attendance system.

## 📁 File Structure

```
msn-attendance-app/
├── face_recognition_app/
│   ├── face_recognition_app.py    # Main face recognition app
│   ├── shared/
│   │   └── employees_data.csv     # Employee data
│   └── modules/                   # Data processing modules
├── streamlit_app/
│   └── complete_attendance_system.py  # Main attendance app
├── known_face/                    # Employee face images
│   ├── MSN001.jpg
│   ├── MSN002.jpg
│   └── ...
├── launch_face_recognition.py     # Launcher script
└── README_FACE_RECOGNITION.md     # This file
```

## 🚀 Quick Start

### 1. Start the Attendance System
```bash
cd msn-attendance-app/streamlit_app
streamlit run complete_attendance_system.py
```

### 2. Launch Face Recognition
From the attendance app sidebar:
- Click **"📹 LAUNCH FACE RECOGNITION APP"**
- Or manually run: `python launch_face_recognition.py`

### 3. Use Face Recognition
1. Click **"📹 Start Camera"** in the face recognition app
2. Position your face in front of the camera
3. When recognized, attendance is saved to JSON
4. Return to attendance app and click **"🔄 REFRESH & MARK ATTENDANCE"**

## 🔧 Face Recognition App Features

### ✅ Working Features:
- **Real-time face detection** using OpenCV
- **Face encoding** with face_recognition library
- **Employee matching** with known face database
- **JSON data export** for attendance system integration
- **Manual attendance entry** for testing
- **Camera controls** (start/stop/restart)
- **Status notifications** and error handling

### 📊 Employee Data:
- **MSN001**: Ramsha Tariq
- **MSN002**: Tehreem Siddiqui
- **MSN003**: Maryam Sheikh
- **MSN004**: Samreen Fatima
- **MSN005**: Taskeen Abbas
- **MSN006**: Muhammad Shaf
- **MSN007**: Hammad Hassan
- **MSN008**: Fiaz Bhai

## 🎯 How It Works

### 1. Face Recognition Process:
```
Camera → Face Detection → Face Encoding → Employee Matching → JSON Export
```

### 2. Attendance Integration:
```
JSON Data → Attendance App → Process Recognition → Mark Attendance → Excel Report
```

### 3. Data Flow:
1. **Face Recognition App** detects faces and matches with employee database
2. **Recognition data** is saved to `shared/recognized_id.json`
3. **Attendance App** monitors JSON file for new recognitions
4. **Refresh button** processes new recognitions and marks attendance
5. **Excel reports** are generated with attendance data

## 🔧 Configuration

### Employee Face Images:
- Place employee photos in `known_face/` directory
- Name format: `MSN001.jpg`, `MSN002.jpg`, etc.
- Supported formats: JPG, PNG
- Recommended size: 200x200 pixels or larger

### Employee Data:
- Edit `face_recognition_app/shared/employees_data.csv`
- Format: `Employee ID,Name`
- Example: `MSN001,Ramsha Tariq`

## 🛠️ Troubleshooting

### Common Issues:

1. **Camera not working:**
   - Check camera permissions
   - Try different camera indices (0, 1, 2)
   - Restart the app

2. **Face recognition not working:**
   - Ensure face images are in `known_face/` directory
   - Check image quality and face visibility
   - Verify employee data in CSV file

3. **Attendance not marking:**
   - Check JSON file exists in `shared/` directory
   - Click "🔄 REFRESH & MARK ATTENDANCE" button
   - Verify employee ID matches between apps

4. **Dependencies missing:**
   ```bash
   pip install face-recognition opencv-python PyQt5 pandas numpy
   ```

## 📊 Status Indicators

### Face Recognition Status:
- **🟢 Data Available**: Recognition data ready to process
- **🟡 Waiting for Data**: JSON file exists but empty
- **🔴 Not Connected**: JSON file not found

### Attendance Status:
- **✅ Present**: Employee marked present
- **⚠️ Late**: Employee marked late
- **❌ Absent**: Employee not marked today

## 🎯 Integration Points

### JSON Data Format:
```json
[
  {
    "employee_id": "MSN001",
    "name": "Ramsha Tariq",
    "timestamp": "2024-01-15T10:30:00",
    "status": "recognized",
    "unique_id": "MSN001_20240115_103000_123456"
  }
]
```

### Shared Files:
- `shared/recognized_id.json`: Recognition data
- `shared/employees_data.csv`: Employee database
- `shared/attendance_log.csv`: Attendance records

## 🚀 Advanced Features

### Manual Testing:
- Use **"🧪 Test Recognition"** button for testing
- Use **"✏️ Manual Entry"** for manual attendance marking
- Use **"📊 Check Status"** to verify system status

### Debug Information:
- JSON file status and content
- Recognition timestamps and data
- System error messages and logs

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure file paths and permissions are correct
4. Check camera and face image quality

---

**Built with ❤️ for MSN Global IT Solutions** 