# main.py
"""
CORD-19 Data Analysis Project
Author: [Your Name]
Date: [Current Date]

This project analyzes the CORD-19 dataset containing COVID-19 research papers.
The analysis includes data exploration, cleaning, visualization, and an interactive web app.
"""

from data_loading import load_and_explore_data, check_missing_values, basic_statistics
from data_cleaning import clean_data, get_cleaning_report
from analysis_visualization import analyze_publication_trends, analyze_titles, analyze_sources, generate_analysis_report

def main():
    """Main execution function"""
    print("CORD-19 DATA ANALYSIS PROJECT")
    print("=" * 50)
    
    # Part 1: Data Loading and Exploration
    print("\nPART 1: DATA LOADING AND EXPLORATION")
    df = load_and_explore_data('metadata.csv')
    missing_df = check_missing_values(df)
    numerical_cols = basic_statistics(df)
    
    # Part 2: Data Cleaning
    print("\nPART 2: DATA CLEANING")
    df_clean = clean_data(df)
    get_cleaning_report(df, df_clean)
    
    # Part 3: Analysis and Visualization
    print("\nPART 3: ANALYSIS AND VISUALIZATION")
    yearly_counts, top_journals = analyze_publication_trends(df_clean)
    common_words = analyze_titles(df_clean)
    top_sources = analyze_sources(df_clean)
    
    # Generate final report
    generate_analysis_report(df_clean, yearly_counts, top_journals, top_sources)
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Run 'streamlit run app.py' to launch the interactive web application")
    print("2. Check the generated visualizations in the plots folder")
    print("3. Review the analysis report above for key insights")

if __name__ == "__main__":
    main()