import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

# --- Sheet Config ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CHAR_SHEET_ID = "1E_9zy74ZfB-SaXxbBpD8E8WnNVzPlqmJbukLsPt5Hys"  # Your actual sheet ID
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(CHAR_SHEET_ID).sheet1


def load_user_characters(username):
    rows = sheet.get_all_records()
    return [row for row in rows if row['username'] == username]


def add_character(username, name, cls, lvl, prof):
    # Adjusted to match new column order: username, character_name, class, level, proficiency_bonus
    sheet.append_row([username, name, cls, lvl, prof])


# --- Main App ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

username = st.session_state.username
st.title(f"🧙 Character Selection for {username}")

chars = load_user_characters(username)

if chars:
    st.subheader("Your Characters:")
    for char in chars:
        if st.button(f"{char['character_name']} ({char['class']} {char['level']})"):
            st.session_state.selected_character = char
            st.switch_page("pages/character_sheet.py")

else:
    st.info("No characters found. Create one below!")

st.divider()
st.subheader("➕ Create New Character")
with st.form("new_character"):
    name = st.text_input("Character Name")
    cls = st.selectbox("Class", ["Wizard", "Fighter", "Cleric", "Rogue", "Bard", "Other"])
    lvl = st.number_input("Level", min_value=1, max_value=20, value=1)
    prof = st.number_input("Proficiency Bonus", min_value=1, max_value=10, value=2)
    submitted = st.form_submit_button("Create")
    if submitted:
        add_character(username, name, cls, lvl, prof)
        st.success(f"Character '{name}' created!")
        st.rerun()
