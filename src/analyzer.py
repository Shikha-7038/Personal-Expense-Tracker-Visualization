"""
Module: analyzer.py
Purpose: Analyze expense patterns and generate insights
"""

import pandas as pd
import numpy as np

def category_analysis(df):
    """
    Analyze expenses by category
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    
    Returns:
    pandas.DataFrame: Category-wise summary
    """
    category_summary = df.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    
    category_summary.columns = ['total_spent', 'avg_per_transaction', 'transaction_count']
    category_summary = category_summary.sort_values('total_spent', ascending=False)
    
    # Add percentage
    total_spent = category_summary['total_spent'].sum()
    category_summary['percentage'] = (category_summary['total_spent'] / total_spent * 100).round(1)
    
    print("\n📊 Category-wise Analysis:")
    print(category_summary)
    
    # Find highest spending category
    top_category = category_summary.index[0]
    top_amount = category_summary.iloc[0]['total_spent']
    print(f"\n🏆 Highest spending category: {top_category} (₹{top_amount:,.2f})")
    
    return category_summary

def monthly_analysis(df):
    """
    Analyze expenses by month
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    
    Returns:
    pandas.DataFrame: Monthly summary
    """
    monthly_summary = df.groupby('month').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    
    monthly_summary.columns = ['total_spent', 'avg_per_transaction', 'transaction_count']
    monthly_summary = monthly_summary.sort_index()
    
    print("\n📅 Monthly Analysis:")
    print(monthly_summary)
    
    # Calculate month-over-month change
    monthly_summary['mom_change'] = monthly_summary['total_spent'].pct_change() * 100
    print("\n📈 Month-over-Month Change (%):")
    print(monthly_summary['mom_change'].round(1))
    
    return monthly_summary

def payment_method_analysis(df):
    """
    Analyze expenses by payment method
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    
    Returns:
    pandas.DataFrame: Payment method summary
    """
    payment_summary = df.groupby('payment_method').agg({
        'amount': ['sum', 'count']
    }).round(2)
    
    payment_summary.columns = ['total_spent', 'transaction_count']
    payment_summary = payment_summary.sort_values('total_spent', ascending=False)
    
    total = payment_summary['total_spent'].sum()
    payment_summary['percentage'] = (payment_summary['total_spent'] / total * 100).round(1)
    
    print("\n💳 Payment Method Analysis:")
    print(payment_summary)
    
    return payment_summary

def daily_analysis(df):
    """
    Analyze daily spending patterns
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    
    Returns:
    pandas.DataFrame: Daily summary
    """
    # Daily totals
    daily_totals = df.groupby('date')['amount'].sum().sort_index()
    
    # Weekday pattern
    weekday_totals = df.groupby('weekday')['amount'].agg(['sum', 'count']).round(2)
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_totals = weekday_totals.reindex(weekday_order)
    
    print("\n📆 Daily Analysis:")
    print(f"   Average daily spend: ₹{daily_totals.mean():,.2f}")
    print(f"   Highest spending day: {daily_totals.idxmax().strftime('%Y-%m-%d')} (₹{daily_totals.max():,.2f})")
    print(f"   Lowest spending day: {daily_totals.idxmin().strftime('%Y-%m-%d')} (₹{daily_totals.min():,.2f})")
    
    print("\n📊 Weekday Pattern:")
    print(weekday_totals)
    
    return daily_totals, weekday_totals

def generate_kpis(df):
    """
    Generate Key Performance Indicators
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    
    Returns:
    dict: KPIs
    """
    kpis = {
        'total_expenses': df['amount'].sum(),
        'average_expense': df['amount'].mean(),
        'median_expense': df['amount'].median(),
        'max_expense': df['amount'].max(),
        'min_expense': df['amount'].min(),
        'total_transactions': len(df),
        'unique_categories': df['category'].nunique(),
        'unique_payment_methods': df['payment_method'].nunique(),
        'total_days': (df['date'].max() - df['date'].min()).days,
        'avg_daily_spend': df['amount'].sum() / max((df['date'].max() - df['date'].min()).days, 1)
    }
    
    print("\n🎯 Key Performance Indicators:")
    for key, value in kpis.items():
        if 'amount' in key or 'spend' in key or 'expense' in key:
            print(f"   {key.replace('_', ' ').title()}: ₹{value:,.2f}")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    return kpis

if __name__ == "__main__":
    # Test with sample data
    sample_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'category': ['Food'] * 10 + ['Transport'] * 10 + ['Shopping'] * 10,
        'amount': np.random.uniform(100, 1000, 30),
        'payment_method': ['Card'] * 15 + ['Cash'] * 15,
        'month': ['2024-01'] * 30,
        'weekday': pd.date_range('2024-01-01', periods=30, freq='D').day_name()
    })
    
    category_analysis(sample_df)
    monthly_analysis(sample_df)
    payment_method_analysis(sample_df)
    generate_kpis(sample_df)