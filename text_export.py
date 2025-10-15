"""
Advanced text export with better formatting
"""

import pandas as pd
import json
from datetime import datetime

class AgricultureTextExporter:
    def __init__(self):
        self.df = pd.read_csv('data/processed/agriculture_data.csv')
    
    def export_comprehensive_report(self):
        """Export comprehensive report with all data"""
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
            content.append("")
            content.append("    📖 CONTENT SUMMARY:")
            content.append("    " + "─" * 45)
            
            # Format summary with proper indentation
            summary = row['summary']
            wrapped_summary = self.wrap_text(summary, 60)
            for line in wrapped_summary:
                content.append(f"    {line}")
            
            content.append("")
            
            # Categories (if available)
            if pd.notna(row['categories']) and row['categories']:
                content.append("    🏷️ RELATED CATEGORIES:")
                categories = row['categories'].split(' | ')[:10]  # First 10 categories
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
            summary_preview = row['summary'][:300] + "..." if len(row['summary']) > 300 else row['summary']
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
        print("📄 Creating Minimal Export...")
        
        content = []
        content.append("AGRICULTURE PAGES - MINIMAL VIEW")
        content.append("=" * 50)
        content.append("")
        
        for i, row in self.df.iterrows():
            content.append(f"→ {row['title']}")
            content.append(f"  Words: {row['word_count']:,}")
            content.append(f"  URL: {row['url']}")
            content.append("")
            # Very short summary
            short_summary = row['summary'][:150] + "..." if len(row['summary']) > 150 else row['summary']
            content.append(f"  {short_summary}")
            content.append("")
        
        filename = f"Agriculture_Minimal.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Minimal export saved: {filename}")
        return filename
    
    def wrap_text(self, text, width=70):
        """Wrap text to specified width"""
        import textwrap
        return textwrap.fill(text, width=width).split('\n')
    
    def export_all_formats(self):
        """Export all formats at once"""
        print("🔄 Exporting all text formats...")
        
        files = []
        files.append(self.export_comprehensive_report())
        files.append(self.export_for_research())
        files.append(self.export_minimal())
        
        print(f"\n✅ All formats exported: {len(files)} files created")
        return files

def main():
    """Main function for advanced export"""
    print("🌾 ADVANCED TEXT EXPORT FOR AGRICULTURE DATA")
    print("=" * 50)
    
    try:
        exporter = AgricultureTextExporter()
        
        print("\n📋 Available Export Formats:")
        print("1. Comprehensive Report (Detailed)")
        print("2. Research Paper Format")
        print("3. Minimal View (Quick Read)")
        print("4. All Formats")
        
        choice = input("\nChoose format (1-4): ").strip()
        
        if choice == '1':
            exporter.export_comprehensive_report()
        elif choice == '2':
            exporter.export_for_research()
        elif choice == '3':
            exporter.export_minimal()
        elif choice == '4':
            exporter.export_all_formats()
        else:
            print("❌ Invalid choice")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()