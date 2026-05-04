"""
Module: synthetic_data.py
Purpose: Generate synthetic expense data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_expenses(start_date='2024-01-01', end_date='2024-12-31', num_transactions=500):
    """
    Generate synthetic expense data
    
    Parameters:
    start_date (str): Start date for data generation
    end_date (str): End date for data generation
    num_transactions (int): Number of transactions to generate
    
    Returns:
    pandas.DataFrame: Synthetic expense data
    """
    
    # Define categories and their typical amounts and frequencies
    categories = {
        'Food & Dining': {'amount_range': (50, 800), 'weight': 25, 'descriptions': [
            'Restaurant', 'Cafe', 'Lunch', 'Dinner', 'Coffee', 'Snacks', 'Takeout']},
        'Groceries': {'amount_range': (200, 3000), 'weight': 15, 'descriptions': [
            'Supermarket', 'Vegetables', 'Groceries', 'Weekly shopping', 'Fruits']},
        'Transport': {'amount_range': (20, 500), 'weight': 15, 'descriptions': [
            'Uber', 'Ola', 'Metro', 'Bus', 'Fuel', 'Auto', 'Taxi']},
        'Shopping': {'amount_range': (300, 10000), 'weight': 12, 'descriptions': [
            'Amazon', 'Flipkart', 'Clothes', 'Electronics', 'Shoes', 'Accessories']},
        'Entertainment': {'amount_range': (100, 2000), 'weight': 10, 'descriptions': [
            'Netflix', 'Movie', 'Concert', 'Spotify', 'Game', 'OTT Subscription']},
        'Bills & Utilities': {'amount_range': (500, 5000), 'weight': 10, 'descriptions': [
            'Electricity', 'Water', 'Internet', 'Mobile Recharge', 'Gas Bill']},
        'Healthcare': {'amount_range': (100, 2000), 'weight': 5, 'descriptions': [
            'Medicine', 'Doctor', 'Pharmacy', 'Health Checkup', 'Gym']},
        'Education': {'amount_range': (500, 5000), 'weight': 3, 'descriptions': [
            'Course', 'Books', 'School Fee', 'Tuition', 'Online Course']},
        'Other': {'amount_range': (50, 1000), 'weight': 5, 'descriptions': [
            'Misc', 'Gift', 'Donation', 'Service', 'Repair']}
    }
    
    # Payment methods
    payment_methods = ['Card', 'Cash', 'UPI', 'Net Banking']
    payment_weights = [0.4, 0.2, 0.35, 0.05]
    
    # Generate date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    total_days = (end - start).days
    
    # Create list to store transactions
    transactions = []
    
    # Generate transactions based on weights
    category_list = []
    for cat, info in categories.items():
        category_list.extend([cat] * info['weight'])
    
    for i in range(num_transactions):
        # Random date within range
        random_days = random.randint(0, total_days)
        date = start + timedelta(days=random_days)
        
        # Select category based on weight
        category = random.choice(category_list)
        cat_info = categories[category]
        
        # Generate amount
        amount = random.randint(cat_info['amount_range'][0], cat_info['amount_range'][1])
        
        # Add weekend effect (higher spending on weekends)
        if date.weekday() >= 5:  # Saturday or Sunday
            amount = int(amount * random.uniform(1.2, 1.8))
        
        # Select description
        description = random.choice(cat_info['descriptions'])
        
        # Add variety to description
        if random.random() > 0.7:
            description = f"{description} - {random.choice(['Bill', 'Payment', 'Purchase', 'Expense'])}"
        
        # Select payment method
        payment_method = random.choices(payment_methods, weights=payment_weights)[0]
        
        # Add occasional notes
        note = ""
        if random.random() > 0.8:
            note = random.choice(['Weekly expense', 'Monthly expense', 'Urgent purchase', 'Planned expense'])
        
        transactions.append({
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'amount': amount,
            'description': description,
            'payment_method': payment_method,
            'note': note
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

def generate_monthly_income(df, income_amount=50000, income_day=1):
    """
    Add monthly income entries to the expense data
    
    Parameters:
    df (pandas.DataFrame): Expense dataframe
    income_amount (int): Monthly income amount
    income_day (int): Day of month when income is received
    
    Returns:
    pandas.DataFrame: Data with income entries
    """
    # Get unique months from expenses
    df['date_obj'] = pd.to_datetime(df['date'])
    months = df['date_obj'].dt.to_period('M').unique()
    
    income_entries = []
    for month in months:
        # Create income date (first or specified day of month)
        income_date = pd.Period(month).start_time + timedelta(days=income_day - 1)
        
        # Add some variation (bonus or deduction)
        actual_income = income_amount
        if random.random() > 0.8:
            actual_income = income_amount + random.randint(-5000, 10000)
        
        income_entries.append({
            'date': income_date.strftime('%Y-%m-%d'),
            'category': 'Income',
            'amount': actual_income,
            'description': 'Monthly Salary',
            'payment_method': 'Bank Transfer',
            'note': 'Income'
        })
    
    # Append income to expenses
    income_df = pd.DataFrame(income_entries)
    df = pd.concat([df, income_df], ignore_index=True)
    
    # Make income amounts negative (or keep positive for expenses)
    # We'll track expenses as positive, income as positive but with category 'Income'
    
    return df

def save_to_csv(df, file_path="data/expenses.csv"):
    """
    Save dataframe to CSV
    
    Parameters:
    df (pandas.DataFrame): Data to save
    file_path (str): Path to save CSV
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"✅ Saved {len(df)} records to {file_path}")
    return file_path

def generate_sample_data():
    """
    Generate complete sample dataset for the project
    """
    print("🔄 Generating synthetic expense data...")
    
    # Generate expenses for current year
    df = generate_expenses(
        start_date='2024-01-01',
        end_date='2024-12-31',
        num_transactions=750
    )
    
    # Add monthly income
    df = generate_monthly_income(df, income_amount=45000, income_day=5)
    
    # Save to CSV
    save_to_csv(df)
    
    # Display summary
    print("\n📊 Data Summary:")
    print(f"   Total records: {len(df)}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Categories: {df['category'].nunique()}")
    print(f"   Total spending: ₹{df[df['category'] != 'Income']['amount'].sum():,.2f}")
    print(f"   Total income: ₹{df[df['category'] == 'Income']['amount'].sum():,.2f}")
    
    return df

if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data()
    
    # Preview
    print("\n📋 Preview of generated data:")
    print(df.head(10))