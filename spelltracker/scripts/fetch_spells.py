import requests
from bs4 import BeautifulSoup
import json
import time
import os

SPELLS_INDEX_URL = "https://dnd5e.wikidot.com/spells"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, "spells.json")

def get_spell_links():
    r = requests.get(SPELLS_INDEX_URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    spell_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("/spell:"):
            full_url = "https://dnd5e.wikidot.com" + href
            spell_links.append(full_url)

    return sorted(set(spell_links))

def parse_spell_page(spell_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(spell_url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch {spell_url}: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.find("title")
    if not title_tag or not title_tag.text:
        print(f"❌ No title found on {spell_url}")
        return None

    title = title_tag.text.strip()
    if " - DND 5th Edition" in title:
        title = title.replace(" - DND 5th Edition", "").strip()

    content_div = soup.find("div", {"id": "page-content"})
    if not content_div:
        print(f"❌ No content div found on {spell_url}")
        return None

    content_text = content_div.get_text(separator="\n").strip()
    if not content_text:
        print(f"❌ Content div is empty on {spell_url}")
        return None

    return {
        "title": title,
        "description": content_text,
        "url": spell_url
    }

def fetch_and_save_all_spells():
    print("Fetching spell index...")
    spell_links = get_spell_links()
    print(f"Found {len(spell_links)} spells to fetch...")

    spells = []
    for i, url in enumerate(spell_links, 1):
        print(f"Fetching {i}/{len(spell_links)}: {url}")
        spell = parse_spell_page(url)
        if spell:
            spells.append(spell)
        else:
            print(f"❌ Failed to parse {url}")
        time.sleep(0.2)  # be kind to the server

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(spells, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(spells)} spells to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_save_all_spells()
