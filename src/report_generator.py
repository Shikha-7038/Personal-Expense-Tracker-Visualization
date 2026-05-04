"""
Module: report_generator.py
Purpose: Generate comprehensive expense reports
"""

import pandas as pd
import os
from datetime import datetime

def generate_text_report(df, category_summary, monthly_summary, 
                         payment_summary, kpis, save_path="outputs/reports/expense_report.txt"):
    """
    Generate a text report with all findings
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    category_summary (pandas.DataFrame): Category analysis
    monthly_summary (pandas.DataFrame): Monthly analysis
    payment_summary (pandas.DataFrame): Payment method analysis
    kpis (dict): Key performance indicators
    save_path (str): Path to save the report
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("         PERSONAL EXPENSE TRACKER - DETAILED REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Analysis Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}\n")
        f.write(f"Total Days: {kpis['total_days']}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        # KPIs Section
        f.write("📊 KEY PERFORMANCE INDICATORS (KPIs)\n")
        f.write("-" * 40 + "\n")
        for key, value in kpis.items():
            if 'amount' in key or 'spend' in key or 'expense' in key:
                f.write(f"{key.replace('_', ' ').title():<25}: ₹{value:>15,.2f}\n")
            else:
                f.write(f"{key.replace('_', ' ').title():<25}: {value:>15}\n")
        
        # Category Analysis Section
        f.write("\n" + "=" * 80 + "\n")
        f.write("📂 CATEGORY-WISE SPENDING ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Category':<20} {'Total Spent':>15} {'Transactions':>12} {'Percentage':>12}\n")
        f.write("-" * 60 + "\n")
        for category, row in category_summary.iterrows():
            f.write(f"{category:<20} ₹{row['total_spent']:>12,.2f} {row['transaction_count']:>12} {row['percentage']:>11.1f}%\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'TOTAL':<20} ₹{category_summary['total_spent'].sum():>12,.2f} {category_summary['transaction_count'].sum():>12} {'100.0':>11}%\n")
        
        # Find top category
        top_cat = category_summary.index[0]
        f.write(f"\n💡 Insight: Your highest spending category is '{top_cat}' with ₹{category_summary.loc[top_cat, 'total_spent']:,.2f} ({category_summary.loc[top_cat, 'percentage']:.1f}% of total)\n")
        
        # Monthly Analysis Section
        f.write("\n" + "=" * 80 + "\n")
        f.write("📅 MONTHLY SPENDING TREND\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Month':<12} {'Total Spent':>15} {'Avg/Transaction':>18} {'Transactions':>12} {'MoM Change':>12}\n")
        f.write("-" * 70 + "\n")
        for month, row in monthly_summary.iterrows():
            mom = row.get('mom_change', 0)
            mom_str = f"{mom:+.1f}%" if pd.notna(mom) else "N/A"
            f.write(f"{month:<12} ₹{row['total_spent']:>12,.2f} ₹{row['avg_per_transaction']:>14,.2f} {row['transaction_count']:>12} {mom_str:>12}\n")
        
        # Payment Method Analysis
        f.write("\n" + "=" * 80 + "\n")
        f.write("💳 PAYMENT METHOD BREAKDOWN\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Payment Method':<20} {'Total Spent':>15} {'Transactions':>12} {'Percentage':>12}\n")
        f.write("-" * 60 + "\n")
        for method, row in payment_summary.iterrows():
            f.write(f"{method:<20} ₹{row['total_spent']:>12,.2f} {row['transaction_count']:>12} {row['percentage']:>11.1f}%\n")
        
        # Daily Pattern Analysis
        f.write("\n" + "=" * 80 + "\n")
        f.write("📆 DAILY SPENDING PATTERNS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Average Daily Spend: ₹{kpis['avg_daily_spend']:,.2f}\n")
        f.write(f"Highest Spending Day: {df.loc[df['amount'].idxmax(), 'date'].strftime('%Y-%m-%d')} (₹{df['amount'].max():,.2f})\n")
        f.write(f"Lowest Spending Day: {df.loc[df['amount'].idxmin(), 'date'].strftime('%Y-%m-%d')} (₹{df['amount'].min():,.2f})\n")
        
        # Top 10 Expenses
        f.write("\n" + "=" * 80 + "\n")
        f.write("🔝 TOP 10 LARGEST EXPENSES\n")
        f.write("-" * 40 + "\n")
        top_expenses = df.nlargest(10, 'amount')[['date', 'category', 'amount', 'description', 'payment_method']]
        f.write(f"{'Date':<12} {'Category':<15} {'Amount':>12} {'Description':<25} {'Payment':<10}\n")
        f.write("-" * 75 + "\n")
        for _, row in top_expenses.iterrows():
            f.write(f"{row['date'].strftime('%Y-%m-%d'):<12} {row['category']:<15} ₹{row['amount']:>10,.2f} {row['description'][:24]:<25} {row['payment_method']:<10}\n")
        
        # Spending Recommendations
        f.write("\n" + "=" * 80 + "\n")
        f.write("💡 SPENDING INSIGHTS & RECOMMENDATIONS\n")
        f.write("-" * 40 + "\n")
        
        # Generate insights
        top_cat_pct = category_summary.iloc[0]['percentage']
        if top_cat_pct > 30:
            f.write(f"⚠️  Your '{category_summary.index[0]}' category consumes {top_cat_pct:.1f}% of total spending. Consider reviewing these expenses.\n")
        
        # Check month-over-month increase
        if len(monthly_summary) > 1:
            last_month_change = monthly_summary.iloc[-1].get('mom_change', 0)
            if last_month_change > 10:
                f.write(f"⚠️  Your spending increased by {last_month_change:.1f}% compared to previous month. Review your budget.\n")
        
        # Payment method insight
        if len(payment_summary) > 0:
            top_payment = payment_summary.index[0]
            f.write(f"💳 You predominantly use '{top_payment}' for {payment_summary.iloc[0]['percentage']:.1f}% of transactions.\n")
        
        f.write("\n✅ RECOMMENDATIONS:\n")
        f.write("   1. Set monthly budget limits for each category\n")
        f.write("   2. Track recurring expenses to identify subscriptions\n")
        f.write("   3. Aim to save 20% of your income each month\n")
        f.write("   4. Review weekly spending to stay on track\n")
        f.write("   5. Use cash for discretionary spending to limit overspending\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("Report generated with ❤️ by Personal Expense Tracker\n")
        f.write("=" * 80 + "\n")
    
    print(f"✅ Saved text report: {save_path}")
    return save_path

def generate_csv_report(df, save_path="outputs/reports/expense_details.csv"):
    """
    Export cleaned expense data to CSV
    
    Parameters:
    df (pandas.DataFrame): Cleaned expense data
    save_path (str): Path to save CSV
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Saved CSV report: {save_path}")
    return save_path

