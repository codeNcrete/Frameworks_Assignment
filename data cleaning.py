# data_cleaning.py
import pandas as pd
import numpy as np
from datetime import datetime

def clean_data(df):
    """Clean and prepare the dataset for analysis"""
    print("Starting data cleaning process...")
    
    # Create a copy to avoid modifying original data
    df_clean = df.copy()
    
    print(f"Original dataset shape: {df_clean.shape}")
    
    # Handle publication dates
    df_clean = handle_dates(df_clean)
    
    # Handle missing values in key columns
    df_clean = handle_missing_values(df_clean)
    
    # Create new features
    df_clean = create_new_features(df_clean)
    
    print(f"Cleaned dataset shape: {df_clean.shape}")
    
    return df_clean

def handle_dates(df):
    """Convert and extract date information"""
    print("Processing date columns...")
    
    # Convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    
    # Extract year and month
    df['publication_year'] = df['publish_time'].dt.year
    df['publication_month'] = df['publish_time'].dt.month
    
    # Fill missing years with mode or reasonable value
    mode_year = df['publication_year'].mode()
    if len(mode_year) > 0:
        df['publication_year'] = df['publication_year'].fillna(mode_year[0])
    
    print(f"Date range: {df['publication_year'].min()} - {df['publication_year'].max()}")
    
    return df

def handle_missing_values(df):
    """Handle missing values in important columns"""
    print("Handling missing values...")
    
    # For title - we can't analyze papers without titles, but let's keep them for now
    df['title'] = df['title'].fillna('Unknown Title')
    
    # For abstract - fill with empty string
    df['abstract'] = df['abstract'].fillna('')
    
    # For journal - fill with 'Unknown Journal'
    df['journal'] = df['journal'].fillna('Unknown Journal')
    
    # Remove rows where both title and abstract are missing
    initial_count = len(df)
    df = df[~(df['title'].isna() & df['abstract'].isna())]
    removed_count = initial_count - len(df)
    print(f"Removed {removed_count} rows with both title and abstract missing")
    
    return df

def create_new_features(df):
    """Create new features for analysis"""
    print("Creating new features...")
    
    # Abstract word count
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))
    
    # Title word count
    df['title_word_count'] = df['title'].apply(lambda x: len(str(x).split()))
    
    # Has abstract flag
    df['has_abstract'] = df['abstract'].apply(lambda x: len(str(x).strip()) > 0)
    
    # Paper source type (simplified)
    df['source_type'] = df['source_x'].fillna('Unknown')
    
    return df

def get_cleaning_report(original_df, cleaned_df):
    """Generate a report of cleaning operations"""
    print("\n=== DATA CLEANING REPORT ===")
    print(f"Original dataset size: {original_df.shape}")
    print(f"Cleaned dataset size: {cleaned_df.shape}")
    print(f"Rows removed: {original_df.shape[0] - cleaned_df.shape[0]}")
    print(f"Columns in cleaned data: {list(cleaned_df.columns)}")
    
    # Check key columns
    key_columns = ['title', 'abstract', 'journal', 'publication_year']
    for col in key_columns:
        missing_pct = (cleaned_df[col].isnull().sum() / len(cleaned_df)) * 100
        print(f"Missing values in {col}: {missing_pct:.2f}%")