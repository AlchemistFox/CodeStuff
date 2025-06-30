import requests
from bs4 import BeautifulSoup
import json
import time

SPELLS_INDEX_URL = "https://dnd5e.wikidot.com/spells"

def get_spell_links():
    """Scrape Wikidot spell list using the correct `spell:` page format."""
    r = requests.get(SPELLS_INDEX_URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    spell_links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/spell:'):
            page_name = href.strip('/')
            spell_links.append(page_name)

    return sorted(set(spell_links))




def get_wikidot_page_content(site: str, page: str):
    api_url = f"https://{site}.wikidot.com/ajax-module-connector.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # Correctly format the JSON string parameter
    params = {
        'moduleName': 'wiki_ajax',
        'method': 'getPage',
        'params': f'{{"page":"{page}"}}'
    }

    try:
        r = requests.get(api_url, params=params, headers=headers)
        r.raise_for_status()
        data = r.json()
        if "page" not in data:
            print(f"❌ No page found in response for {page}")
            return None
        return data
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return None






def parse_spell_page(data):
    """
    Parses the raw JSON data from a spell page into a clean dict.
    """
    if not data:
        return None

    page = data.get('page', {})
    if not page:
        print("⚠️  No 'page' found in response")
        return None

    page_content = page.get('content', '')
    title = page.get('title', 'Unknown')

    if not page_content:
        print(f"⚠️  Empty content for: {title}")
        return None

    return {
        'title': title,
        'content': page_content,
    }


def fetch_all_spells():
    site = 'dnd5e'
    spell_links = get_spell_links()
    print(f"Found {len(spell_links)} spells to fetch...")

    spells = []
    for i, page_path in enumerate(spell_links, 1):
        print(f"Fetching {i}/{len(spell_links)}: {page_path}")
        spell = get_wikidot_page_content(page_path)

        if spell:
            print(f"✅ Parsed: {spell['title']}")
            spells.append(spell)
        else:
            print(f"❌ Failed to parse {page_path}")
        time.sleep(0.3)
        print(f"Fetching {i}/{len(spell_links)}: {page_path} → https://dnd5e.wikidot.com/{page_path}")


    return spells



def save_spells_to_json(spells, filename='data/spells.json'):
    """Save spells list to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(spells, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(spells)} spells to {filename}")
