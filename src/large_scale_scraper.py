"""
Large-scale Wikipedia agriculture scraper - FIXED SAVING VERSION
"""

import wikipediaapi
import pandas as pd
import time
import json
import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from tqdm import tqdm
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import os
from config.settings import (WIKIPEDIA_CONFIG, AGRICULTURE_PORTALS, 
                           AGRICULTURE_CATEGORIES, AGRICULTURE_KEYWORDS, 
                           SCRAPING_CONFIG, EXPORT_CONFIG)

@dataclass
class AgriculturePage:
    """Enhanced page data structure for comprehensive scraping"""
    title: str
    url: str
    summary: str
    full_text: str
    categories: List[str]
    sections: Dict[str, str]
    links: List[str]
    word_count: int
    page_id: int
    last_modified: str
    scraped_at: str
    agriculture_score: float = 0.0

class LargeScaleAgricultureScraper:
    """
    Large-scale scraper for comprehensive agriculture data collection
    """
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=WIKIPEDIA_CONFIG['user_agent'],
            language=WIKIPEDIA_CONFIG['language'],
            extract_format=wikipediaapi.ExtractFormat.HTML
        )
        
        # Tracking sets to avoid duplicates
        self.scraped_titles: Set[str] = set()
        self.queued_titles: Set[str] = set()
        self.failed_titles: Set[str] = set()
        
        # Storage
        self.scraped_pages: List[AgriculturePage] = []
        
        # Statistics
        self.stats = {
            'total_scraped': 0,
            'total_words': 0,
            'start_time': None,
            'agriculture_pages': 0,
            'failed_requests': 0
        }
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for large-scale scraping"""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/large_scale_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def calculate_agriculture_score(self, page_title: str, content: str, categories: List[str]) -> float:
        """Calculate how agriculture-related a page is"""
        score = 0.0
        content_lower = content.lower()
        
        # Check title
        title_lower = page_title.lower()
        for keyword in AGRICULTURE_KEYWORDS:
            if keyword in title_lower:
                score += 2.0
        
        # Check content
        for keyword in AGRICULTURE_KEYWORDS:
            score += content_lower.count(keyword) * 0.1
        
        # Check categories
        for category in categories:
            category_lower = category.lower()
            for keyword in AGRICULTURE_KEYWORDS:
                if keyword in category_lower:
                    score += 1.0
        
        return score
    
    def scrape_page_comprehensive(self, page_title: str) -> Optional[AgriculturePage]:
        """Scrape a page with comprehensive data extraction"""
        if page_title in self.scraped_titles:
            return None
        
        try:
            page = self.wiki.page(page_title)
            
            if not page.exists():
                self.failed_titles.add(page_title)
                return None
            
            # Extract sections with content
            sections = self._extract_all_sections(page)
            
            # Calculate agriculture score
            agriculture_score = self.calculate_agriculture_score(
                page_title, page.text, list(page.categories.keys())
            )
            
            # Skip if not agriculture-related and score is too low
            if agriculture_score < 0.5 and 'agriculture' not in page_title.lower():
                return None
            
            page_data = AgriculturePage(
                title=page.title,
                url=page.fullurl,
                summary=page.summary,
                full_text=page.text,
                categories=list(page.categories.keys()),
                sections=sections,
                links=list(page.links.keys())[:SCRAPING_CONFIG['max_links_per_page']],
                word_count=len(page.text.split()),
                page_id=page.pageid,
                last_modified=str(page.lastrevid),
                scraped_at=pd.Timestamp.now().isoformat(),
                agriculture_score=agriculture_score
            )
            
            # Update statistics
            self.stats['total_scraped'] += 1
            self.stats['total_words'] += page_data.word_count
            if agriculture_score > 1.0:
                self.stats['agriculture_pages'] += 1
            
            self.scraped_titles.add(page_title)
            self.queued_titles.discard(page_title)
            
            time.sleep(WIKIPEDIA_CONFIG['rate_limit_delay'])
            
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {page_title}: {e}")
            self.failed_titles.add(page_title)
            self.queued_titles.discard(page_title)
            return None
    
    def _extract_all_sections(self, page) -> Dict[str, str]:
        """Extract all sections with their full content"""
        sections = {}
        
        def _extract_section_recursive(section, level=0):
            if section.title and section.title.strip():
                sections[section.title] = {
                    'content': section.text,
                    'level': level,
                    'word_count': len(section.text.split())
                }
            
            for subsection in section.sections:
                _extract_section_recursive(subsection, level + 1)
        
        for section in page.sections:
            _extract_section_recursive(section)
        
        return sections
    
    def get_category_pages(self, category_name: str, max_pages: int = None) -> List[str]:
        """Get all pages in a category"""
        if max_pages is None:
            max_pages = SCRAPING_CONFIG['max_pages_per_category']
        
        category = self.wiki.page(category_name)
        if not category.exists():
            return []
        
        pages = []
        for page_title in list(category.categorymembers.keys())[:max_pages]:
            if (page_title not in self.scraped_titles and 
                page_title not in self.queued_titles):
                pages.append(page_title)
                self.queued_titles.add(page_title)
        
        self.logger.info(f"Found {len(pages)} pages in category {category_name}")
        return pages
    
    def get_portal_links(self, portal_name: str) -> List[str]:
        """Get all links from an agriculture portal"""
        portal = self.wiki.page(portal_name)
        if not portal.exists():
            return []
        
        links = []
        for link_title in list(portal.links.keys())[:SCRAPING_CONFIG['max_links_per_page']]:
            if (link_title not in self.scraped_titles and 
                link_title not in self.queued_titles and
                self.is_agriculture_related(link_title)):
                links.append(link_title)
                self.queued_titles.add(link_title)
        
        self.logger.info(f"Found {len(links)} agriculture links from portal {portal_name}")
        return links
    
    def is_agriculture_related(self, title: str) -> bool:
        """Check if a title is likely agriculture-related"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in AGRICULTURE_KEYWORDS)
    
    def explore_links(self, page_data: AgriculturePage, depth: int = 1) -> List[str]:
        """Explore links from a page with depth limitation"""
        if depth >= SCRAPING_CONFIG['max_depth']:
            return []
        
        new_links = []
        for link_title in page_data.links:
            if (self.is_agriculture_related(link_title) and
                link_title not in self.scraped_titles and
                link_title not in self.queued_titles and
                len(self.scraped_titles) + len(self.queued_titles) < SCRAPING_CONFIG['max_total_pages']):
                
                new_links.append(link_title)
                self.queued_titles.add(link_title)
        
        return new_links
    
    def scrape_batch(self, page_titles: List[str], batch_size: int = 50) -> List[AgriculturePage]:
        """Scrape a batch of pages"""
        scraped_batch = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_title = {
                executor.submit(self.scrape_page_comprehensive, title): title 
                for title in page_titles[:batch_size]
            }
            
            for future in tqdm(as_completed(future_to_title), total=len(future_to_title), desc="Scraping batch"):
                page_data = future.result()
                if page_data:
                    scraped_batch.append(page_data)
        
        return scraped_batch
    
    def save_progress(self, batch_number: int = None):
        """Save progress to avoid data loss - FIXED VERSION"""
        if not self.scraped_pages:
            self.logger.warning("No data to save")
            return
        
        # Ensure directories exist
        os.makedirs('data/processed', exist_ok=True)
        os.makedirs('data/raw', exist_ok=True)
        
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        batch_suffix = f"_batch_{batch_number}" if batch_number else ""
        
        try:
            # Save CSV
            df = self.export_to_dataframe()
            csv_path = f"data/processed/agriculture{batch_suffix}_{timestamp}.csv"
            df.to_csv(csv_path, index=False, encoding=EXPORT_CONFIG['csv_encoding'])
            self.logger.info(f"✅ CSV saved: {csv_path} ({len(df)} rows)")
            
            # Save JSON (compressed)
            json_path = f"data/raw/agriculture{batch_suffix}_{timestamp}.json.gz"
            json_data = [asdict(page) for page in self.scraped_pages]
            with gzip.open(json_path, 'wt', encoding='utf-8') as f:
                json.dump(json_data, f, indent=EXPORT_CONFIG['json_indent'], ensure_ascii=False)
            self.logger.info(f"✅ JSON saved: {json_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
            return False
    
    def run_comprehensive_scraping(self) -> List[AgriculturePage]:
        """Run comprehensive agriculture data scraping"""
        self.stats['start_time'] = pd.Timestamp.now()
        self.logger.info("Starting comprehensive agriculture data scraping...")
        
        all_pages_to_scrape = []
        
        # Step 1: Scrape agriculture portals
        self.logger.info("Scraping agriculture portals...")
        for portal in AGRICULTURE_PORTALS:
            portal_links = self.get_portal_links(portal)
            all_pages_to_scrape.extend(portal_links)
        
        # Step 2: Scrape agriculture categories
        self.logger.info("Scraping agriculture categories...")
        for category in AGRICULTURE_CATEGORIES:
            category_pages = self.get_category_pages(category)
            all_pages_to_scrape.extend(category_pages)
        
        # Remove duplicates
        all_pages_to_scrape = list(set(all_pages_to_scrape))
        self.logger.info(f"Total unique pages to scrape: {len(all_pages_to_scrape)}")
        
        # Step 3: Batch scraping with saving
        batch_size = 100
        batch_number = 0
        
        for i in range(0, len(all_pages_to_scrape), batch_size):
            if len(self.scraped_titles) >= SCRAPING_CONFIG['max_total_pages']:
                break
                
            batch = all_pages_to_scrape[i:i + batch_size]
            batch_number += 1
            self.logger.info(f"Processing batch {batch_number} ({len(batch)} pages)")
            
            scraped_batch = self.scrape_batch(batch, batch_size)
            self.scraped_pages.extend(scraped_batch)
            
            # Save after each batch
            self.save_progress(batch_number)
            
            # Explore links from scraped pages (limited depth)
            for page in scraped_batch:
                if len(self.scraped_titles) < SCRAPING_CONFIG['max_total_pages']:
                    new_links = self.explore_links(page, depth=1)
                    all_pages_to_scrape.extend(new_links)
        
        # Final save
        self.save_progress()
        self.logger.info("Comprehensive scraping completed!")
        self.print_final_stats()
        
        return self.scraped_pages
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Convert scraped data to pandas DataFrame"""
        rows = []
        
        for page in self.scraped_pages:
            row = {
                'title': page.title,
                'url': page.url,
                'summary': page.summary,
                'full_text_length': len(page.full_text),
                'word_count': page.word_count,
                'categories_count': len(page.categories),
                'sections_count': len(page.sections),
                'links_count': len(page.links),
                'page_id': page.page_id,
                'agriculture_score': page.agriculture_score,
                'last_modified': page.last_modified,
                'scraped_at': page.scraped_at,
                'categories': ' | '.join(page.categories),
                'is_high_agriculture': page.agriculture_score > 2.0
            }
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def print_final_stats(self):
        """Print comprehensive scraping statistics"""
        duration = pd.Timestamp.now() - self.stats['start_time']
        
        print("\n" + "="*70)
        print("🌾 LARGE-SCALE AGRICULTURE SCRAPING - FINAL STATISTICS")
        print("="*70)
        print(f"🕒 Duration: {duration}")
        print(f"📄 Total Pages Scraped: {self.stats['total_scraped']}")
        print(f"🌾 Agriculture-Related Pages: {self.stats['agriculture_pages']}")
        print(f"📝 Total Words: {self.stats['total_words']:,}")
        print(f"❌ Failed Requests: {len(self.failed_titles)}")
        print(f"💾 Memory Usage: {len(self.scraped_titles)} titles tracked")
        
        if self.stats['total_scraped'] > 0:
            avg_words = self.stats['total_words'] / self.stats['total_scraped']
            agriculture_ratio = (self.stats['agriculture_pages'] / self.stats['total_scraped']) * 100
            print(f"📊 Average Words per Page: {avg_words:,.0f}")
            print(f"🎯 Agriculture Content Ratio: {agriculture_ratio:.1f}%")
        
        print("="*70)

def main():
    """Standalone large-scale scraping"""
    scraper = LargeScaleAgricultureScraper()
    scraper.run_comprehensive_scraping()

if __name__ == "__main__":
    main()