#!/usr/bin/env python3
"""
Enhanced Wikipedia Agriculture Scraper - Main Execution File
"""

import os
import sys
import pandas as pd
import traceback

# Add src to path
sys.path.append('src')

try:
    from enhanced_scraper import EnhancedAgricultureScraper
    ENHANCED_SCRAPER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced scraper not available: {e}")
    ENHANCED_SCRAPER_AVAILABLE = False

def setup_environment():
    """Setup the project environment"""
    print("🔧 Setting up project environment...")
    
    directories = [
        'data/raw',
        'data/processed', 
        'results/analysis_results',
        'results/visualizations',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_enhanced_scraping():
    """Run enhanced scraping with Wikipedia API"""
    print("🚀 Starting Enhanced Wikipedia Agriculture Scraping...")
    
    try:
        # Initialize scraper with safe settings
        scraper = EnhancedAgricultureScraper(delay=1.0)  # Slower to be safe
        
        # Scrape core agriculture topics
        core_topics = ['Agriculture', 'Farming', 'Crop', 'Irrigation', 'Soil_science']
        
        all_pages = []
        
        for topic in core_topics:
            try:
                print(f"\n🌾 Scraping: {topic}")
                page_data = scraper.scrape_page(topic)
                if page_data:
                    all_pages.append(page_data)
                    print(f"✅ Success: {page_data.title} ({page_data.word_count} words)")
                else:
                    print(f"⚠️ Failed: {topic}")
            except Exception as e:
                print(f"❌ Error with {topic}: {str(e)}")
                continue
        
        if all_pages:
            scraper.scraped_pages = all_pages
            file_paths = scraper.save_data("agriculture_data")
            scraper.print_scraping_summary()
            return file_paths
        else:
            print("❌ No pages were successfully scraped")
            return None
            
    except Exception as e:
        print(f"❌ Enhanced scraping failed: {e}")
        traceback.print_exc()
        return None

def check_existing_data():
    """Check if we already have scraped data"""
    csv_paths = [
        "data/processed/agriculture_comprehensive.csv",
        "data/processed/agriculture_data.csv", 
        "data/processed/agriculture_safe.csv"
    ]
    
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            print(f"✅ Found existing data: {csv_path}")
            try:
                df = pd.read_csv(csv_path)
                print(f"   📊 {len(df)} pages, {df['word_count'].sum():,} total words")
                return csv_path
            except Exception as e:
                print(f"   ⚠️ Error reading file: {e}")
    
    return None

def main():
    """Main execution function"""
    print("🌾 WIKIPEDIA AGRICULTURE SCRAPER")
    print("=" * 50)
    
    setup_environment()
    
    # Check for existing data first
    existing_data = check_existing_data()
    
    if existing_data:
        print(f"\n🎉 Data already exists at: {existing_data}")
        print("💡 Run analysis or export scripts to work with the data.")
        return
    
    print("\n📥 No existing data found. Starting fresh scrape...")
    
    # Try enhanced scraper
    if ENHANCED_SCRAPER_AVAILABLE:
        print("\n🔄 Starting enhanced scraping...")
        file_paths = run_enhanced_scraping()
        if file_paths:
            print("\n✅ Enhanced scraping completed successfully!")
            print(f"📁 Data saved to:")
            print(f"   • {file_paths['csv_path']}")
            print(f"   • {file_paths['json_path']}")
        else:
            print("\n❌ Enhanced scraping failed.")
            print("💡 Please check your internet connection and try again.")
    else:
        print("\n❌ Enhanced scraper not available.")
        print("💡 Please install dependencies: pip install wikipedia-api pandas")
    
    print("\n🎉 PROCESSING COMPLETED!")

if __name__ == "__main__":
    main()