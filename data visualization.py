# analysis_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

def analyze_publication_trends(df):
    """Analyze publication trends over time"""
    print("Analyzing publication trends...")
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Publications by year
    plt.subplot(2, 2, 1)
    yearly_counts = df['publication_year'].value_counts().sort_index()
    yearly_counts = yearly_counts[yearly_counts.index >= 2019]  # Focus on recent years
    
    plt.bar(yearly_counts.index, yearly_counts.values)
    plt.title('COVID-19 Publications by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)
    
    # Plot 2: Top journals
    plt.subplot(2, 2, 2)
    top_journals = df['journal'].value_counts().head(10)
    plt.barh(range(len(top_journals)), top_journals.values)
    plt.yticks(range(len(top_journals)), top_journals.index)
    plt.title('Top 10 Journals by Publication Count')
    plt.xlabel('Number of Publications')
    
    # Plot 3: Abstract word count distribution
    plt.subplot(2, 2, 3)
    plt.hist(df[df['abstract_word_count'] > 0]['abstract_word_count'], bins=50, alpha=0.7)
    plt.title('Distribution of Abstract Word Count')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    
    # Plot 4: Papers with/without abstracts
    plt.subplot(2, 2, 4)
    has_abstract_counts = df['has_abstract'].value_counts()
    plt.pie(has_abstract_counts.values, labels=['Has Abstract', 'No Abstract'], autopct='%1.1f%%')
    plt.title('Papers with Abstracts')
    
    plt.tight_layout()
    plt.show()
    
    return yearly_counts, top_journals

def analyze_titles(df):
    """Analyze paper titles and create word cloud"""
    print("Analyzing paper titles...")
    
    # Combine all titles
    all_titles = ' '.join(df['title'].dropna().astype(str))
    
    # Clean the text
    words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by', 
                 'from', 'as', 'an', 'at', 'that', 'this', 'is', 'are', 'was', 'were',
                 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
    
    filtered_words = [word for word in words if word not in stop_words]
    
    # Get most common words
    word_freq = Counter(filtered_words)
    common_words = word_freq.most_common(20)
    
    # Plot common words
    plt.figure(figsize=(12, 8))
    
    plt.subplot(1, 2, 1)
    words, counts = zip(*common_words)
    plt.barh(range(len(words)), counts)
    plt.yticks(range(len(words)), words)
    plt.title('Top 20 Most Common Words in Titles')
    plt.xlabel('Frequency')
    
    # Create word cloud
    plt.subplot(1, 2, 2)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Paper Titles')
    
    plt.tight_layout()
    plt.show()
    
    return common_words

def analyze_sources(df):
    """Analyze paper sources"""
    print("Analyzing paper sources...")
    
    plt.figure(figsize=(12, 6))
    
    # Top sources
    top_sources = df['source_x'].value_counts().head(15)
    
    plt.bar(range(len(top_sources)), top_sources.values)
    plt.xticks(range(len(top_sources)), top_sources.index, rotation=45, ha='right')
    plt.title('Top 15 Sources by Publication Count')
    plt.xlabel('Source')
    plt.ylabel('Number of Publications')
    plt.tight_layout()
    plt.show()
    
    return top_sources

def generate_analysis_report(df, yearly_counts, top_journals, top_sources):
    """Generate a comprehensive analysis report"""
    print("\n" + "="*50)
    print("COMPREHENSIVE ANALYSIS REPORT")
    print("="*50)
    
    print(f"\nTotal papers analyzed: {len(df):,}")
    print(f"Time period: {yearly_counts.index.min()} - {yearly_counts.index.max()}")
    
    print(f"\nPublication peak year: {yearly_counts.idxmax()} with {yearly_counts.max():,} papers")
    
    print(f"\nTop 5 Journals:")
    for i, (journal, count) in enumerate(top_journals.head().items(), 1):
        print(f"  {i}. {journal}: {count:,} papers")
    
    print(f"\nTop 5 Sources:")
    for i, (source, count) in enumerate(top_sources.head().items(), 1):
        print(f"  {i}. {source}: {count:,} papers")
    
    print(f"\nPapers with abstracts: {df['has_abstract'].sum():,} ({df['has_abstract'].mean()*100:.1f}%)")
    print(f"Average abstract length: {df[df['abstract_word_count'] > 0]['abstract_word_count'].mean():.1f} words")