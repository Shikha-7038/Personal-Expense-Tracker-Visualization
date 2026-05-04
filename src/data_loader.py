"""
Module: data_loader.py
Purpose: Load expense data from CSV file
"""

import pandas as pd
import os

def load_expenses(file_path="data/expenses.csv"):
    """
    Load expense data from CSV file
    
    Parameters:
    file_path (str): Path to CSV file
    
    Returns:
    pandas.DataFrame: Loaded expense data
    """
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            print("Generating sample data first...")
            return None
        
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} expense records")
        print(f"📊 Columns: {list(df.columns)}")
        return df
    
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def preview_data(df, rows=5):
    """
    Display preview of the data
    
    Parameters:
    df (pandas.DataFrame): Expense data
    rows (int): Number of rows to display
    """
    print("\n📋 Data Preview:")
    print(df.head(rows))
    print("\n📈 Data Info:")
    print(df.info())
    print("\n📊 Statistical Summary:")
    print(df.describe())

if __name__ == "__main__":
    # Test the loader
    df = load_expenses()
    if df is not None:
        preview_data(df)