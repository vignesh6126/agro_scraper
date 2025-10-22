import json

# Load the scraped JSON data
with open("agriculture_wiki_data.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Open a text file to write
with open("agriculture_wiki_data.txt", "w", encoding="utf-8") as f:
    f.write("AGRICULTURE WIKIPEDIA DATA\n")
    f.write("="*80 + "\n\n")
    
    for idx, article in enumerate(articles, 1):
        f.write(f"[{idx}] {article['title']}\n")
        f.write(f"URL: {article['url']}\n")
        f.write(f"Categories: {', '.join(article['categories'])}\n")
        f.write(f"Summary:\n{article['summary']}\n\n")
        f.write("Full Text:\n")
        f.write(article['text'] + "\n")
        f.write("="*80 + "\n\n")

print("✅ Converted JSON to readable text: 'agriculture_wiki_data.txt'")
