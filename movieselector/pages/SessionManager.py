# pages/SessionManager.py
import streamlit as st
import sessions
import time

st.set_page_config(page_title="Session Manager", layout="centered")

st.title("Session Manager")

if "user" not in st.session_state:
    st.warning("Please log in to continue.")
    st.stop()

username = st.session_state["user"]

if "session_code" not in st.session_state:
    st.session_state.session_code = ""

st.write(f"Logged in as: **{username}**")

col1, col2 = st.columns(2)

with col1:
    if st.button("Create New Session"):
        code = sessions.create_session(username)
        st.session_state.session_code = code
        st.success(f"Session created! Code: {code}")

with col2:
    join_code = st.text_input("Enter Session Code to Join").upper()
    if st.button("Join Session"):
        if sessions.session_exists(join_code):
            if sessions.add_user_to_session(join_code, username):
                st.session_state.session_code = join_code
                st.success(f"Joined session {join_code}!")
            else:
                st.error("Could not join the session.")
        else:
            st.error("Session code not found.")

if st.session_state.session_code:
    st.write(f"Current session code: **{st.session_state.session_code}**")
    users = sessions.get_users_in_session(st.session_state.session_code)
    if users:
        st.subheader("Users in this session:")
        if st.button("🔄 Refresh User List"):
            st.rerun()

        for u in users:
            st.write(f"- {u}")
    else:
        st.write("No users in this session yet.")

    if st.button("👉 Start Selecting Movies"):
        time.sleep(0.1)
        st.switch_page("pages/MovieSelector.py")