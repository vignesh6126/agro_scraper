import wikipediaapi
import json
from tqdm import tqdm
import time

# --------------------------
# Initialize Wikipedia API
# --------------------------
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='AgriPortalScraperBot/1.0 (vignesh@example.com)'
)

# --------------------------
# Helper: Scrape full article
# --------------------------
def get_wiki_article(title):
    page = wiki.page(title)
    if not page.exists():
        return None
    return {
        "title": page.title,
        "url": page.fullurl,
        "summary": page.summary,
        "text": page.text,
        "categories": list(page.categories.keys())
    }

# --------------------------
# Main scraper
# --------------------------
def scrape_agriculture_portal():
    print("🚀 Scraping Portal:Agriculture ...")
    
    portal = wiki.page("Portal:Agriculture")
    if not portal.exists():
        print("❌ Portal not found!")
        return

    # Get all links from the portal page
    links = portal.links  # dict of {title: page_obj}
    article_titles = [
        title for title in links
        if not any(x in title for x in [":"])  # exclude Category:, Help:, File:, etc.
    ]

    print(f"✅ Found {len(article_titles)} linked articles in the portal.")

    data = []
    failed = []

    # Scrape each linked article
    for title in tqdm(article_titles, desc="Scraping Articles"):
        try:
            article = get_wiki_article(title)
            if article:
                data.append(article)
            time.sleep(0.5)  # polite delay
        except Exception as e:
            failed.append({"title": title, "error": str(e)})

    print(f"\n✅ Successfully scraped {len(data)} articles.")
    print(f"❌ Failed to scrape {len(failed)} articles.")

    # Save data
    with open("agriculture_wiki_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if failed:
        with open("failed_articles.json", "w", encoding="utf-8") as f:
            json.dump(failed, f, ensure_ascii=False, indent=2)

    print("📁 Saved data to 'agriculture_wiki_data.json'")
    return data

# --------------------------
# Run scraper
# --------------------------
if __name__ == "__main__":
    scrape_agriculture_portal()
