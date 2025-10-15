"""
Configuration settings for Wikipedia Agriculture Scraper
"""

# Wikipedia API Configuration
WIKIPEDIA_CONFIG = {
    'user_agent': 'AgricultureResearchBot/1.0 (https://github.com/yourusername/agriculture-scraper)',
    'language': 'en',
    'rate_limit_delay': 0.5,  # seconds between requests
    'timeout': 30,
}

# Agriculture Topics to Scrape
AGRICULTURE_TOPICS = [
    # Core Agriculture Topics
    'Agriculture',
    'Farming',
    'Crop',
    'Livestock',
    'Horticulture',
    
    # Agricultural Practices
    'Irrigation',
    'Crop_rotation',
    'Sustainable_agriculture',
    'Organic_farming',
    'Precision_agriculture',
    
    # Agricultural Science
    'Agronomy',
    'Soil_science',
    'Plant_breeding',
    'Agricultural_engineering',
    
    # Agricultural Economics
    'Agricultural_economics',
    'Food_security',
    'Agricultural_subsidy',
    
    # Specific Crops and Animals
    'Wheat',
    'Rice',
    'Maize',
    'Cattle',
    'Poultry_farming',
    
    # Agricultural Technology
    'Agricultural_technology',
    'Greenhouse',
    'Hydroponics',
    'Agricultural_robot'
]

# Data Export Settings
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'json_indent': 2,
    'image_dpi': 300,
    'image_format': 'png'
}

# Analysis Settings
ANALYSIS_CONFIG = {
    'top_n_categories': 15,
    'wordcloud_max_words': 100,
    'min_word_length': 4
}