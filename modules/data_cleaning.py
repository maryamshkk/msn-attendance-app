import pandas as pd
from datetime import datetime, time
import os
import sys
# Append module path
sys.path.append(os.path.abspath('..'))
# from modules.data_cleaning import convert_to_time  # Adjust path if needed

# Global cutoff
cutoff_time = time(10, 30)



# ✅ Calculate late minutes
def get_late_minutes(entry_time, cutoff=cutoff_time):
    if not entry_time:
        return 0
    entry_dt = datetime.combine(datetime.today(), entry_time)
    cutoff_dt = datetime.combine(datetime.today(), cutoff)
    delta = (entry_dt - cutoff_dt).total_seconds() / 60
    return max(0, int(delta))

def clean_realtime_attendance(df_input, employee_df):
    df = df_input.copy()

    # Ensure proper matching with employee master
    df = pd.merge(df, employee_df[['Employee ID', 'Name']], on='Employee ID', how='left')

    # Drop if no match
    df = df.dropna(subset=['Employee ID', 'Name'])

    # Convert time
    df['Entry_Time'] = df['Entry_Time'].apply(convert_to_time)
    df['Late_Min'] = df['Entry_Time'].apply(get_late_minutes)

    # Format time
    df['Entry_Time'] = df['Entry_Time'].apply(lambda t: t.strftime('%H:%M') if pd.notna(t) and t else None)

    # Predict status
    def predict_status(row):
        if not row['Entry_Time']:
            return 'Absent'
        elif row['Late_Min'] > 0:
            return 'Late'
        else:
            return 'Present'

    df['Status'] = df.apply(predict_status, axis=1)

    return df[['Employee ID', 'Name', 'Entry_Time', 'Status']]

# ✅ Save cleaned data to Excel
def save_attendance_to_excel(df_cleaned, folder_path, filename="realtime_attendance.xlsx"):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    df_cleaned.to_excel(file_path, index=False)
    print(f"✅ Saved to {file_path}")

# ✅ Example usage
if __name__ == "__main__":
    # Load raw real-time attendance (e.g., from face recognition output)
    df_input = pd.read_csv("realtime_raw.csv")

    # Load employee master CSV (uploaded custom one)
    employee_df = pd.read_csv("employees_data.csv")

    # Clean and match with employee data
    cleaned_df = clean_realtime_attendance(df_input, employee_df)

    # Save to Excel
    save_attendance_to_excel(cleaned_df, r'C:\Users\Sheikh\Desktop\prediction_system\excels')
