import streamlit as st
import random


# test for testing_12

# Easy to edit list of things.
VERSION = "v0.3"

# Display the version in hte top left corner.
st.markdown(
    f"""
    <style>
    .version-box {{
        position: absolute;
        top: 10px;
        left: 25px;
        background-color: rgba(1, 50, 32, 0.8);
        color: white;
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 14px;
        z-index: 1000;
    }}
    </style>
    <div class="version-box">{VERSION}</div>
    """,
    unsafe_allow_html=True
)

# Try to remove the chunky top-frame.
st.markdown(
    """
    <style>
    /* Reduce vertical spacing at top of page */
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
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
