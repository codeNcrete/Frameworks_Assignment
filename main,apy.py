# cord19_analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_explore_data(file_path='metadata.csv'):
    """Load the dataset and perform initial exploration"""
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    print("\n=== DATASET BASIC INFORMATION ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Number of rows: {df.shape[0]:,}")
    print(f"Number of columns: {df.shape[1]}")
    
    print("\n=== FIRST FEW ROWS ===")
    print(df.head())
    
    print("\n=== COLUMN DATA TYPES ===")
    print(df.dtypes)
    
    print("\n=== DATASET INFO ===")
    df.info()
    
    return df

def check_missing_values(df):
    """Analyze missing values in the dataset"""
    print("\n=== MISSING VALUES ANALYSIS ===")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Missing Count': missing_data,
        'Missing Percentage': missing_percent
    }).sort_values('Missing Count', ascending=False)
    
    print(missing_df.head(15))
    
    # Plot missing values
    plt.figure(figsize=(12, 6))
    missing_df_head = missing_df.head(10)
    plt.bar(missing_df_head.index, missing_df_head['Missing Percentage'])
    plt.title('Top 10 Columns with Missing Values (%)')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Percentage Missing')
    plt.tight_layout()
    plt.show()
    
    return missing_df

def basic_statistics(df):
    """Generate basic statistics for numerical columns"""
    print("\n=== BASIC STATISTICS ===")
    print(df.describe())
    
    # Check for numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nNumerical columns: {list(numerical_cols)}")
    
    return numerical_cols

if __name__ == "__main__":
    # Load and explore data
    df = load_and_explore_data('metadata.csv')
    
    # Check missing values
    missing_df = check_missing_values(df)
    
    # Basic statistics
    numerical_cols = basic_statistics(df)