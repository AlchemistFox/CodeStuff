import streamlit as st
from auth import login_user, register_user

st.set_page_config(page_title="D&D Spell Tracker", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Login or Register")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Incorrect username or password.")

with tab2:
    new_user = st.text_input("New Username", key="reg_user")
    new_pass = st.text_input("New Password", type="password", key="reg_pass")
    if st.button("Register"):
        success, msg = register_user(new_user, new_pass)
        if success:
            st.success(msg)
        else:
            st.error(msg)

if st.session_state.logged_in:
    st.switch_page("pages/character_select.py")
