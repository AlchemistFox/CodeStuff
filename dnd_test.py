import streamlit as st
import random

st.markdown(
    """
    <style>
    /* Change the whole page background */
    .css-1d391kg {
        background-color: #013220 !important;
    }
    /* Change main content background */
    .css-18e3th9 {
        background-color: #013220 !important;
    }
    /* Change sidebar background (if you use one) */
    .css-1v3fvcr {
        background-color: #013220 !important;
    }
    /* Change text color */
    .stText, .stMarkdown, .stButton>button {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set up session state for roll history
if "roll_history" not in st.session_state:
    st.session_state.roll_history = []

st.title("🎲 D&D D20 Dice Roller")

# Button to roll the die
if st.button("Roll D20"):
    result = random.randint(1, 20)
    st.session_state.roll_history.insert(0, result)  # Add to top
    st.session_state.roll_history = st.session_state.roll_history[:10]  # Keep only last 10

# Show latest result
if st.session_state.roll_history:
    st.subheader(f"🎯 Latest Roll: {st.session_state.roll_history[0]}")

# Show history
if st.session_state.roll_history:
    st.markdown("### 🕒 Last 10 Rolls")
    st.write(st.session_state.roll_history)