if __name__ == "__main__":
    # Test with sample data
    test_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30),
        'category': ['Food'] * 10 + ['Transport'] * 10 + ['Shopping'] * 10,
        'amount': [500, 600, 700, 800, 900, 400, 300, 200, 100, 1000] * 3,
        'description': ['Expense'] * 30,
        'payment_method': ['Card'] * 30,
        'month': ['2024-01'] * 30,
        'weekday': ['Monday'] * 30
    })
    
    test_cat = pd.DataFrame({
        'total_spent': [15000, 10000, 5000],
        'transaction_count': [15, 10, 5],
        'percentage': [50, 33.3, 16.7]
    }, index=['Food', 'Transport', 'Shopping'])
    
    test_monthly = pd.DataFrame({
        'total_spent': [25000, 28000],
        'avg_per_transaction': [500, 560],
        'transaction_count': [50, 50],
        'mom_change': [12, 0]
    }, index=['2024-01', '2024-02'])
    
    test_payment = pd.DataFrame({
        'total_spent': [30000],
        'transaction_count': [30],
        'percentage': [100]
    }, index=['Card'])
    
    test_kpis = {
        'total_expenses': 30000,
        'average_expense': 500,
        'total_transactions': 60,
        'total_days': 30,
        'avg_daily_spend': 1000
    }
    
    generate_text_report(test_df, test_cat, test_monthly, test_payment, test_kpis)