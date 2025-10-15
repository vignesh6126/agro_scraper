import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
from typing import Dict, List, Tuple
import json
import numpy as np
from config.settings import ANALYSIS_CONFIG

class AgricultureDataAnalyzer:
    """
    Advanced analyzer for agriculture Wikipedia data
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.setup_visualizations()
    
    def setup_visualizations(self):
        """Setup visualization parameters"""
        plt.style.use('default')
        sns.set_palette("husl")
        self.colors = px.colors.qualitative.Set3
    
    def _convert_to_serializable(self, obj):
        """
        Convert numpy and pandas objects to JSON-serializable types
        """
        if pd.isna(obj):  # Handle NaN values
            return None
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._convert_to_serializable(value) for key, value in obj.items()}
        elif hasattr(obj, 'isoformat'):  # Handles datetime objects
            return obj.isoformat()
        else:
            return obj
    
    def basic_statistics(self) -> Dict:
        """Calculate basic statistics"""
        stats = {
            'total_pages': int(len(self.df)),
            'total_words': int(self.df['word_count'].sum()),
            'avg_words_per_page': float(self.df['word_count'].mean()),
            'median_words_per_page': float(self.df['word_count'].median()),
            'max_words_page': str(self.df.loc[self.df['word_count'].idxmax()]['title']),
            'max_words_count': int(self.df['word_count'].max()),
            'min_words_page': str(self.df.loc[self.df['word_count'].idxmin()]['title']),
            'min_words_count': int(self.df['word_count'].min()),
            'pages_with_agriculture_categories': int(len(self.df[self.df['categories'].str.contains('agriculture', na=False)])),
            'avg_sections_per_page': float(self.df['sections_count'].mean()),
            'avg_links_per_page': float(self.df['links_count'].mean())
        }
        return stats
    
    def analyze_categories(self) -> pd.DataFrame:
        """Analyze category distribution"""
        all_categories = []
        
        for categories_str in self.df['categories'].dropna():
            if isinstance(categories_str, str):
                categories = categories_str.split(' | ')
                all_categories.extend(categories)
        
        category_counts = Counter(all_categories)
        category_df = pd.DataFrame(category_counts.most_common(), 
                                 columns=['Category', 'Count'])
        
        return category_df
    
    def generate_word_analysis(self, text_column: str = 'summary') -> Dict:
        """Generate word frequency analysis"""
        all_text = ' '.join(self.df[text_column].dropna().astype(str))
        
        # Clean and tokenize text
        words = re.findall(r'\b[a-z]{%d,}\b' % ANALYSIS_CONFIG['min_word_length'], 
                          all_text.lower())
        
        # Common stop words to exclude
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'were', 'which', 
            'their', 'there', 'about', 'other', 'also', 'such', 'these',
            'when', 'what', 'where', 'like', 'such', 'will', 'than'
        }
        
        # Filter words
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = Counter(filtered_words)
        
        # Convert to serializable format
        word_frequency = {word: int(count) for word, count in word_freq.most_common(50)}
        most_common_words = [(word, int(count)) for word, count in word_freq.most_common(20)]
        
        return {
            'total_words': int(len(words)),
            'unique_words': int(len(set(words))),
            'word_frequency': word_frequency,
            'most_common_words': most_common_words
        }
    
    def create_word_cloud(self, text_column: str = 'summary', 
                         save_path: str = None):
        """Create and display word cloud"""
        all_text = ' '.join(self.df[text_column].dropna().astype(str))
        
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=ANALYSIS_CONFIG['wordcloud_max_words'],
            colormap='viridis',
            stopwords=None
        ).generate(all_text)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Agriculture Wikipedia - Word Cloud', fontsize=16, pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Word cloud saved to: {save_path}")
        
        plt.show()
    
    def plot_distributions(self):
        """Plot various distributions"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Word count distribution
        sns.histplot(data=self.df, x='word_count', bins=30, ax=axes[0, 0])
        axes[0, 0].set_title('Distribution of Word Counts')
        axes[0, 0].set_xlabel('Word Count')
        
        # Sections count distribution
        sns.histplot(data=self.df, x='sections_count', bins=20, ax=axes[0, 1])
        axes[0, 1].set_title('Distribution of Sections Count')
        axes[0, 1].set_xlabel('Number of Sections')
        
        # Categories count distribution
        sns.histplot(data=self.df, x='categories_count', bins=20, ax=axes[1, 0])
        axes[1, 0].set_title('Distribution of Categories Count')
        axes[1, 0].set_xlabel('Number of Categories')
        
        # Links count distribution
        sns.histplot(data=self.df, x='links_count', bins=20, ax=axes[1, 1])
        axes[1, 1].set_title('Distribution of Links Count')
        axes[1, 1].set_xlabel('Number of Links')
        
        plt.tight_layout()
        plt.show()
    
    def plot_interactive_charts(self):
        """Create interactive Plotly charts"""
        # Top categories
        top_categories = self.analyze_categories().head(15)
        
        fig1 = px.bar(top_categories, x='Count', y='Category', 
                     title='Top 15 Agriculture-Related Categories',
                     orientation='h', color='Count',
                     color_continuous_scale='viridis')
        fig1.show()
        
        # Word count vs sections
        fig2 = px.scatter(self.df, x='word_count', y='sections_count',
                         size='categories_count', color='links_count',
                         hover_name='title',
                         title='Word Count vs Sections Count',
                         labels={'word_count': 'Word Count', 
                                'sections_count': 'Number of Sections'})
        fig2.show()
    
    def analyze_agriculture_subfields(self) -> Dict:
        """Analyze different subfields of agriculture"""
        subfield_keywords = {
            'Crop Science': ['crop', 'plant', 'harvest', 'yield', 'cultivation', 'breeding'],
            'Livestock & Animals': ['livestock', 'animal', 'cattle', 'poultry', 'dairy', 'meat'],
            'Sustainable Agriculture': ['sustainable', 'organic', 'environment', 'ecological', 'conservation'],
            'Agricultural Technology': ['technology', 'precision', 'irrigation', 'mechanization', 'robot', 'automation'],
            'Agricultural Economics': ['economic', 'market', 'trade', 'price', 'subsidy', 'export'],
            'Soil & Water Management': ['soil', 'water', 'irrigation', 'fertility', 'conservation', 'management']
        }
        
        subfield_analysis = {}
        
        for subfield, keywords in subfield_keywords.items():
            page_count = 0
            word_matches = 0
            
            for summary in self.df['summary'].dropna():
                summary_lower = summary.lower()
                matches = [keyword for keyword in keywords if keyword in summary_lower]
                if matches:
                    page_count += 1
                    word_matches += len(matches)
            
            subfield_analysis[subfield] = {
                'page_count': int(page_count),
                'word_matches': int(word_matches),
                'coverage_percentage': float((page_count / len(self.df)) * 100)
            }
        
        return subfield_analysis
    
    def create_comprehensive_report(self, save_path: str = None) -> Dict:
        """Create a comprehensive analysis report"""
        print("📋 Generating comprehensive analysis report...")
        
        # Gather all analysis
        basic_stats = self.basic_statistics()
        category_analysis = self.analyze_categories()
        word_analysis = self.generate_word_analysis()
        subfield_analysis = self.analyze_agriculture_subfields()
        
        # Convert DataFrames to serializable format
        top_categories_serializable = []
        for _, row in category_analysis.head(10).iterrows():
            top_categories_serializable.append({
                'Category': str(row['Category']),
                'Count': int(row['Count'])
            })
        
        # Convert top pages to serializable format
        top_pages_by_length = []
        for _, row in self.df.nlargest(5, 'word_count')[['title', 'word_count']].iterrows():
            top_pages_by_length.append({
                'title': str(row['title']),
                'word_count': int(row['word_count'])
            })
        
        most_categorized_pages = []
        for _, row in self.df.nlargest(5, 'categories_count')[['title', 'categories_count']].iterrows():
            most_categorized_pages.append({
                'title': str(row['title']),
                'categories_count': int(row['categories_count'])
            })
        
        # Create report with serializable data
        report = {
            'metadata': {
                'analysis_date': pd.Timestamp.now().isoformat(),
                'total_pages_analyzed': int(len(self.df)),
                'data_source': 'Wikipedia API'
            },
            'basic_statistics': basic_stats,
            'top_categories': top_categories_serializable,
            'word_analysis': {
                'most_common_words': word_analysis['most_common_words'],
                'vocabulary_richness': float(word_analysis['unique_words'] / word_analysis['total_words']),
                'total_words_analyzed': word_analysis['total_words'],
                'unique_words_count': word_analysis['unique_words']
            },
            'subfield_analysis': subfield_analysis,
            'top_pages_by_length': top_pages_by_length,
            'most_categorized_pages': most_categorized_pages
        }
        
        # Make sure everything is serializable
        report = self._convert_to_serializable(report)
        
        # Save report if path provided
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"✅ Comprehensive report saved to: {save_path}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
                # Try alternative saving method
                self._save_report_alternative(report, save_path)
        
        return report
    
    def _save_report_alternative(self, report: Dict, save_path: str):
        """Alternative method to save report if primary method fails"""
        try:
            # Convert all values to strings as last resort
            string_report = {}
            for key, value in report.items():
                if isinstance(value, dict):
                    string_report[key] = {k: str(v) for k, v in value.items()}
                else:
                    string_report[key] = str(value)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(string_report, f, indent=2, ensure_ascii=False)
            print(f"✅ Report saved (alternative method) to: {save_path}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
    
    def print_analysis_summary(self):
        """Print a summary of the analysis"""
        stats = self.basic_statistics()
        subfields = self.analyze_agriculture_subfields()
        
        print("\n" + "="*60)
        print("🔍 AGRICULTURE DATA ANALYSIS SUMMARY")
        print("="*60)
        print(f"📊 Basic Statistics:")
        print(f"   • Total Pages: {stats['total_pages']}")
        print(f"   • Total Words: {stats['total_words']:,}")
        print(f"   • Average Words per Page: {stats['avg_words_per_page']:,.0f}")
        print(f"   • Longest Page: {stats['max_words_page']} ({stats['max_words_count']:,} words)")
        
        print(f"\n🌾 Agriculture Subfield Coverage:")
        for subfield, data in sorted(subfields.items(), 
                                   key=lambda x: x[1]['coverage_percentage'], 
                                   reverse=True):
            print(f"   • {subfield}: {data['page_count']} pages ({data['coverage_percentage']:.1f}%)")
        
        print("="*60)