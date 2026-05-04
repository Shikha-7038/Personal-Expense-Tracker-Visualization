"""
Module: dashboard.py
Purpose: Beautiful Streamlit dashboard for expense tracker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data_loader import load_expenses
from src.data_cleaner import clean_expenses

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Expense Tracker Dashboard | Finance Analytics",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS FOR DARK MODERN DESIGN ==============
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hide default Streamlit white background */
    .stApp > header {
        background-color: transparent;
    }
    
    .stAppViewContainer {
        background-color: transparent;
    }
    
    /* Custom sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Card styling with glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
        transform: scale(1.02);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 0.5rem;
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.2rem;
        border-left: 4px solid #4CAF50;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.5rem 0;
    }
    
    .insight-title {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 1px;
    }
    
    .insight-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #4CAF50;
        margin-top: 0.3rem;
    }
    
    .insight-sub {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.2rem;
    }
    
    /* Report period card */
    .report-card {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(33, 150, 243, 0.3);
        text-align: center;
    }
    
    .report-period {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2196F3;
        margin-bottom: 0.5rem;
    }
    
    .report-count {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    /* Headers */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #FFD700, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        margin: 1rem 0;
        padding-left: 0.5rem;
        border-left: 3px solid #FFD700;
    }
    
    /* Custom selectbox styling */
    [data-testid="stSelectbox"] label {
        color: rgba(255, 255, 255, 0.8);
    }
    
    [data-testid="stSelectbox"] div {
        background-color: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    /* Date input styling */
    [data-testid="stDateInput"] label {
        color: rgba(255, 255, 255, 0.8);
    }
    
    [data-testid="stDateInput"] div {
        background-color: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

def load_and_process_data():
    """Load and process expense data"""
    df = load_expenses("data/expenses.csv")
    if df is None:
        st.error("⚠️ No data found! Please run 'python main.py' first to generate data.")
        return None
    
    df_clean = clean_expenses(df)
    return df_clean

def create_beautiful_category_chart(df):
    """Create stunning category bar chart"""
    category_data = df[df['category'] != 'Income'].groupby('category')['amount'].sum().reset_index()
    category_data = category_data.sort_values('amount', ascending=True)
    
    fig = px.bar(
        category_data,
        x='amount',
        y='category',
        orientation='h',
        title='',
        color='amount',
        color_continuous_scale='Viridis',
        labels={'amount': 'Total Spent (₹)', 'category': ''},
        text='amount'
    )
    fig.update_traces(
        texttemplate='₹%{text:,.0f}',
        textposition='outside',
        marker=dict(line=dict(width=0), opacity=0.9),
        hovertemplate='<b>%{y}</b><br>Spent: ₹%{x:,.0f}<extra></extra>'
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='rgba(255,255,255,0.7)')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    return fig

def create_beautiful_monthly_chart(df):
    """Create stunning monthly trend chart"""
    monthly_data = df[df['category'] != 'Income'].copy()
    monthly_data['month'] = pd.to_datetime(monthly_data['date']).dt.strftime('%Y-%m')
    monthly_trend = monthly_data.groupby('month')['amount'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_trend['month'],
        y=monthly_trend['amount'],
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=3, shape='spline'),
        marker=dict(size=10, color='#FFD700', symbol='circle', line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)',
        name='Spending'
    ))
    
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='rgba(255,255,255,0.7)')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Total Spent (₹)'),
        showlegend=False,
        hovermode='x unified'
    )
    return fig

def create_beautiful_payment_chart(df):
    """Create stunning payment method chart"""
    payment_data = df[df['category'] != 'Income'].groupby('payment_method')['amount'].sum().reset_index()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    fig = go.Figure(data=[go.Pie(
        labels=payment_data['payment_method'],
        values=payment_data['amount'],
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='rgba(0,0,0,0.3)', width=2)),
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(size=12, color='white'),
        hoverinfo='label+value',
        hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(font=dict(color='rgba(255,255,255,0.7)'), bgcolor='rgba(0,0,0,0)')
    )
    return fig

def create_beautiful_treemap(df):
    """Create stunning treemap"""
    treemap_data = df[df['category'] != 'Income'].groupby('category')['amount'].sum().reset_index()
    
    fig = px.treemap(
        treemap_data,
        path=['category'],
        values='amount',
        title='',
        color='amount',
        color_continuous_scale='Viridis',
        labels={'amount': 'Spent (₹)'},
        hover_data={'amount': ':,.0f'}
    )
    fig.update_traces(
        textinfo='label+value',
        textfont=dict(size=14, color='white'),
        marker=dict(line=dict(width=1, color='rgba(255,255,255,0.2)'))
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

def create_beautiful_heatmap(df):
    """Create stunning heatmap"""
    daily_data = df[df['category'] != 'Income'].copy()
    daily_data['date'] = pd.to_datetime(daily_data['date'])
    daily_data['day'] = daily_data['date'].dt.day
    daily_data['month'] = daily_data['date'].dt.month
    daily_data['month_name'] = daily_data['date'].dt.strftime('%B')
    
    heatmap_data = daily_data.pivot_table(
        values='amount', 
        index='day', 
        columns='month_name', 
        aggfunc='sum', 
        fill_value=0
    )
    
    fig = px.imshow(
        heatmap_data,
        title='',
        labels=dict(x="", y="Day", color="Spending (₹)"),
        color_continuous_scale='Reds',
        aspect='auto'
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickangle=45)
    )
    return fig

def create_weekday_chart(df):
    """Create weekday spending chart"""
    weekday_data = df[df['category'] != 'Income'].copy()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_spend = weekday_data.groupby('weekday')['amount'].sum().reindex(weekday_order).reset_index()
    
    fig = px.bar(
        weekday_spend,
        x='weekday',
        y='amount',
        title='',
        color='amount',
        color_continuous_scale='Blues',
        labels={'weekday': '', 'amount': 'Total Spent (₹)'},
        text='amount'
    )
    fig.update_traces(
        texttemplate='₹%{text:,.0f}',
        textposition='outside',
        marker=dict(line=dict(width=0), opacity=0.8)
    )
    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.7)')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    return fig

def display_kpi_cards(df):
    """Display KPI metrics in glass cards"""
    total_expenses = df[df['category'] != 'Income']['amount'].sum()
    avg_expense = df[df['category'] != 'Income']['amount'].mean()
    total_transactions = len(df[df['category'] != 'Income'])
    daily_avg = df[df['category'] != 'Income'].groupby('date')['amount'].sum().mean()
    max_expense = df[df['category'] != 'Income']['amount'].max()
    unique_categories = df[df['category'] != 'Income']['category'].nunique()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        (col1, "💰", "Total Expenses", f"₹{total_expenses:,.0f}", f"{len(df)} records"),
        (col2, "📊", "Avg Transaction", f"₹{avg_expense:,.0f}", f"{total_transactions} txns"),
        (col3, "📅", "Daily Average", f"₹{daily_avg:,.0f}", "per day"),
        (col4, "🎯", "Categories", f"{unique_categories}", "total categories"),
        (col5, "🔥", "Highest Spend", f"₹{max_expense:,.0f}", "single transaction"),
        (col6, "💳", "Payment Methods", f"{df['payment_method'].nunique()}", "types used")
    ]
    
    for col, icon, label, value, sub in metrics:
        with col:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 2rem;'>{icon}</div>
                    <div class='metric-value'>{value}</div>
                    <div class='metric-label'>{label}</div>
                    <div style='font-size: 0.7rem; color: rgba(255,255,255,0.4);'>{sub}</div>
                </div>
            """, unsafe_allow_html=True)

