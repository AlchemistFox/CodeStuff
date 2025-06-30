# sessions.py
import random
import string
from sheets_service import get_sheet

# Your sessions Google Sheet ID (replace with your actual Sheet ID)
SESSIONS_SHEET_ID = "1P7IQIzz1kbZZxM2JZkWQ9thpg61wK7fi_NXm9MhsyR0"

def get_sessions_sheet():
    # Use gspread to open the sessions sheet by key
    from google.oauth2.service_account import Credentials
    import gspread
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SESSIONS_SHEET_ID).sheet1

def generate_session_code(length=6):
    """Generate a random alphanumeric session code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def session_exists(session_code):
    sheet = get_sessions_sheet()
    records = sheet.get_all_records()
    for rec in records:
        if rec.get("session_code") == session_code:
            return True
    return False

def create_session(username):
    sheet = get_sessions_sheet()
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not session_exists(code):
            break

    sheet.append_row([code, username])
    return code


def add_user_to_session(session_code, username):
    """Add a username to an existing session"""
    sheet = get_sessions_sheet()
    records = sheet.get_all_records()
    for idx, rec in enumerate(records, start=2):  # start=2 for header offset
        if rec.get("session_code") == session_code:
            users = rec.get("username", "")
            user_list = users.split(",") if users else []
            if username not in user_list:
                user_list.append(username)
                updated_users = ",".join(user_list)
                sheet.update(f"B{idx}", [[updated_users]])
            return True
    return False  # session not found

def get_users_in_session(code):
    sheet = get_sessions_sheet()
    records = sheet.get_all_values()

    # First row is headers: ['session_code', 'users']
    for row in records[1:]:
        if row[0] == code:
            return row[1].split(",") if len(row) > 1 and row[1] else []

    return []
