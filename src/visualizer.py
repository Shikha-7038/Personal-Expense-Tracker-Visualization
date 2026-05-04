"""
Module: visualizer.py
Purpose: Create visualizations for expense data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np

# Set style for better looking charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Set font to handle Windows encoding
plt.rcParams['font.sans-serif'] = ['Arial', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_category_bar_chart(category_summary, save_path="outputs/charts/category_bar.png"):
    """
    Create bar chart for category-wise spending
    
    Parameters:
    category_summary (pandas.DataFrame): Category analysis summary
    save_path (str): Path to save the chart
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(category_summary.index, category_summary['total_spent'], 
                   color=sns.color_palette("viridis", len(category_summary)))
    
    # Customize chart (removed emoji)
    plt.title('Category-wise Spending', fontsize=16, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Spent (INR)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, category_summary['total_spent']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f'INR {value:,.0f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved category bar chart: {save_path}")
    return save_path

def create_monthly_trend_chart(monthly_summary, save_path="outputs/charts/monthly_trend.png"):
    """
    Create line chart for monthly spending trend
    
    Parameters:
    monthly_summary (pandas.DataFrame): Monthly analysis summary
    save_path (str): Path to save the chart
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Create line chart with markers
    plt.plot(monthly_summary.index, monthly_summary['total_spent'], 
             marker='o', linewidth=2, markersize=8, color='#2E86AB')
    
    # Fill area under curve
    plt.fill_between(range(len(monthly_summary.index)), monthly_summary['total_spent'], 
                     alpha=0.3, color='#2E86AB')
    
    # Customize chart (removed emoji)
    plt.title('Monthly Spending Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Spent (INR)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels
    for i, (month, amount) in enumerate(zip(monthly_summary.index, monthly_summary['total_spent'])):
        plt.text(i, amount + 100, f'INR {amount:,.0f}', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved monthly trend chart: {save_path}")
    return save_path

def create_payment_pie_chart(payment_summary, save_path="outputs/charts/payment_pie.png"):
    """
    Create pie chart for payment method distribution
    
    Parameters:
    payment_summary (pandas.DataFrame): Payment method summary
    save_path (str): Path to save the chart
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    
    # Create pie chart
    colors = sns.color_palette("pastel", len(payment_summary))
    wedges, texts, autotexts = plt.pie(payment_summary['total_spent'], 
                                        labels=payment_summary.index,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        explode=[0.05] * len(payment_summary))
    
    # Style the text
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title('Payment Method Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved payment pie chart: {save_path}")
    return save_path

def create_daily_trend_chart(daily_totals, save_path="outputs/charts/daily_trend.png"):
    """
    Create daily spending trend chart
    
    Parameters:
    daily_totals (pandas.Series): Daily spending totals
    save_path (str): Path to save the chart
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(14, 6))
    
    # Create bar chart for daily spending
    x_positions = range(len(daily_totals))
    plt.bar(x_positions, daily_totals.values, color='#A23B72', alpha=0.7)
    
    # Add trend line (using numpy polyfit instead of scipy)
    if len(daily_totals) > 1:
        z = np.polyfit(x_positions, daily_totals.values, 1)
        p = np.poly1d(z)
        plt.plot(x_positions, p(x_positions), "r--", linewidth=2, label='Trend Line')
    
    # Customize chart (removed emoji)
    plt.title('Daily Spending Pattern', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Amount Spent (INR)', fontsize=12)
    plt.xticks(x_positions[::max(1, len(x_positions)//10)], 
               [d.strftime('%Y-%m-%d') for d in daily_totals.index[::max(1, len(daily_totals)//10)]], 
               rotation=45)
    plt.legend()
    
    # Add horizontal line for average
    avg_spend = daily_totals.mean()
    plt.axhline(y=avg_spend, color='green', linestyle=':', alpha=0.7, label=f'Average: INR {avg_spend:.0f}')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved daily trend chart: {save_path}")
    return save_path

def create_weekday_chart(weekday_totals, save_path="outputs/charts/weekday_pattern.png"):
    """
    Create weekday spending pattern chart
    
    Parameters:
    weekday_totals (pandas.DataFrame): Weekday totals
    save_path (str): Path to save the chart
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar chart for total spending by weekday
    bars1 = ax1.bar(weekday_totals.index, weekday_totals['sum'], 
                   color=sns.color_palette("coolwarm", len(weekday_totals)))
    ax1.set_title('Total Spending by Weekday', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Weekday')
    ax1.set_ylabel('Total Spent (INR)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars1, weekday_totals['sum']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f'INR {value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # Bar chart for transaction count by weekday
    bars2 = ax2.bar(weekday_totals.index, weekday_totals['count'],
                   color=sns.color_palette("viridis", len(weekday_totals)))
    ax2.set_title('Transaction Count by Weekday', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Weekday')
    ax2.set_ylabel('Number of Transactions')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars2, weekday_totals['count']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{int(value)}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved weekday pattern chart: {save_path}")
    return save_path

if __name__ == "__main__":
    # Test with sample data
    test_categories = pd.DataFrame({
        'total_spent': [50000, 30000, 20000, 15000, 10000],
        'percentage': [40, 24, 16, 12, 8]
    }, index=['Food', 'Transport', 'Shopping', 'Entertainment', 'Bills'])
    
    test_monthly = pd.DataFrame({
        'total_spent': [25000, 28000, 22000, 30000]
    }, index=['2024-01', '2024-02', '2024-03', '2024-04'])
    
    test_payment = pd.DataFrame({
        'total_spent': [45000, 35000, 25000],
        'percentage': [42.9, 33.3, 23.8]
    }, index=['Card', 'UPI', 'Cash'])
    
    test_daily = pd.Series([500, 300, 800, 200, 600, 400, 700], 
                           index=pd.date_range('2024-01-01', periods=7))
    
    create_category_bar_chart(test_categories)
    create_monthly_trend_chart(test_monthly)
    create_payment_pie_chart(test_payment)
    create_daily_trend_chart(test_daily)