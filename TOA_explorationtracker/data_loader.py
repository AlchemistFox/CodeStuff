import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # TOA_explorationtracker folder path
Encounter_PATH = os.path.join(BASE_DIR, "encounters.csv")
Findings_PATH = os.path.join(BASE_DIR, "findings.csv")

def load_all_encounters(filepath=Encounter_PATH):
    print(f"Loading encounters from: {filepath}")
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def load_all_findings(filepath=Findings_PATH):
    print(f"Loading encounters from: {filepath}")
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

