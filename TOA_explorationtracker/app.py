import streamlit as st
import random
from data_loader import load_all_encounters
import os
from data_loader import load_all_findings

# Inject CSS to reduce vertical spacing
st.markdown(
    """
    <style>
    .css-1d391kg {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .css-1lcbmhc {
        padding-top: 0.5rem;
    }
    .stButton>button {
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load from CSV
encounters = load_all_encounters()
findings = load_all_findings()
# Create a dictionary for fast lookup by name
findings_dict = {f['name']: f for f in findings}

# Set defaults
DEFAULT_TERRAIN = "Jungle"
DEFAULT_CHANCE = "Medium"

def d20():
    return random.randint(1, 20)

def d6():
    return random.randint(1, 6)

def roll_weather():
    roll = d20()
    if roll < 17:
        return "light", "Occasional light rain"
    elif roll < 20:
        return "heavy", "Heavy rain"
    else:
        return "storm", "Tropical storm"

def rainwater_collection(weather_key, has_rain_catcher):
    base_rain = {"light": 1, "heavy": 3, "storm": 5}
    return base_rain.get(weather_key, 0) * (2 if has_rain_catcher else 1)

def food_needs(food_method, weather_key, nav_mod, hunt_dc):
    if food_method == "Rations":
        return "Rations used as normal."
    elif food_method == "Hunt/Scavenge":
        roll = d20() + nav_mod
        if roll >= hunt_dc:
            return f"Hunting success! Roll: {roll} ≥ DC {hunt_dc}. Food acquired."
        else:
            return f"Hunting failed. Roll: {roll} < DC {hunt_dc}. Rations needed."
    else:
        return "No food source; rations required."

def roll_navigation(terrain, pace, nav_mod, advantage, disadvantage):
    base_dc = 10 if terrain == "Beach" else 15
    stealth_msg = ""
    passive_penalty = 0

    if pace == "Slow":
        nav_mod += 5
        stealth_msg = "Party can move stealthily."
    elif pace == "Fast":
        nav_mod -= 5
        passive_penalty = -5
        stealth_msg = "−5 to passive perception."

    if advantage and disadvantage:
        roll = d20()
        roll_desc = "Roll with neither advantage nor disadvantage"
    elif advantage:
        roll = max(d20(), d20())
        roll_desc = "Roll with advantage"
    elif disadvantage:
        roll = min(d20(), d20())
        roll_desc = "Roll with disadvantage"
    else:
        roll = d20()
        roll_desc = "Roll normally"

    total = roll + nav_mod
    success = total >= base_dc
    lost_direction = random.choice(["N", "NE", "SE", "S", "SW", "NW"])

    return roll, total, success, lost_direction, roll_desc, stealth_msg, passive_penalty

def roll_encounter(filtered):
    roll = random.randint(1, 20)
    if roll < 18:
        return roll, None
    return roll, random.choice(filtered) if filtered else None


# Streamlit UI
st.title("TOA Exploration Tracker")

# Terrain selector
terrains = sorted(set(e["main_table"] for e in encounters))
terrain = st.selectbox("Select Terrain", terrains, index=terrains.index(DEFAULT_TERRAIN) if DEFAULT_TERRAIN in terrains else 0)

# Encounter chance (unused currently but kept if you want later)
chance = st.selectbox("Encounter Chance", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(DEFAULT_CHANCE))

# Filter encounters by terrain only (no category)
filtered = [e for e in encounters if e["main_table"] == terrain]

# Navigation inputs
pace = st.selectbox("Pace", ["Slow", "Normal", "Fast"], index=1)
nav_mod = st.number_input("Navigation Modifier", min_value=-10, max_value=10, value=0, step=1)
advantage = st.checkbox("Navigation Advantage")
disadvantage = st.checkbox("Navigation Disadvantage")

if advantage and disadvantage:
    st.error("Cannot have both advantage and disadvantage.")
    st.stop()

# Rain and food
has_rain_catcher = st.checkbox("Have 5e Rain Catcher")
food_method = st.selectbox("Food Provisions Method", ["Rations", "Hunt/Scavenge", "None"])
hunt_dc = st.number_input("Hunt/Scavenge DC", min_value=5, max_value=30, value=15)

# Generate exploration
if st.button("Generate Exploration"):
    st.header("Weather")
    weather_key, weather_desc = roll_weather()
    st.write(weather_desc)

    water_collected = rainwater_collection(weather_key, has_rain_catcher)
    st.write(f"Rainwater collected today: {water_collected} units")

    st.write(food_needs(food_method, weather_key, nav_mod, hunt_dc))

    st.header("Navigation")
    roll, total, success, lost_dir, roll_desc, stealth_msg, passive_penalty = roll_navigation(
        terrain, pace, nav_mod, advantage, disadvantage
    )
    st.write(f"{roll_desc}: Roll {roll} + Mod {nav_mod} = {total}")
    if success:
        st.success(f"Navigation successful. {stealth_msg}")
    else:
        st.error(f"Lost! Proceed {lost_dir}. {stealth_msg}")

    st.header("Encounters")
    for time in ["Morning", "Afternoon", "Night"]:
        roll, encounter = roll_encounter(filtered)
        st.subheader(time)
        if encounter is None:
            st.write(f"Roll: {roll} → No encounter")
        else:
            name = encounter['name']
            st.write(f"Roll: {roll} → {name}")
            st.markdown(f"*{encounter.get('description', '')}*")

            # 5e.tools link based on name slug
            monster_slug = name.lower().replace(" ", "_")
            url = f"https://5e.tools/bestiary.html#{monster_slug}"
            st.markdown(f"[View on 5e.tools: {name}]({url})")

            # Show detailed findings if available
            info = findings_dict.get(name)
            if info:
                desc = info.get("desc", "")
                st.markdown(desc)
