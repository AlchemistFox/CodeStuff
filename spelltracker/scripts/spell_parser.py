from bs4 import BeautifulSoup

def parse_spell_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Example: grab spell name/title from the <h1> tag or similar
    title_tag = soup.find("h1")
    name = title_tag.text.strip() if title_tag else "Unknown"

    # Grab description paragraphs, just an example
    desc = []
    for p in soup.find_all("p"):
        desc.append(p.text.strip())

    # Return a dict with info
    return {
        "name": name,
        "description": "\n\n".join(desc),
        # Add more fields as you parse them...
    }
