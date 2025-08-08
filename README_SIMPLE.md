# Simple Face Recognition Attendance System

## Quick Start

1. **Start Attendance App:**
   ```bash
   cd streamlit_app
   streamlit run complete_attendance_system.py
   ```

2. **Launch Face Recognition:**
   ```bash
   cd face_recognition_app
   python face_recognition_app.py
   ```

3. **Use Face Recognition:**
   - Click "📹 Start Camera" in face app
   - Position face in camera
   - When recognized, attendance is automatically processed
   - Click "🔄 REFRESH ATTENDANCE" if needed

## Files

- `face_recognition_app/face_recognition_app.py` - Face recognition app
- `streamlit_app/complete_attendance_system.py` - Attendance app
- `known_face/` - Employee photos (MSN001.jpg, etc.)

## Features

- **No duplication** - 3-second cooldown prevents multiple saves
- **Accurate recognition** - Distance-based matching (threshold: 0.6)
- **Auto-processing** - JSON data automatically processed when available
- **Simple interface** - Just start camera and position face

## Dependencies

```bash
pip install face-recognition opencv-python PyQt5 pandas streamlit
```

## Employee Data

Edit `face_recognition_app/shared/employees_data.csv`:
```
Employee ID,Name
MSN001,Ramsha Tariq
MSN002,Tehreem Siddiqui
```

## Face Images

Place employee photos in `known_face/`:
- MSN001.jpg
- MSN002.jpg
- etc. 