import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

# Set up Google Sheets API credentials from st.secrets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "weight_tracker_data"
sheet = client.open(SHEET_NAME).sheet1

# Load existing data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# If empty or missing headers, initialize with correct structure
if not data or "Date" not in data[0]:
    df = pd.DataFrame(columns=["Date", "Weight"])

st.title("🏋️ Weight Tracker")

# Input today's weight
today = datetime.date.today().isoformat()
weight_input = st.number_input("Enter today's weight (kg):", min_value=0.0, step=0.1)

if st.button("Add today's weight"):
    df = df[df["Date"] != today]  # Remove any existing entry for today
    df.loc[len(df.index)] = [today, weight_input]
    
    # Clear and rewrite sheet
    sheet.clear()
    sheet.append_row(["Date", "Weight"])
    for row in df.values.tolist():
        sheet.append_row(row)
    
    st.success("Weight saved to Google Sheets!")

# Handle deletion
# Handle confirmed deletion
if "delete_row_confirmed" in st.session_state:
    delete_index = st.session_state["delete_row_confirmed"]
    df = df.drop(index=delete_index).reset_index(drop=True)
    del st.session_state["delete_row_confirmed"]

    # Rewrite sheet
    sheet.clear()
    sheet.append_row(["Date", "Weight"])
    for row in df.values.tolist():
        sheet.append_row(row)
    
    st.success("Entry deleted!")
    st.rerun()

# Display table and delete buttons
st.subheader("📅 Weight History")
if not df.empty:
    df_sorted = df.sort_values("Date").reset_index(drop=True)
    for i, row in df_sorted.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(row["Date"])
        with col2:
            st.write(f'{row["Weight"]} kg')
        with col3:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state["pending_delete"] = i

    # Show confirmation popup if delete was clicked
    if "pending_delete" in st.session_state:
        idx = st.session_state["pending_delete"]
        row = df_sorted.loc[idx]
        st.warning(f"Are you sure you want to delete the entry from **{row['Date']} ({row['Weight']} kg)**?")
        col_confirm, col_cancel = st.columns([1, 1])
        with col_confirm:
            if st.button("✅ Yes, delete it"):
                st.session_state["delete_row_confirmed"] = idx
                del st.session_state["pending_delete"]
                st.rerun()
        with col_cancel:
            if st.button("❌ Cancel"):
                del st.session_state["pending_delete"]
                st.rerun()

    # Chart
    st.subheader("📈 Progress Over Time")
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"])
    df_sorted.set_index("Date", inplace=True)
    st.line_chart(df_sorted["Weight"])
else:
    st.info("No weight data found. Add your first entry above.")
