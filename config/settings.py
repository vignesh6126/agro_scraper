"""
Configuration for Large-Scale Wikipedia Agriculture Scraping
"""

# Wikipedia API Configuration
WIKIPEDIA_CONFIG = {
    'user_agent': 'AgricultureResearchBot/2.0 (https://github.com/vignesh6126/agro_scraper)',
    'language': 'en',
    'rate_limit_delay': 0.3,  # Faster but still respectful
    'timeout': 30,
    'max_retries': 3
}

# Agriculture Portal and Main Categories
AGRICULTURE_PORTALS = [
    'Portal:Agriculture',
    'Portal:Agriculture_and_Agronomy',
    'Portal:Fishing',
    'Portal:Forestry'
]

# Agriculture Categories to Explore
AGRICULTURE_CATEGORIES = [
    'Category:Agriculture',
    'Category:Agronomy',
    'Category:Farming',
    'Category:Horticulture',
    'Category:Livestock',
    'Category:Agricultural_technology',
    'Category:Sustainable_agriculture',
    'Category:Agricultural_economics',
    'Category:Food_industry',
    'Category:Crops',
    'Category:Soil_science',
    'Category:Irrigation',
    'Category:Agricultural_engineering'
]

# Keywords to identify agriculture-related content
AGRICULTURE_KEYWORDS = [
    'agriculture', 'farm', 'crop', 'soil', 'irrigation', 'harvest', 'livestock',
    'organic', 'sustainable', 'horticulture', 'agri', 'farming', 'cultivation',
    'cattle', 'poultry', 'fertilizer', 'pesticide', 'agronomy', 'hydroponics',
    'greenhouse', 'agricultural', 'agro', 'yield', 'plantation', 'orchard',
    'pasture', 'dairy', 'meat', 'wool', 'fiber', 'feed', 'forage', 'silage',
    'compost', 'manure', 'tillage', 'harvester', 'tractor', 'irrigate',
    'aquaculture', 'fishery', 'forestry', 'timber', 'lumber', 'silviculture',
    'agribusiness', 'food security', 'crop rotation', 'soil conservation'
]

# Scraping Limits (adjust based on your needs)
SCRAPING_CONFIG = {
    'max_pages_per_category': 500,
    'max_links_per_page': 100,
    'max_depth': 3,
    'max_total_pages': 10000,  # Increase for more data
    'min_word_count': 50,  # Skip very short pages
}

# Data Export Settings
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'json_indent': 2,
    'batch_size': 1000,  # Save in batches to avoid memory issues
    'compression': 'gzip'  # Compress large files
}