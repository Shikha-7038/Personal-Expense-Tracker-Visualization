"""
Module: data_cleaner.py
Purpose: Clean and preprocess expense data
"""

import pandas as pd
import numpy as np

def clean_expenses(df):
    """
    Clean the expense dataframe
    
    Parameters:
    df (pandas.DataFrame): Raw expense data
    
    Returns:
    pandas.DataFrame: Cleaned expense data
    """
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    print("\n🔧 Starting Data Cleaning...")
    
    # 1. Remove duplicates
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"   Removed {initial_count - len(df_clean)} duplicate rows")
    
    # 2. Handle missing values
    df_clean = df_clean.dropna(subset=['amount'])
    df_clean['description'] = df_clean['description'].fillna('No description')
    df_clean['payment_method'] = df_clean['payment_method'].fillna('Cash')
    print(f"   Handled missing values")
    
    # 3. Convert date to datetime
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    print(f"   Converted date column to datetime")
    
    # 4. Ensure amount is numeric and positive (expense amount)
    df_clean['amount'] = pd.to_numeric(df_clean['amount'], errors='coerce')
    df_clean['amount'] = df_clean['amount'].abs()  # Make all amounts positive
    
    # 5. Remove outliers (amounts > 100000 or < 0)
    df_clean = df_clean[(df_clean['amount'] > 0) & (df_clean['amount'] <= 100000)]
    print(f"   Removed outlier amounts")
    
    # 6. Standardize category names
    category_mapping = {
        'food': 'Food & Dining',
        'restaurant': 'Food & Dining',
        'groceries': 'Groceries',
        'grocery': 'Groceries',
        'transport': 'Transport',
        'uber': 'Transport',
        'ola': 'Transport',
        'shopping': 'Shopping',
        'entertainment': 'Entertainment',
        'bills': 'Bills & Utilities',
        'utilities': 'Bills & Utilities',
        'health': 'Healthcare',
        'medical': 'Healthcare',
        'education': 'Education',
        'other': 'Other'
    }
    
    df_clean['category'] = df_clean['category'].str.lower().map(
        lambda x: next((v for k,v in category_mapping.items() if k in str(x)), x.title())
    )
    
    # 7. Extract month and day for analysis
    df_clean['month'] = df_clean['date'].dt.strftime('%Y-%m')
    df_clean['day'] = df_clean['date'].dt.day
    df_clean['weekday'] = df_clean['date'].dt.day_name()
    
    print(f"✅ Cleaning complete! Final records: {len(df_clean)}")
    
    return df_clean

def validate_data(df):
    """
    Validate cleaned data
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    """
    print("\n🔍 Data Validation:")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Categories: {df['category'].nunique()}")
    print(f"   Total expenses: ₹{df['amount'].sum():,.2f}")
    print(f"   Average expense: ₹{df['amount'].mean():,.2f}")

if __name__ == "__main__":
    # Test with sample data
    sample_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'category': ['Food', 'Transport', 'Shopping'],
        'amount': [500, 200, 1000],
        'payment_method': ['Card', 'Cash', 'UPI'],
        'description': ['Lunch', 'Bus fare', 'Clothes']
    })
    cleaned = clean_expenses(sample_data)
    print(cleaned)