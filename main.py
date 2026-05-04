"""
Personal Expense Tracker with Data Visualization
Main execution script

Author: Student Project
Date: 2024
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from src.synthetic_data import generate_sample_data, save_to_csv
from src.data_loader import load_expenses, preview_data
from src.data_cleaner import clean_expenses, validate_data
from src.analyzer import (category_analysis, monthly_analysis, 
                          payment_method_analysis, daily_analysis, generate_kpis)
from src.visualizer import (create_category_bar_chart, create_monthly_trend_chart,
                           create_payment_pie_chart, create_daily_trend_chart,
                           create_weekday_chart)
from src.report_generator import generate_text_report, generate_csv_report

def setup_directories():
    """Create necessary directories for the project"""
    directories = [
        'data',
        'outputs/charts',
        'outputs/reports',
        'images',
        'notebooks'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Created project directories")

def run_pipeline():
    """
    Execute the complete expense tracking pipeline
    """
    print("=" * 60)
    print("   PERSONAL EXPENSE TRACKER WITH DATA VISUALIZATION")
    print("=" * 60)
    
    # Step 1: Setup directories
    print("\n📁 Step 1: Setting up directories...")
    setup_directories()
    
    # Step 2: Generate or load data
    print("\n📊 Step 2: Loading expense data...")
    
    if not os.path.exists("data/expenses.csv"):
        print("   No existing data found. Generating synthetic data...")
        df = generate_sample_data()
    else:
        df = load_expenses()
        if df is None:
            print("   Generating new synthetic data...")
            df = generate_sample_data()
    
    # Step 3: Clean data
    print("\n🧹 Step 3: Cleaning data...")
    df_clean = clean_expenses(df)
    validate_data(df_clean)
    
    # Step 4: Analyze data
    print("\n📈 Step 4: Analyzing data...")
    category_summary = category_analysis(df_clean)
    monthly_summary = monthly_analysis(df_clean)
    payment_summary = payment_method_analysis(df_clean)
    daily_totals, weekday_totals = daily_analysis(df_clean)
    kpis = generate_kpis(df_clean)
    
    # Step 5: Create visualizations
    print("\n🎨 Step 5: Creating visualizations...")
    
    # Category bar chart
    create_category_bar_chart(category_summary)
    
    # Monthly trend chart
    create_monthly_trend_chart(monthly_summary)
    
    # Payment method pie chart
    create_payment_pie_chart(payment_summary)
    
    # Daily trend chart
    create_daily_trend_chart(daily_totals)
    
    # Weekday pattern chart
    create_weekday_chart(weekday_totals)
    
    # Step 6: Generate reports
    print("\n📝 Step 6: Generating reports...")
    
    # Text report
    generate_text_report(df_clean, category_summary, monthly_summary, 
                        payment_summary, kpis)
    
    # CSV export
    generate_csv_report(df_clean)
    
    # Step 7: Final summary
    print("\n" + "=" * 60)
    print("   PROJECT COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\n📁 OUTPUT FILES GENERATED:")
    print("   ├── data/expenses.csv - Raw expense data")
    print("   ├── outputs/charts/ - All visualization charts")
    print("   │   ├── category_bar.png")
    print("   │   ├── monthly_trend.png")
    print("   │   ├── payment_pie.png")
    print("   │   ├── daily_trend.png")
    print("   │   └── weekday_pattern.png")
    print("   └── outputs/reports/ - Summary reports")
    print("       ├── expense_report.txt")
    print("       └── expense_details.csv")
    
    print("\n💡 KEY INSIGHTS:")
    print(f"   • Total Expenses: ₹{kpis['total_expenses']:,.2f}")
    print(f"   • Average Daily Spend: ₹{kpis['avg_daily_spend']:,.2f}")
    print(f"   • Top Category: {category_summary.index[0]} (₹{category_summary.iloc[0]['total_spent']:,.2f})")
    print(f"   • Total Transactions: {kpis['total_transactions']}")
    
    print("\n✅ All tasks completed! Check the 'outputs' folder for results.")
    
    return df_clean, category_summary, monthly_summary, payment_summary, kpis

def run_quick_analysis():
    """
    Quick analysis without generating new data
    """
    df = load_expenses("data/expenses.csv")
    if df is None:
        print("No data found. Run main pipeline first.")
        return
    
    df_clean = clean_expenses(df)
    category_summary = category_analysis(df_clean)
    monthly_summary = monthly_analysis(df_clean)
    payment_summary = payment_method_analysis(df_clean)
    kpis = generate_kpis(df_clean)
    
    return df_clean, category_summary, monthly_summary, payment_summary, kpis

if __name__ == "__main__":
    # Run the complete pipeline
    results = run_pipeline()
    
    # Optional: Run interactive mode
    print("\n🔧 Interactive mode enabled. Type 'help' for commands.")
    while True:
        cmd = input("\n> ").strip().lower()
        if cmd == 'exit':
            break
        elif cmd == 'help':
            print("Commands: exit, summary, categories, months, payments")
        elif cmd == 'summary':
            print(f"Total: ₹{results[4]['total_expenses']:,.2f} | Transactions: {results[4]['total_transactions']}")
        elif cmd == 'categories':
            print(results[1])
        elif cmd == 'months':
            print(results[2])
        elif cmd == 'payments':
            print(results[3])
        else:
            print("Unknown command. Type 'help' for options.")