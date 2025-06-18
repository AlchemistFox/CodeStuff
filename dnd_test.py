import streamlit as st
import random

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
