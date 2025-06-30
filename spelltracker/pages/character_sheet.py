import streamlit as st
import os

# --- Ensure character is selected ---
if "selected_character" not in st.session_state:
    st.error("No character selected. Please return to the character list.")
    st.stop()

char = st.session_state.selected_character

st.title(f"{char['character_name']} — Level {char['level']} {char['class']}")

# --- Character Summary ---
st.subheader("Character Info")
col1, col2 = st.columns(2)
with col1:
    st.text(f"Class: {char['class']}")
with col2:
    st.text(f"Level: {char['level']}")
    st.text(f"Proficiency Bonus: {char['proficiency_bonus']}")

st.divider()

# --- Spell Section (To Be Developed) ---
st.subheader("✨ Spell Slots")
st.info("Spell slot tracking coming soon...")

# --- Abilities Section (To Be Developed) ---
st.subheader("💥 Class Abilities")
st.info("Ability usage tracking coming soon...")

# --- Rest Section ---
st.subheader("🛏️ Rest Options")

col1, col2 = st.columns(2)
if col1.button("Short Rest"):
    st.success("Short rest applied! (Effects coming soon...)")
if col2.button("Long Rest"):
    st.success("Long rest applied! (Spell slots & abilities will reset here)")

# --- Navigation ---
if st.button("🔙 Back to Character List"):
    st.switch_page("pages/character_select.py")

st.markdown("---")
st.markdown("🔁 Want to change your prepared spells?")

if st.button("Open Spell Library"):
    st.switch_page("pages/spell_library.py")