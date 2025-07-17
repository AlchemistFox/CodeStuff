import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
import json

# Set up Google Sheets API credentials from st.secrets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Convert st.secrets object to a dict
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

# Open the Google Sheet
SHEET_NAME = "weight_tracker_data"  # Change to match your actual Google Sheet name
sheet = client.open(SHEET_NAME).sheet1

# Load existing data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# If empty or missing headers, initialize with correct structure
if not data or "Date" not in data[0]:
    df = pd.DataFrame(columns=["Date", "Weight"])
else:
    df = pd.DataFrame(data)

st.title("🏋️ Weight Tracker")

# Input today's weight
today = datetime.date.today().isoformat()
weight_input = st.number_input("Enter today's weight (kg):", min_value=0.0, step=0.1)

if st.button("Add today's weight"):
    # Remove any existing entry for today
    df = df[df["Date"] != today]
    df.loc[len(df.index)] = [today, weight_input]

    # Clear sheet and rewrite all rows
    sheet.clear()
    sheet.append_row(["Date", "Weight"])
    for row in df.values.tolist():
        sheet.append_row(row)

    st.success("Weight saved to Google Sheets!")

# Display data table
st.subheader("📅 Weight History")
if not df.empty:
    df_sorted = df.sort_values("Date")
    st.dataframe(df_sorted)

    # Display line chart
    st.subheader("📈 Progress Over Time")
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"])
    df_sorted.set_index("Date", inplace=True)
    st.line_chart(df_sorted["Weight"])
else:
    st.info("No weight data found. Add your first entry above.")
