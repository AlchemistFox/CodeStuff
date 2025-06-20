import streamlit as st
import pandas as pd
import random

# Initialize session state
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = True

def roll_d20(mod=0):
    roll = random.randint(1, 20)
    return roll, roll + mod

def get_modifier(score):
    return (score - 10) // 2

def save_to_csv(data):
    pd.DataFrame([data]).to_csv("character_sheet.csv", index=False)

def load_from_csv():
    try:
        return pd.read_csv("character_sheet.csv").iloc[0].to_dict()
    except:
        return {}

default = {
    "Name": "Arthas",
    "Class": "Paladin",
    "Race": "Human",
    "Level": 1,
    "Strength": 15,
    "Dexterity": 14,
    "Constitution": 13,
    "Intelligence": 12,
    "Wisdom": 10,
    "Charisma": 16
}

data = {**default, **load_from_csv()}

st.title("D&D 5e Character Sheet")

# Header inputs
cols = st.columns([3,2,2,1])
with cols[0]:
    data["Name"] = st.text_input("Name", value=data["Name"], disabled=not st.session_state.edit_mode)
with cols[1]:
    data["Class"] = st.text_input("Class", value=data["Class"], disabled=not st.session_state.edit_mode)
with cols[2]:
    data["Race"] = st.text_input("Race", value=data["Race"], disabled=not st.session_state.edit_mode)
with cols[3]:
    data["Level"] = st.number_input("Level", min_value=1, max_value=20, value=int(data["Level"]), disabled=not st.session_state.edit_mode)

if st.button("🔒 Lock" if st.session_state.edit_mode else "🔓 Unlock"):
    st.session_state.edit_mode = not st.session_state.edit_mode
    if not st.session_state.edit_mode:
        save_to_csv(data)
        st.toast("Character saved!", icon="💾")

abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

# --- CSS for fixed-size boxes ---
st.markdown("""
<style>
    .ability-grid {
        display: grid;
        grid-template-columns: repeat(6, 100px);
        gap: 10px;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stat-box {
        border: 2px solid black;
        border-radius: 6px;
        background-color: white;
        text-align: center;
        padding: 10px;
        user-select: none;
        width: 100px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-family: "Times New Roman", serif;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.15);
    }
    .stat-label {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
    }
    .mod-value {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .roll-btn {
        margin-top: auto;
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.edit_mode:
    st.subheader("Edit Ability Scores")
    for attr in abilities:
        data[attr] = st.number_input(attr, min_value=1, max_value=30, value=data[attr], key=attr)
else:
    st.subheader("Ability Scores")
    st.markdown("<div class='ability-grid'>", unsafe_allow_html=True)
    for attr in abilities:
        mod = get_modifier(data[attr])
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-label'>{attr}</div>
                <div class='mod-value'>{mod:+}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Roll buttons outside the grid for better layout
    roll_cols = st.columns(len(abilities))
    for i, attr in enumerate(abilities):
        mod = get_modifier(data[attr])
        if roll_cols[i].button(f"Roll {attr}", key=f"roll_{attr}"):
            roll, total = roll_d20(mod)
            st.success(f"{attr} Check: Rolled {roll} + {mod} = {total}")
