import requests
from bs4 import BeautifulSoup
import wikipediaapi
import json
import time

# ========================================
# CONFIGURATION
# ========================================
START_URL = "https://en.wikipedia.org/wiki/Portal:Agriculture"
OUTPUT_FILE = "agriculture_wiki_data.json"
MAX_DEPTH = 3

AGRI_KEYWORDS = [
    "agri", "farm", "crop", "soil", "irrig", "fertilizer", "pesticide",
    "livestock", "horticulture", "harvest", "plantation", "food", "sustainable",
    "climate", "drought", "rural", "farming", "cattle", "dairy"
]

HEADERS = {
    "User-Agent": "AgriScraperBot/3.0 (contact: vignesh@example.com)"
}

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="AgriScraperBot/3.0 (contact: vignesh@example.com)"
)

visited = set()
results = []

# ========================================
# HELPER FUNCTIONS
# ========================================
def is_valid_link(href):
    """Check if link is a valid Wikipedia internal link."""
    if not href:
        return False
    invalid_prefixes = [
        "Help:", "File:", "Template:", "Talk:", "Special:", "Draft:",
        "Wikipedia:", "Template_talk:", "Module:", "User:"
    ]
    return href.startswith("/wiki/") and not any(p in href for p in invalid_prefixes)

def is_agri_related(title_or_url):
    """Check if title or URL is agriculture related."""
    text = title_or_url.lower()
    return any(k in text for k in AGRI_KEYWORDS)

def extract_links(url):
    """Extract internal Wikipedia links from a page."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        links = [
            "https://en.wikipedia.org" + a["href"]
            for a in soup.find_all("a", href=True)
            if is_valid_link(a["href"])
        ]
        return links
    except Exception as e:
        print(f"⚠️ Error extracting links from {url}: {e}")
        return []

def scrape_article(url):
    """Scrape a Wikipedia article via API."""
    try:
        title = url.split("/wiki/")[-1]
        page = wiki.page(title)
        if page.exists() and len(page.text.strip()) > 500:
            results.append({
                "title": page.title,
                "url": url,
                "content": page.text.strip(),
                "categories": list(page.categories.keys())
            })
            return True
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
    return False

def recursive_scrape(url, depth=0):
    """Recursively scrape up to MAX_DEPTH levels."""
    if url in visited or depth > MAX_DEPTH:
        return
    visited.add(url)

    if "Category:" in url:
        print(f"📂 Category page (depth {depth}): {url}")
    else:
        print(f"📘 Article (depth {depth}): {url}")

    # Try to scrape the article itself
    if is_agri_related(url):
        scrape_article(url)

    # Stop recursion if depth limit reached
    if depth >= MAX_DEPTH:
        return

    # Extract links for deeper traversal
    links = extract_links(url)
    for link in links[:20]:  # limit per page for speed
        if link not in visited and (is_agri_related(link) or "Category:" in link):
            time.sleep(0.5)
            recursive_scrape(link, depth + 1)

# ========================================
# MAIN
# ========================================
if __name__ == "__main__":
    print("🌾 Starting agriculture scraper (depth limit = 3)\n")

    # Load existing data if available
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
            results.extend(existing)
            visited.update([r["url"] for r in existing])
            print(f"🔁 Resuming from {len(existing)} previously saved articles.\n")
    except FileNotFoundError:
        print("🆕 Starting fresh scrape...\n")

    recursive_scrape(START_URL, depth=0)

    # Save results
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n✅ Scraping complete!")
    print(f"🧠 Total articles collected: {len(results)}")
    print(f"📂 Saved knowledge base: {OUTPUT_FILE}")
