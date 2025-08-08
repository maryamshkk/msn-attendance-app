# MSN Global IT - Attendance System

A cloud-based employee attendance management system built with Streamlit.

## 🚀 Features

- **Secure Login System** - Manager authentication
- **Manual Attendance Marking** - Mark present/late for employees
- **CSV Employee Upload** - Upload employee data via CSV
- **Excel Report Generation** - Generate styled attendance reports
- **Monthly Reports** - Create comprehensive monthly summaries
- **Data Export** - Export attendance data as CSV
- **Real-time Dashboard** - Live attendance statistics

## 📋 Requirements

- Python 3.8+
- Streamlit
- Pandas
- OpenPyXL
- Plotly

## 🏗️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd prediction_system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app/cloud_attendance_system.py
   ```

## ☁️ Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit for cloud deployment"
   git push origin main
   ```

2. **Ensure your repository structure:**
   ```
   prediction_system/
   ├── streamlit_app/
   │   └── cloud_attendance_system.py
   ├── requirements.txt
   ├── assets/
   │   └── logo.png
   └── README.md
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Select your repository
   - Set **Main file path:** `streamlit_app/cloud_attendance_system.py`
   - Click "Deploy"

3. **Wait for Deployment:**
   - Streamlit will automatically install dependencies
   - Your app will be available at a public URL

## 🔐 Default Credentials

- **Username:** `msnglobalit`
- **Password:** `msnglobalit123`

## 📁 File Structure

```
prediction_system/
├── streamlit_app/
│   ├── cloud_attendance_system.py    # Main cloud app
│   └── complete_attendance_system.py # Local app with face recognition
├── assets/
│   └── logo.png                      # Company logo
├── requirements.txt                   # Python dependencies
└── README.md                         # This file
```

## 🔧 Configuration

### Environment Variables (Optional)
- No environment variables required for basic deployment
- Data is stored locally in the `excels/` directory

### Customization
- **Logo:** Replace `assets/logo.png` with your company logo
- **Colors:** Modify CSS in the app for custom branding
- **Employees:** Upload CSV with Employee ID and Name columns

## 📊 Features Overview

### Dashboard
- Real-time attendance statistics
- Today's present/late/absent counts
- Quick action buttons for common tasks

### Manual Attendance
- Select employee from dropdown
- Mark as Present or Late
- Prevents duplicate entries per day

### Reports
- **Generate Report:** Creates styled Excel report
- **Monthly Report:** Employee-wise monthly summary
- **Export Data:** Download today's attendance as CSV

### Data Management
- **Clear Entries:** Remove today's attendance data
- **CSV Upload:** Update employee list via CSV file
- **Auto Refresh:** Toggle automatic data refresh

## 🚨 Important Notes

1. **Cloud Limitations:**
   - Face recognition features removed for cloud compatibility
   - Only manual attendance marking available
   - Data stored in temporary cloud storage

2. **Data Persistence:**
   - Data may be reset on app restart
   - Consider using cloud databases for production

3. **Security:**
   - Change default credentials for production use
   - Implement proper authentication for sensitive data

## 🆘 Troubleshooting

### Common Issues:

1. **App won't deploy:**
   - Check `requirements.txt` has all dependencies
   - Ensure main file path is correct
   - Verify Python version compatibility

2. **Import errors:**
   - All imports are standard libraries
   - No custom modules required

3. **File not found errors:**
   - App creates necessary directories automatically
   - Default employee data is generated if missing

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit Cloud documentation
3. Ensure all files are properly committed to GitHub

---

**Built with ❤️ for MSN Global IT Solutions** 