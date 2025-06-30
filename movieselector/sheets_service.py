import gspread
from google.oauth2.service_account import Credentials
import os

# Get the directory where sheets_service.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Compose full path to your service_account.json inside movieselector/
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

# Google Sheets API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Your Google Sheet ID (from the sheet URL)
SPREADSHEET_ID = "1zTFjFDlJhjCfIt2-RNQ7hz-Yk5pfTHihHAiCt14hD3k"  # replace with your actual Sheet ID

def get_sheet():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # default to first sheet
    return sheet

def read_all_records():
    sheet = get_sheet()
    return sheet.get_all_records()

def append_record(row_values):
    sheet = get_sheet()
    sheet.append_row(row_values)

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)