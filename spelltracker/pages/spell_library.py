import streamlit as st
import gspread
import json
import os
import re
from google.oauth2.service_account import Credentials
from collections import defaultdict

# --- Google Sheets Setup ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials.json")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SPELL_SHEET_ID = "1ht1OhZi4UWwyeGDMAAuuMxCwCAeLmjWMTM4ivAgpNN0"  # Replace with your sheet ID
spell_sheet = client.open_by_key(SPELL_SHEET_ID).sheet1

# --- Load Character Info ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

character = st.session_state.selected_character
username = st.session_state.username
char_name = character['character_name']
char_class = character['class']

# --- Load Spells ---
with open(os.path.join(os.path.dirname(__file__), "../data/spells.json"), encoding="utf-8") as f:
    all_spells = json.load(f)

# --- Helper Functions ---

def get_spell_level(description: str) -> str:
    """Extracts spell level like 'Cantrip' or 'Level 1' from the description."""
    lines = description.splitlines()
    for line in lines:
        line = line.strip().lower()
        if "cantrip" in line:
            return "Cantrip"
        match = re.search(r"(\d+)(?:st|nd|rd|th)?-level", line)
        if match:
            return f"Level {int(match.group(1))}"
    return "Unknown"

def sort_level_key(level: str):
    """Sort key for spell levels: Cantrip first, then numeric levels, then Unknown last."""
    if level.lower() == "cantrip":
        return 0
    match = re.search(r"\d+", level)
    if match:
        return int(match.group())
    return 99

def spell_matches_class(description, class_name):
    return class_name.lower() in description.lower()

# --- CSS to reduce column width and spacing ---
st.markdown("""
    <style>
        div[data-testid="column"] {
            width: fit-content !important;
            flex: unset;
        }
        div[data-testid="column"] * {
            width: fit-content !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI Controls ---
st.title(f"🧙 Spell Library for {char_name}")
st.caption(f"Class: {char_class}")

show_all = st.checkbox("Show spells from all classes", value=False)

# --- Filter spells by class ---
if not show_all:
    spells = [s for s in all_spells if spell_matches_class(s['description'], char_class)]
else:
    spells = all_spells

# --- Group spells by level ---
spells_by_level = defaultdict(list)
for spell in spells:
    level = get_spell_level(spell['description'])
    spells_by_level[level].append(spell)

# --- Spell Selection State ---
if "selected_spells" not in st.session_state:
    st.session_state.selected_spells = set()

# --- Level counters ---
level_counts = defaultdict(int)

# --- Display spells grouped by level with expanders and tight columns ---
for level in sorted(spells_by_level.keys(), key=sort_level_key):
    with st.expander(f"{level} ({len(spells_by_level[level])} spells)", expanded=False):
        for spell in spells_by_level[level]:
            spell_id = spell["title"]
            selected = spell_id in st.session_state.selected_spells

            cols = st.columns([0.1, 0.6, 0.2], gap="small")

            with cols[0]:
                checkbox = st.checkbox(
                    "Select spell",
                    key=spell_id,
                    value=selected,
                    label_visibility="hidden"
                )
            with cols[1]:
                st.write(spell_id)
            with cols[2]:
                if st.button("Info", key=f"info_btn_{spell_id}"):
                    st.session_state[f"desc_{spell_id}"] = not st.session_state.get(f"desc_{spell_id}", False)

            if checkbox:
                st.session_state.selected_spells.add(spell_id)
                level_counts[level] += 1
            else:
                st.session_state.selected_spells.discard(spell_id)

            if st.session_state.get(f"desc_{spell_id}", False):
                st.markdown(
                    f"<div style='font-size:none; white-space: pre-wrap; padding-left: 20px;'>{spell['description']}</div>",
                    unsafe_allow_html=True
                )

# --- Display selected spell counts by level ---
st.subheader("📊 Spell Level Count")
for lvl, count in sorted(level_counts.items(), key=lambda x: sort_level_key(x[0])):
    st.markdown(f"- **{lvl}:** {count} selected")


# --- Clear and Save buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Clear Selection"):
        st.session_state.selected_spells.clear()
        st.rerun()

with col2:
    if st.button("💾 Save Spells"):
        existing = spell_sheet.get_all_records()
        # Remove existing spells for this user/character
        new_data = [row for row in existing if not (row['username'] == username and row['character_name'] == char_name)]
        spell_sheet.clear()
        spell_sheet.append_row(["username", "character_name", "spell_title", "spell_level", "spell_url"])
        for row in new_data:
            spell_sheet.append_row([row['username'], row['character_name'], row['spell_title'], row['spell_level'], row['spell_url']])

        for spell in all_spells:
            if spell['title'] in st.session_state.selected_spells:
                level = get_spell_level(spell['description'])
                spell_sheet.append_row([username, char_name, spell["title"], level, spell["url"]])
        st.success("✅ Spells saved!")

if st.button("⬅️ Back to Character Sheet"):
    # Clear URL query parameters by assigning empty dict
    st.query_params = {}

    # Switch page by the file name inside pages folder WITHOUT extension or folder path
    st.switch_page("pages/character_sheet.py")
