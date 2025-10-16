#!/usr/bin/env python3
"""
Large-Scale Wikipedia Agriculture Scraper - For Deep Learning Training
"""

import os
import sys
import pandas as pd
import traceback

# Add src to path
sys.path.append('src')

try:
    from large_scale_scraper import LargeScaleAgricultureScraper
    LARGE_SCALE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Large-scale scraper not available: {e}")
    LARGE_SCALE_AVAILABLE = False

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

def run_large_scale_scraping():
    """Run large-scale agriculture data scraping"""
    print("🚀 Starting Large-Scale Agriculture Data Collection...")
    print("💡 This will scrape thousands of agriculture-related pages for deep learning training.")
    
    try:
        scraper = LargeScaleAgricultureScraper()
        scraped_data = scraper.run_comprehensive_scraping()
        
        if scraped_data:
            print(f"\n✅ Large-scale scraping completed!")
            print(f"📊 Collected {len(scraped_data)} agriculture-related pages")
            return True
        else:
            print("❌ No data was collected")
            return False
            
    except Exception as e:
        print(f"❌ Large-scale scraping failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main execution function"""
    print("🌾 LARGE-SCALE WIKIPEDIA AGRICULTURE SCRAPER")
    print("=" * 60)
    print("🎯 Purpose: Collect massive agriculture data for deep learning")
    print("📈 Target: 10,000+ agriculture-related Wikipedia pages")
    print("=" * 60)
    
    setup_environment()
    
    if LARGE_SCALE_AVAILABLE:
        print("\n🔄 Starting large-scale data collection...")
        success = run_large_scale_scraping()
        
        if success:
            print("\n🎉 DATA COLLECTION COMPLETED!")
            print("💾 Check 'data/processed/' for your agriculture dataset")
        else:
            print("\n❌ Data collection failed")
    else:
        print("\n❌ Large-scale scraper not available.")
        print("💡 Please install dependencies: pip install wikipedia-api pandas tqdm")

if __name__ == "__main__":
    main()