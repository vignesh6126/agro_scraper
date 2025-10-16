"""
Advanced text export with better formatting - UPDATED VERSION
"""

import pandas as pd
import json
from datetime import datetime
import os

class AgricultureTextExporter:
    def __init__(self, csv_path=None):
        # Try to find the CSV file automatically if not provided
        if csv_path is None:
            csv_path = self.find_latest_csv()
        
        if csv_path and os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
            print(f"✅ Loaded dataset: {len(self.df)} pages, {self.df['word_count'].sum():,} words")
        else:
            print("❌ No CSV file found. Please provide a valid path.")
            self.df = pd.DataFrame()
    
    def find_latest_csv(self):
        """Find the most recent agriculture CSV file"""
        possible_paths = [
            "data/processed/agriculture_comprehensive_large.csv",
            "data/processed/agriculture_data.csv", 
            "data/processed/agriculture_comprehensive.csv"
        ]
        
        # Also check for any CSV files in processed directory
        if os.path.exists("data/processed"):
            csv_files = [f for f in os.listdir("data/processed") if f.endswith('.csv') and 'agriculture' in f.lower()]
            if csv_files:
                # Get the most recent file
                csv_files_with_paths = [os.path.join("data/processed", f) for f in csv_files]
                csv_files_with_paths.sort(key=os.path.getmtime, reverse=True)
                possible_paths.extend(csv_files_with_paths)
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def export_comprehensive_report(self):
        """Export comprehensive report with all data"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return None
        
        print("📋 Creating Comprehensive Text Report...")
        
        content = []
        
        # Header
        content.append(" " * 20 + "AGRICULTURE WIKIPEDIA RESEARCH")
        content.append(" " * 25 + "COMPREHENSIVE REPORT")
        content.append("=" * 70)
        content.append("")
        
        # Executive Summary
        content.append("EXECUTIVE SUMMARY")
        content.append("-" * 50)
        content.append(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
        content.append(f"Total Pages Analyzed: {len(self.df)}")
        content.append(f"Total Word Count: {self.df['word_count'].sum():,}")
        content.append(f"Average Page Length: {self.df['word_count'].mean():.0f} words")
        content.append(f"Agriculture Focused Pages: {self.df['is_high_agriculture'].sum() if 'is_high_agriculture' in self.df.columns else 'N/A'}")
        content.append("")
        
        # Page Details
        content.append("PAGE DETAILS")
        content.append("-" * 50)
        content.append("")
        
        for i, row in self.df.iterrows():
            content.append(f"【{i+1}】 {row['title'].upper()}")
            content.append("")
            content.append(f"    📍 Source: {row['url']}")
            content.append(f"    📊 Statistics:")
            content.append(f"        • Words: {row['word_count']:,}")
            content.append(f"        • Categories: {row['categories_count']}")
            content.append(f"        • Sections: {row['sections_count']}")
            content.append(f"        • Links: {row['links_count']}")
            if 'agriculture_score' in row:
                content.append(f"        • Agriculture Score: {row['agriculture_score']:.2f}")
            content.append("")
            content.append("    📖 CONTENT SUMMARY:")
            content.append("    " + "─" * 45)
            
            # Format summary with proper indentation
            summary = str(row['summary']) if pd.notna(row['summary']) else "No summary available"
            wrapped_summary = self.wrap_text(summary, 60)
            for line in wrapped_summary:
                content.append(f"    {line}")
            
            content.append("")
            
            # Categories (if available)
            if pd.notna(row['categories']) and row['categories']:
                content.append("    🏷️ RELATED CATEGORIES:")
                categories = str(row['categories']).split(' | ')[:10]  # First 10 categories
                for cat in categories:
                    content.append(f"        • {cat}")
                content.append("")
            
            content.append("    " + "═" * 50)
            content.append("")
        
        # Comparative Analysis
        content.append("COMPARATIVE ANALYSIS")
        content.append("-" * 50)
        content.append("")
        
        longest_page = self.df.loc[self.df['word_count'].idxmax()]
        shortest_page = self.df.loc[self.df['word_count'].idxmin()]
        
        content.append(f"📈 Longest Page: {longest_page['title']} ({longest_page['word_count']:,} words)")
        content.append(f"📉 Shortest Page: {shortest_page['title']} ({shortest_page['word_count']:,} words)")
        content.append(f"📊 Size Range: {shortest_page['word_count']:,} to {longest_page['word_count']:,} words")
        content.append("")
        
        # Save file
        filename = f"Agriculture_Comprehensive_Report.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Comprehensive report saved: {filename}")
        return filename
    
    def export_for_research(self):
        """Export in research paper format"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return None
        
        print("🎓 Creating Research Format Export...")
        
        content = []
        
        # Research Header
        content.append("RESEARCH DATA: AGRICULTURE-RELATED WIKIPEDIA CONTENT")
        content.append("=" * 70)
        content.append("")
        content.append("ABSTRACT")
        content.append("This document contains scraped data from Wikipedia pages")
        content.append("related to agriculture, including summaries and metadata.")
        content.append("")
        content.append(f"Data Collection Date: {datetime.now().strftime('%Y-%m-%d')}")
        content.append(f"Sample Size: {len(self.df)} pages")
        content.append(f"Total Corpus Size: {self.df['word_count'].sum():,} words")
        content.append("")
        
        # Methodology
        content.append("METHODOLOGY")
        content.append("-" * 30)
        content.append("1. Data sourced from Wikipedia API")
        content.append("2. Pages selected based on agriculture relevance")
        content.append("3. Content extracted includes summaries and metadata")
        content.append("4. Data exported in structured text format")
        content.append("")
        
        # Data Section
        content.append("DATA COLLECTION RESULTS")
        content.append("-" * 30)
        content.append("")
        
        for i, row in self.df.iterrows():
            content.append(f"{i+1}. {row['title']}")
            content.append(f"   URL: {row['url']}")
            content.append(f"   Length: {row['word_count']} words")
            content.append(f"   Structure: {row['sections_count']} sections, {row['categories_count']} categories")
            content.append("")
            content.append("   Content Extract:")
            summary = str(row['summary']) if pd.notna(row['summary']) else "No summary available"
            summary_preview = summary[:300] + "..." if len(summary) > 300 else summary
            wrapped = self.wrap_text(summary_preview, 65)
            for line in wrapped:
                content.append(f"   {line}")
            content.append("")
            content.append("   " + "─" * 40)
            content.append("")
        
        filename = f"Agriculture_Research_Data.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Research format saved: {filename}")
        return filename
    
    def export_minimal(self):
        """Export minimal version for quick reading"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return None
        
        print("📄 Creating Minimal Export...")
        
        content = []
        content.append("AGRICULTURE PAGES - MINIMAL VIEW")
        content.append("=" * 50)
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        content.append(f"Total Pages: {len(self.df)}")
        content.append("")
        
        for i, row in self.df.iterrows():
            content.append(f"→ {row['title']}")
            content.append(f"  📍 {row['url']}")
            content.append(f"  📊 {row['word_count']:,} words")
            content.append("")
            # Very short summary
            summary = str(row['summary']) if pd.notna(row['summary']) else "No summary available"
            short_summary = summary[:150] + "..." if len(summary) > 150 else summary
            wrapped = self.wrap_text(short_summary, 65)
            for line in wrapped:
                content.append(f"  {line}")
            content.append("")
        
        filename = f"Agriculture_Minimal_View.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Minimal export saved: {filename}")
        return filename
    
    def export_simple_list(self):
        """Export simple list format - easiest for Notepad"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return None
        
        print("📝 Creating Simple List Export...")
        
        content = []
        content.append("AGRICULTURE WIKIPEDIA PAGES - SIMPLE LIST")
        content.append("=" * 50)
        content.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        content.append(f"Total Pages: {len(self.df)}")
        content.append(f"Total Words: {self.df['word_count'].sum():,}")
        content.append("")
        
        for i, row in self.df.iterrows():
            content.append(f"{i+1}. {row['title']}")
            content.append(f"   URL: {row['url']}")
            content.append(f"   Words: {row['word_count']:,}")
            content.append(f"   Summary: {str(row['summary']) if pd.notna(row['summary']) else 'No summary'}")
            content.append("")
        
        filename = f"Agriculture_Simple_List.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Simple list saved: {filename}")
        return filename
    
    def export_category_summary(self):
        """Export categorized summary"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return None
        
        print("🏷️ Creating Category Summary Export...")
        
        # Extract and count categories
        all_categories = []
        for categories_str in self.df['categories'].fillna(''):
            if isinstance(categories_str, str):
                categories = categories_str.split(' | ')
                all_categories.extend(categories)
        
        from collections import Counter
        category_counts = Counter(all_categories)
        
        content = []
        content.append("AGRICULTURE CATEGORIES SUMMARY")
        content.append("=" * 50)
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        content.append(f"Total Categories: {len(category_counts)}")
        content.append(f"Total Pages: {len(self.df)}")
        content.append("")
        
        content.append("TOP CATEGORIES:")
        content.append("-" * 30)
        for category, count in category_counts.most_common(20):
            content.append(f"{category}: {count} pages")
        
        content.append("")
        content.append("PAGES BY CATEGORY:")
        content.append("-" * 30)
        
        # Group pages by their first category
        for category in list(category_counts.keys())[:15]:  # Top 15 categories
            content.append("")
            content.append(f"CATEGORY: {category}")
            content.append("-" * 40)
            
            category_pages = []
            for i, row in self.df.iterrows():
                if pd.notna(row['categories']) and category in str(row['categories']):
                    category_pages.append((row['title'], row['word_count']))
            
            for title, word_count in category_pages[:10]:  # Show first 10 pages per category
                content.append(f"  • {title} ({word_count:,} words)")
        
        filename = f"Agriculture_Category_Summary.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Category summary saved: {filename}")
        return filename
    
    def wrap_text(self, text, width=70):
        """Wrap text to specified width"""
        import textwrap
        if not text:
            return [""]
        return textwrap.fill(str(text), width=width).split('\n')
    
    def export_all_formats(self):
        """Export all formats at once"""
        if self.df.empty:
            print("❌ No data available. Please load a valid CSV file first.")
            return []
        
        print("🔄 Exporting all text formats...")
        
        files = []
        files.append(self.export_comprehensive_report())
        files.append(self.export_for_research())
        files.append(self.export_minimal())
        files.append(self.export_simple_list())
        files.append(self.export_category_summary())
        
        print(f"\n✅ All formats exported: {len([f for f in files if f])} files created")
        return [f for f in files if f]

def main():
    """Main function for advanced export"""
    print("🌾 ADVANCED TEXT EXPORT FOR AGRICULTURE DATA")
    print("=" * 50)
    
    # Auto-detect CSV file or ask for path
    csv_path = None
    
    # Try to find automatically
    exporter = AgricultureTextExporter()
    
    if exporter.df.empty:
        # If auto-detection failed, ask for path
        print("\n📁 Please provide the path to your agriculture CSV file:")
        print("   Example: data/processed/agriculture_comprehensive_large.csv")
        csv_path = input("CSV file path: ").strip()
        
        if not csv_path:
            print("❌ No path provided. Exiting.")
            return
        
        exporter = AgricultureTextExporter(csv_path)
        
        if exporter.df.empty:
            print("❌ Could not load the CSV file. Please check the path.")
            return
    
    print(f"\n✅ Successfully loaded: {len(exporter.df)} agriculture pages")
    print(f"📊 Total words: {exporter.df['word_count'].sum():,}")
    
    print("\n📋 Available Export Formats:")
    print("1. Comprehensive Report (Detailed)")
    print("2. Research Paper Format")
    print("3. Minimal View (Quick Read)")
    print("4. Simple List (Easiest for Notepad)")
    print("5. Category Summary")
    print("6. All Formats")
    
    choice = input("\nChoose option (1-6): ").strip()
    
    if choice == '1':
        exporter.export_comprehensive_report()
    elif choice == '2':
        exporter.export_for_research()
    elif choice == '3':
        exporter.export_minimal()
    elif choice == '4':
        exporter.export_simple_list()
    elif choice == '5':
        exporter.export_category_summary()
    elif choice == '6':
        exporter.export_all_formats()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()