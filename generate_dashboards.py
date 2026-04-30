"""
Business Analytics Dashboard Generator
Generates two interactive dashboards: Customer Analytics and Financial Analytics
Exports as standalone HTML files for GitHub Pages deployment
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import os

# Ensure dashboard directory exists
os.makedirs('dashboard', exist_ok=True)

print("🚀 Starting Business Analytics Dashboard Generation...")

# ============================================================================
# 1. CUSTOMER ANALYTICS DASHBOARD
# ============================================================================
print("\n📊 Generating Customer Analytics Dashboard...")

# Generate synthetic retail dataset
np.random.seed(42)
num_records = 500

# Create sample data
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
regions = ['North', 'South', 'East', 'West', 'Central']
dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')

data = {
    'Date': np.random.choice(dates, num_records),
    'Category': np.random.choice(categories, num_records),
    'Region': np.random.choice(regions, num_records),
    'Sales': np.random.uniform(100, 5000, num_records),
    'Quantity': np.random.randint(1, 50, num_records),
}

df = pd.DataFrame(data)
df = df.sort_values('Date').reset_index(drop=True)

# Aggregate data for visualizations
# 1. Sales by Category
sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

# 2. Sales by Region
sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

# 3. Sales Trend Over Time
sales_trend = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
sales_trend['Date'] = sales_trend['Date'].astype(str)

# Create Customer Analytics Dashboard with multiple subplots
fig_customer = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales by Category', 'Sales by Region', 
                    'Sales Trend Over Time', 'Quantity Distribution'),
    specs=[[{'type': 'bar'}, {'type': 'pie'}],
           [{'type': 'scatter'}, {'type': 'bar'}]]
)

# Subplot 1: Bar chart - Sales by Category
fig_customer.add_trace(
    go.Bar(x=sales_by_category.index, y=sales_by_category.values, 
           name='Sales by Category', marker_color='#1f77b4'),
    row=1, col=1
)

# Subplot 2: Pie chart - Sales by Region
fig_customer.add_trace(
    go.Pie(labels=sales_by_region.index, values=sales_by_region.values, 
           name='Sales by Region'),
    row=1, col=2
)

# Subplot 3: Line chart - Sales Trend
fig_customer.add_trace(
    go.Scatter(x=sales_trend['Date'], y=sales_trend['Sales'], 
               mode='lines+markers', name='Monthly Sales',
               line=dict(color='#2ca02c', width=3)),
    row=2, col=1
)

# Subplot 4: Bar chart - Quantity by Category
quantity_by_category = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
fig_customer.add_trace(
    go.Bar(x=quantity_by_category.index, y=quantity_by_category.values,
           name='Quantity', marker_color='#ff7f0e'),
    row=2, col=2
)

# Update layout
fig_customer.update_layout(
    title_text="📈 Customer Analytics Dashboard",
    height=900,
    showlegend=True,
    hovermode='closest',
    template='plotly_white',
    font=dict(size=12)
)

# Update axes labels
fig_customer.update_xaxes(title_text="Category", row=1, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=1, col=1)
fig_customer.update_xaxes(title_text="Month", row=2, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=2, col=1)
fig_customer.update_xaxes(title_text="Category", row=2, col=2)
fig_customer.update_yaxes(title_text="Quantity", row=2, col=2)

# Export Customer Dashboard
customer_html_path = 'dashboard/customer_dashboard.html'
fig_customer.write_html(customer_html_path)
print(f"✅ Customer Analytics Dashboard saved to: {customer_html_path}")

# ============================================================================
# 2. FINANCIAL ANALYTICS DASHBOARD
# ============================================================================
print("\n📊 Generating Financial Analytics Dashboard...")

# Fetch AAPL stock data for the past year
print("   Fetching AAPL stock data from Yahoo Finance...")
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

aapl_data = yf.download('AAPL', start=start_date, end=end_date, progress=False)
aapl_data = aapl_data.reset_index()

# Calculate moving averages
aapl_data['MA50'] = aapl_data['Close'].rolling(window=50).mean()
aapl_data['MA100'] = aapl_data['Close'].rolling(window=100).mean()

# Create Financial Analytics Dashboard
fig_financial = make_subplots(
    rows=2, cols=1,
    subplot_titles=('AAPL Stock Price with Moving Averages', 'Trading Volume'),
    specs=[[{'secondary_y': False}],
           [{'secondary_y': False}]],
    vertical_spacing=0.15
)

# Subplot 1: Line chart with moving averages
fig_financial.add_trace(
    go.Scatter(x=aapl_data['Date'], y=aapl_data['Close'],
               mode='lines', name='Close Price',
               line=dict(color='#1f77b4', width=2)),
    row=1, col=1
)

fig_financial.add_trace(
    go.Scatter(x=aapl_data['Date'], y=aapl_data['MA50'],
               mode='lines', name='50-Day MA',
               line=dict(color='#ff7f0e', width=2, dash='dash')),
    row=1, col=1
)

fig_financial.add_trace(
    go.Scatter(x=aapl_data['Date'], y=aapl_data['MA100'],
               mode='lines', name='100-Day MA',
               line=dict(color='#2ca02c', width=2, dash='dot')),
    row=1, col=1
)

# Subplot 2: Volume bar chart
fig_financial.add_trace(
    go.Bar(x=aapl_data['Date'], y=aapl_data['Volume'],
           name='Volume', marker_color='#d62728', opacity=0.7),
    row=2, col=1
)

# Update layout
fig_financial.update_layout(
    title_text="💹 Financial Analytics Dashboard - AAPL Stock",
    height=800,
    showlegend=True,
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=12)
)

# Update axes labels
fig_financial.update_xaxes(title_text="Date", row=2, col=1)
fig_financial.update_yaxes(title_text="Price ($)", row=1, col=1)
fig_financial.update_yaxes(title_text="Volume", row=2, col=1)

# Export Financial Dashboard
financial_html_path = 'dashboard/financial_dashboard.html'
fig_financial.write_html(financial_html_path)
print(f"✅ Financial Analytics Dashboard saved to: {financial_html_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("🎉 DASHBOARD GENERATION COMPLETE!")
print("="*70)
print(f"\n📁 Generated Files:")
print(f"   1. {customer_html_path}")
print(f"   2. {financial_html_path}")
print(f"\n🌐 To view dashboards:")
print(f"   - Open the HTML files directly in your browser")
print(f"   - Or access via GitHub Pages at:")
print(f"     https://parthjain171.github.io/Business-Analytics-Zomato/")
print(f"\n💡 Both dashboards are fully standalone and require no external dependencies!")
print("="*70)
