import json

INPUT_FILE = "agriculture_wiki_data.json"
OUTPUT_FILE = "agriculture_wiki_data.txt"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i, article in enumerate(data, 1):
        title = article.get("title", "Untitled")
        url = article.get("url", "N/A")
        categories = article.get("categories", [])
        summary = article.get("summary", "")  # some scrapers might have it
        content = article.get("content", article.get("text", ""))

        f.write(f"[{i}] {title}\n")
        f.write(f"URL: {url}\n")
        if categories:
            f.write(f"Categories: {', '.join(categories)}\n\n")
        if summary:
            f.write(f"Summary:\n{summary}\n\n")
        f.write("Full Text:\n")
        f.write(content.strip() + "\n")
        f.write("=" * 80 + "\n\n")

print(f"✅ Saved '{OUTPUT_FILE}' successfully with {len(data)} entries.")
