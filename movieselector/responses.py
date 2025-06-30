import gspread
from google.oauth2.service_account import Credentials
import os
from sheets_service import client
import streamlit as st

RESPONSES_SHEET_ID = "13zNplVzwgeOmWRCH6WZb8P7ZEd104wM0m3SDQBAaVUg"  # update if needed

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
RESPONSES_SHEET_ID = "13zNplVzwgeOmWRCH6WZb8P7ZEd104wM0m3SDQBAaVUg"  # Replace if needed

def get_response_sheet():
    return client.open_by_key(RESPONSES_SHEET_ID).sheet1

def log_response(user_id, movie_id, movie_title, response):
    session_code = st.session_state.get("session_code", "")  # <-- NEW
    sheet = get_response_sheet()
    sheet.append_row([user_id, movie_id, movie_title, response, session_code])