def display_beautiful_insights(df):
    """Display insights in beautiful cards"""
    if len(df) == 0:
        return
    
    total_spend = df[df['category'] != 'Income']['amount'].sum()
    top_category = df[df['category'] != 'Income'].groupby('category')['amount'].sum().idxmax()
    top_amount = df[df['category'] != 'Income'].groupby('category')['amount'].sum().max()
    
    # Get month-over-month change
    df_filtered = df[df['category'] != 'Income'].copy()
    df_filtered['month_num'] = pd.to_datetime(df_filtered['date']).dt.month
    monthly_total = df_filtered.groupby('month_num')['amount'].sum()
    if len(monthly_total) > 1:
        mom_change = ((monthly_total.iloc[-1] - monthly_total.iloc[-2]) / monthly_total.iloc[-2]) * 100
        mom_text = f"{mom_change:+.1f}% vs last month"
        mom_color = "#4CAF50" if mom_change < 0 else "#FF6B6B"
    else:
        mom_text = "Need more data"
        mom_color = "rgba(255,255,255,0.6)"
    
    # Busiest day
    busiest_day = df[df['category'] != 'Income']['weekday'].mode()[0] if len(df) > 0 else "N/A"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='insight-card'>
                <div class='insight-title'>🎯 TOP SPENDING CATEGORY</div>
                <div class='insight-value'>{top_category}</div>
                <div class='insight-sub'>₹{top_amount:,.0f} ({top_amount/total_spend*100:.1f}% of total)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='insight-card'>
                <div class='insight-title'>📈 MONTHLY TREND</div>
                <div class='insight-value' style='color: {mom_color};'>{mom_text}</div>
                <div class='insight-sub'>Total: ₹{monthly_total.iloc[-1]:,.0f} this month</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='insight-card'>
                <div class='insight-title'>⏰ PEAK SPENDING DAY</div>
                <div class='insight-value'>{busiest_day}</div>
                <div class='insight-sub'>Most transactions happen on this day</div>
            </div>
        """, unsafe_allow_html=True)

def run_dashboard():
    """Main dashboard function"""
    
    # Header
    st.markdown('<div class="main-title">💰 Personal Finance Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.5); margin-bottom: 2rem;'>Track, Analyze, and Optimize Your Spending</p>", unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading your financial data..."):
        df = load_and_process_data()
    
    if df is None:
        st.warning("⚠️ Please run 'python main.py' first to generate expense data.")
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 3rem;'>📊</div>
                <div style='font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem;'>Control Panel</div>
                <div style='font-size: 0.8rem; color: rgba(255,255,255,0.5);'>Filter your data</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Date range filter
        min_date = pd.to_datetime(df['date']).min()
        max_date = pd.to_datetime(df['date']).max()
        
        start_date = st.date_input("📅 Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("📅 End Date", max_date, min_value=min_date, max_value=max_date)
        
        st.markdown("---")
        
        # Category filter
        categories = ['All'] + sorted(df[df['category'] != 'Income']['category'].unique().tolist())
        selected_category = st.selectbox("🏷️ Category Filter", categories)
        
        # Payment method filter
        payment_methods = ['All'] + sorted(df['payment_method'].unique().tolist())
        selected_payment = st.selectbox("💳 Payment Method", payment_methods)
        
        # Apply filters
        mask = (pd.to_datetime(df['date']) >= pd.to_datetime(start_date)) & \
               (pd.to_datetime(df['date']) <= pd.to_datetime(end_date))
        
        if selected_category != 'All':
            mask = mask & (df['category'] == selected_category)
        
        if selected_payment != 'All':
            mask = mask & (df['payment_method'] == selected_payment)
        
        filtered_df = df[mask].copy()
        
        st.markdown("---")
        
        # Summary card in sidebar
        total_filtered = filtered_df[filtered_df['category'] != 'Income']['amount'].sum()
        st.markdown(f"""
            <div class='report-card'>
                <div class='report-period'>📊 Current View</div>
                <div class='report-count'>₹{total_filtered:,.0f} total</div>
                <div class='report-count'>{len(filtered_df[filtered_df['category'] != 'Income'])} transactions</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✨ Overview", "📈 Analytics", "🎯 Categories", "📅 Calendar", "📋 Reports"
    ])
    
    with tab1:
        st.markdown('<div class="section-header">📊 Financial Overview</div>', unsafe_allow_html=True)
        
        # KPI Cards
        display_kpi_cards(filtered_df)
        
        st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
        display_beautiful_insights(filtered_df)
        
        # Charts row
        st.markdown('<div class="section-header">📈 Spending Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Category Breakdown")
            st.plotly_chart(create_beautiful_category_chart(filtered_df), use_container_width=True, key="cat_chart")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 💳 Payment Distribution")
            st.plotly_chart(create_beautiful_payment_chart(filtered_df), use_container_width=True, key="pay_chart")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-header">📈 Trend Analytics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📅 Monthly Spending Trend")
            st.plotly_chart(create_beautiful_monthly_chart(filtered_df), use_container_width=True, key="month_chart")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Day of Week Pattern")
            st.plotly_chart(create_weekday_chart(filtered_df), use_container_width=True, key="week_chart")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🗺️ Spending Treemap")
        st.plotly_chart(create_beautiful_treemap(filtered_df), use_container_width=True, key="treemap")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-header">🎯 Detailed Category Analysis</div>', unsafe_allow_html=True)
        
        # Category breakdown table
        category_breakdown = filtered_df[filtered_df['category'] != 'Income'].groupby('category').agg({
            'amount': ['sum', 'mean', 'count']
        }).round(2)
        category_breakdown.columns = ['Total Spent', 'Average', 'Transactions']
        category_breakdown = category_breakdown.sort_values('Total Spent', ascending=False)
        
        total = category_breakdown['Total Spent'].sum()
        category_breakdown['Percentage'] = (category_breakdown['Total Spent'] / total * 100).round(1)
        
        # Style the dataframe
        styled_df = category_breakdown.style.format({
            'Total Spent': '₹{:,.0f}',
            'Average': '₹{:,.0f}',
            'Percentage': '{:.1f}%'
        }).background_gradient(cmap='YlOrRd', subset=['Total Spent'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Category time series
        st.markdown("---")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Category Spending Over Time")
        
        time_category = st.selectbox(
            "Select Category to Analyze",
            options=sorted(filtered_df[filtered_df['category'] != 'Income']['category'].unique()),
            key="time_cat"
        )
        
        category_time = filtered_df[filtered_df['category'] == time_category].copy()
        category_time['month'] = pd.to_datetime(category_time['date']).dt.strftime('%Y-%m')
        monthly_category = category_time.groupby('month')['amount'].sum().reset_index()
        
        fig = px.area(
            monthly_category,
            x='month',
            y='amount',
            title=f'',
            labels={'month': '', 'amount': 'Spent (₹)'},
            color_discrete_sequence=['#FF6B6B']
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True, key="cat_time")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-header">📅 Calendar Analytics</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🌡️ Daily Spending Heatmap")
        st.plotly_chart(create_beautiful_heatmap(filtered_df), use_container_width=True, key="heatmap")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Daily Spending Breakdown")
        
        daily_spending = filtered_df[filtered_df['category'] != 'Income'].groupby('date')['amount'].sum().reset_index()
        daily_spending = daily_spending.sort_values('date')
        
        fig = px.bar(
            daily_spending,
            x='date',
            y='amount',
            title='',
            labels={'date': '', 'amount': 'Spent (₹)'},
            color='amount',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(tickangle=45)
        )
        st.plotly_chart(fig, use_container_width=True, key="daily_bar")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="section-header">📋 Detailed Reports</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🔝 Top 10 Expenses")
            top_expenses = filtered_df.nlargest(10, 'amount')[['date', 'category', 'amount', 'description', 'payment_method']]
            st.dataframe(top_expenses, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Statistical Summary")
            stats = filtered_df[filtered_df['category'] != 'Income']['amount'].describe().round(2)
            stats_df = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Min', 'Max', 'Std Dev'],
                'Value': [stats['mean'], stats['50%'], stats['min'], stats['max'], stats['std']]
            })
            stats_df['Value'] = stats_df['Value'].apply(lambda x: f'₹{x:,.0f}')
            st.dataframe(stats_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown("---")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📥 Export Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_full = filtered_df.to_csv(index=False)
            st.download_button(
                label="📄 Export Full Data (CSV)",
                data=csv_full,
                file_name=f"expense_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            summary = filtered_df[filtered_df['category'] != 'Income'].groupby('category')['amount'].sum().to_frame()
            csv_summary = summary.to_csv()
            st.download_button(
                label="📊 Export Category Summary",
                data=csv_summary,
                file_name=f"category_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            top_expenses_csv = filtered_df.nlargest(20, 'amount').to_csv(index=False)
            st.download_button(
                label="🔥 Export Top 20 Expenses",
                data=top_expenses_csv,
                file_name=f"top_expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
        <div class='footer'>
            Built with ❤️ using Python, Pandas, Plotly & Streamlit | Data Period: {start_date} to {end_date}
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main entry point"""
    run_dashboard()

if __name__ == "__main__":
    main()