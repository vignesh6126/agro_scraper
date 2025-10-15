import wikipediaapi
import pandas as pd
import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import re
from tqdm import tqdm
from config.settings import WIKIPEDIA_CONFIG, AGRICULTURE_TOPICS, EXPORT_CONFIG

@dataclass
class PageSection:
    """Data class for page sections"""
    title: str
    content: str
    level: int
    word_count: int

@dataclass
class AgriculturePage:
    """Data class for agriculture page data"""
    title: str
    url: str
    summary: str
    full_text: str
    categories: List[str]
    sections: List[PageSection]
    links: List[str]
    word_count: int
    page_id: int
    last_modified: str
    scraped_at: str

class EnhancedAgricultureScraper:
    """
    Enhanced Wikipedia API Scraper for Agriculture Data
    """
    
    def __init__(self, user_agent: str = None, language: str = 'en', delay: float = 0.5):
        self.config = {
            'user_agent': user_agent or WIKIPEDIA_CONFIG['user_agent'],
            'language': language,
            'delay': delay
        }
        
        # Initialize Wikipedia API
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=self.config['user_agent'],
            language=self.config['language'],
            extract_format=wikipediaapi.ExtractFormat.HTML
        )
        
        # Statistics
        self.stats = {
            'total_pages': 0,
            'successful_scrapes': 0,
            'failed_scrapes': 0,
            'total_words': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Storage for scraped data
        self.scraped_pages: List[AgriculturePage] = []
    
    def scrape_page(self, page_title: str) -> Optional[AgriculturePage]:
        """
        Scrape a single Wikipedia page with comprehensive data
        """
        try:
            print(f"📖 Scraping: {page_title}")
            page = self.wiki.page(page_title)
            
            if not page.exists():
                print(f"❌ Page '{page_title}' does not exist")
                self.stats['failed_scrapes'] += 1
                return None
            
            # Extract sections with hierarchy
            sections = self._extract_sections_with_hierarchy(page)
            
            # Extract categories
            categories = list(page.categories.keys())
            
            # Extract links (limit to avoid too much data)
            links = list(page.links.keys())[:100]
            
            # Create page data object
            page_data = AgriculturePage(
                title=page.title,
                url=page.fullurl,
                summary=page.summary,
                full_text=page.text,
                categories=categories,
                sections=sections,
                links=links,
                word_count=len(page.text.split()),
                page_id=page.pageid,
                last_modified=str(page.lastrevid),
                scraped_at=pd.Timestamp.now().isoformat()  # This is already string
            )
            
            # Update statistics
            self.stats['successful_scrapes'] += 1
            self.stats['total_words'] += page_data.word_count
            
            # Rate limiting
            time.sleep(self.config['delay'])
            
            return page_data
            
        except Exception as e:
            print(f"❌ Error scraping {page_title}: {str(e)}")
            self.stats['failed_scrapes'] += 1
            return None
    
    def _extract_sections_with_hierarchy(self, page) -> List[PageSection]:
        """
        Extract all sections with their hierarchical structure
        """
        sections = []
        
        def _extract_recursive(section, current_level=0):
            if section.title and section.title.strip():
                section_data = PageSection(
                    title=section.title,
                    content=section.text,
                    level=current_level,
                    word_count=len(section.text.split())
                )
                sections.append(section_data)
            
            # Process subsections
            for subsection in section.sections:
                _extract_recursive(subsection, current_level + 1)
        
        # Start extraction from main page sections
        for section in page.sections:
            _extract_recursive(section)
        
        return sections
    
    def find_agriculture_related_pages(self, seed_page_title: str, max_pages: int = 20) -> List[str]:
        """
        Find agriculture-related pages using Wikipedia links
        """
        print(f"🔍 Finding related pages from: {seed_page_title}")
        related_pages = set()
        
        # Get the page object first
        seed_page = self.wiki.page(seed_page_title)
        if not seed_page.exists():
            print(f"❌ Seed page '{seed_page_title}' does not exist")
            return list(related_pages)
        
        # Agriculture-related keywords for filtering
        agriculture_keywords = [
            'agriculture', 'farm', 'crop', 'soil', 'irrigation', 'harvest',
            'livestock', 'organic', 'sustainable', 'horticulture', 'agri',
            'farming', 'cultivation', 'cattle', 'poultry', 'fertilizer',
            'pesticide', 'agronomy', 'hydroponics', 'greenhouse'
        ]
        
        # Check links from seed page
        for link in list(seed_page.links.keys())[:max_pages * 2]:
            if self._is_agriculture_related(link, agriculture_keywords):
                related_pages.add(link)
            if len(related_pages) >= max_pages:
                break
        
        print(f"✅ Found {len(related_pages)} related pages")
        return list(related_pages)
    
    def _is_agriculture_related(self, page_title: str, keywords: List[str]) -> bool:
        """
        Check if a page title is agriculture-related
        """
        page_lower = page_title.lower()
        return any(keyword in page_lower for keyword in keywords)
    
    def scrape_topic_network(self, main_topic: str, max_pages: int = 15) -> List[AgriculturePage]:
        """
        Scrape a network of pages related to a main topic
        """
        print(f"🌐 Building topic network for: {main_topic}")
        scraped_pages = []
        
        # Scrape main topic
        main_page = self.scrape_page(main_topic)
        if main_page:
            scraped_pages.append(main_page)
            print(f"✅ Main topic scraped: {main_topic}")
        else:
            print(f"❌ Failed to scrape main topic: {main_topic}")
            return scraped_pages
        
        # Find and scrape related pages
        related_pages = self.find_agriculture_related_pages(main_topic, max_pages // 2)
        
        for related_page in tqdm(related_pages, desc=f"Related to {main_topic}"):
            # Check if we already have this page
            if not any(p.title == related_page for p in scraped_pages):
                page_data = self.scrape_page(related_page)
                if page_data:
                    scraped_pages.append(page_data)
            
            # Limit total pages
            if len(scraped_pages) >= max_pages:
                break
        
        print(f"✅ Topic network completed: {len(scraped_pages)} pages for {main_topic}")
        return scraped_pages
    
    def scrape_all_agriculture_topics(self) -> List[AgriculturePage]:
        """
        Scrape all predefined agriculture topics
        """
        print("🚀 Starting comprehensive agriculture data scraping...")
        self.stats['start_time'] = pd.Timestamp.now().isoformat()  # Convert to string immediately
        
        all_pages = []
        
        for topic in tqdm(AGRICULTURE_TOPICS, desc="Agriculture Topics"):
            topic_pages = self.scrape_topic_network(topic, max_pages=10)
            all_pages.extend(topic_pages)
            
            # Remove duplicates based on title
            seen_titles = set()
            unique_pages = []
            for page in all_pages:
                if page.title not in seen_titles:
                    seen_titles.add(page.title)
                    unique_pages.append(page)
            all_pages = unique_pages
            
            print(f"📊 Progress: {len(all_pages)} unique pages collected so far")
        
        self.stats['end_time'] = pd.Timestamp.now().isoformat()  # Convert to string immediately
        self.stats['total_pages'] = len(all_pages)
        self.scraped_pages = all_pages
        
        print(f"🎉 Scraping completed! Collected {len(all_pages)} unique pages")
        return all_pages
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Convert scraped data to pandas DataFrame
        """
        if not self.scraped_pages:
            print("⚠️ No data to export. Run scraping first.")
            return pd.DataFrame()
        
        rows = []
        
        for page in self.scraped_pages:
            # Flatten the data for DataFrame
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
                'last_modified': page.last_modified,
                'scraped_at': page.scraped_at,
                'categories': ' | '.join(page.categories),
                'agriculture_categories': ' | '.join([cat for cat in page.categories 
                                                    if any(keyword in cat.lower() 
                                                          for keyword in ['agriculture', 'farm', 'crop'])])
            }
            
            # Add section statistics
            if page.sections:
                section_words = [section.word_count for section in page.sections]
                row['avg_section_words'] = sum(section_words) / len(section_words)
                row['max_section_words'] = max(section_words)
                row['min_section_words'] = min(section_words)
            else:
                row['avg_section_words'] = 0
                row['max_section_words'] = 0
                row['min_section_words'] = 0
            
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def _convert_to_serializable(self, obj):
        """
        Convert non-serializable objects to JSON-serializable formats
        """
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, (pd.DataFrame, pd.Series)):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._convert_to_serializable(value) for key, value in obj.items()}
        else:
            return obj
    
    def save_data(self, base_filename: str = None):
        """
        Save scraped data in multiple formats
        """
        if not self.scraped_pages:
            print("⚠️ No data to save. Run scraping first.")
            return
        
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        base_name = base_filename or f"agriculture_data_{timestamp}"
        
        # 1. Save as CSV (flattened data)
        df = self.export_to_dataframe()
        csv_path = f"data/processed/{base_name}.csv"
        df.to_csv(csv_path, index=False, encoding=EXPORT_CONFIG['csv_encoding'])
        print(f"✅ CSV data saved to: {csv_path}")
        
        # 2. Save as JSON (full structured data)
        json_data = []
        for page in self.scraped_pages:
            page_dict = asdict(page)
            # Convert sections to dict
            page_dict['sections'] = [asdict(section) for section in page.sections]
            json_data.append(page_dict)
        
        json_path = f"data/raw/{base_name}_full.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=EXPORT_CONFIG['json_indent'], ensure_ascii=False)
        print(f"✅ JSON data saved to: {json_path}")
        
        # 3. Save statistics (with proper serialization)
        stats_path = f"results/analysis_results/scraping_stats_{timestamp}.json"
        
        # Convert stats to serializable format
        serializable_stats = self._convert_to_serializable(self.stats)
        
        with open(stats_path, 'w') as f:
            json.dump(serializable_stats, f, indent=EXPORT_CONFIG['json_indent'])
        print(f"✅ Statistics saved to: {stats_path}")
        
        return {
            'csv_path': csv_path,
            'json_path': json_path,
            'stats_path': stats_path
        }
    
    def print_scraping_summary(self):
        """Print a comprehensive scraping summary"""
        if not self.stats['start_time']:
            print("❌ No scraping session recorded.")
            return
        
        # Convert string timestamps back to datetime for duration calculation
        start_time = pd.to_datetime(self.stats['start_time'])
        end_time = pd.to_datetime(self.stats['end_time'])
        duration = end_time - start_time
        
        print("\n" + "="*60)
        print("📊 ENHANCED API SCRAPER - SUMMARY REPORT")
        print("="*60)
        print(f"🕒 Duration: {duration}")
        print(f"📄 Total Pages Attempted: {self.stats['total_pages']}")
        print(f"✅ Successful Scrapes: {self.stats['successful_scrapes']}")
        print(f"❌ Failed Scrapes: {self.stats['failed_scrapes']}")
        print(f"📝 Total Words Collected: {self.stats['total_words']:,}")
        
        if self.stats['successful_scrapes'] > 0:
            avg_words = self.stats['total_words'] / self.stats['successful_scrapes']
            success_rate = (self.stats['successful_scrapes'] / self.stats['total_pages']) * 100
            print(f"📊 Average Words per Page: {avg_words:,.0f}")
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        print("="*60)