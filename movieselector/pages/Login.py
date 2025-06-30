import streamlit as st
import sys
import os
import time

# Fix import path for root-level modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import auth

def login_page():
    st.title("Login or Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if auth.check_login(username, password):
                st.success(f"Welcome back, {username}!")
                st.session_state["user"] = username
                st.query_params["user"] = username
                time.sleep(0.1)
                st.switch_page("pages/SessionManager.py")
            else:
                st.error("Incorrect username or password.")
    with col2:
        if st.button("Register"):
            if auth.register_user(username, password):
                st.success(f"User {username} registered! Please login now.")
            else:
                st.error("Username already exists.")

if __name__ == "__main__":
    login_page()
