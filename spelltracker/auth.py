import hashlib
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

# --- Google Sheet Setup ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_NAME = "DnDSpellTrackerUsers"  
SHEET_ID = "1TOTnHOEv0Kx_8rVUCH7PpZRtq1NenVk13f9jOO8fjr4" 


# Dynamically find path to credentials
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# --- Hash password ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# --- Register new user ---
def register_user(username, password):
    existing = sheet.col_values(1)
    if username in existing:
        return False, "Username already exists."
    
    hashed = hash_password(password)
    sheet.append_row([username, hashed])
    return True, "Account created!"


# --- Login user ---
def login_user(username, password):
    users = sheet.get_all_records()
    entered_hash = hash_password(password)
    print(f"Entered username: {username}")
    print(f"Entered password hash: {entered_hash}")

    for user in users:
        print("Row from sheet:", user)
        if user.get("username") == username:
            print(f"Comparing with stored hash: {user.get('password_hash')}")
            if user.get("password_hash") == entered_hash:
                print("✅ Hashes match — login success")
                
                return True
            else:
                print("❌ Hashes don't match")
    return False