# TOA_explorationtracker/data.py

# Example encounter tables by terrain and roll range
encounters = {
    "Beach": {
        # Key: dice roll or range as string, Value: encounter name
        "1-20": "No encounter",
        "21-50": "Giant Crab",
        "51-100": "Merfolk Ambush",
    },
    "Forest": {
        "1-30": "No encounter",
        "31-60": "Goblin Scouts",
        "61-100": "Owlbear",
    },
    # Add your full tables here as per original JS data
}

# Weather descriptions by roll category
weather_table = {
    "light": "Occasional light rain",
    "heavy": "Heavy rain - Visibility limited to 150 feet",
    "storm": "Tropical storm - Travel by canoe impossible, travel on foot gains 1 level of exhaustion, DC 10 Constitution save or worse. Disadvantage on checks to avoid becoming lost",
}

# Navigation base DC by terrain
navigation_dc = {
    "Beach": 10,
    "Forest": 15,
    # Add other terrains
}
