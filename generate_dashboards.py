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

# Generate synthetic retail dataset with more realistic data
np.random.seed(42)
num_records = 1000

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
sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
sales_trend = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
sales_trend['Date'] = sales_trend['Date'].astype(str)
quantity_by_category = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)

# Create individual figures for better rendering
fig1 = go.Figure(data=[
    go.Bar(x=sales_by_category.index, y=sales_by_category.values,
           marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],
           text=sales_by_category.values.round(0),
           textposition='auto')
])
fig1.update_layout(
    title='Sales by Category',
    xaxis_title='Category',
    yaxis_title='Total Sales ($)',
    template='plotly_white',
    height=400,
    hovermode='x unified'
)

fig2 = go.Figure(data=[
    go.Pie(labels=sales_by_region.index, values=sales_by_region.values,
           marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']))
])
fig2.update_layout(
    title='Sales Distribution by Region',
    template='plotly_white',
    height=400
)

fig3 = go.Figure(data=[
    go.Scatter(x=sales_trend['Date'], y=sales_trend['Sales'],
               mode='lines+markers',
               line=dict(color='#00CC96', width=3),
               marker=dict(size=8),
               fill='tozeroy',
               fillcolor='rgba(0, 204, 150, 0.2)')
])
fig3.update_layout(
    title='Monthly Sales Trend',
    xaxis_title='Month',
    yaxis_title='Total Sales ($)',
    template='plotly_white',
    height=400,
    hovermode='x unified'
)

fig4 = go.Figure(data=[
    go.Bar(x=quantity_by_category.index, y=quantity_by_category.values,
           marker_color='#EF553B',
           text=quantity_by_category.values.round(0),
           textposition='auto')
])
fig4.update_layout(
    title='Total Quantity Sold by Category',
    xaxis_title='Category',
    yaxis_title='Quantity',
    template='plotly_white',
    height=400,
    hovermode='x unified'
)

# Combine all figures into one dashboard
from plotly.subplots import make_subplots

fig_customer = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales by Category', 'Sales Distribution by Region',
                    'Monthly Sales Trend', 'Quantity by Category'),
    specs=[[{'type': 'bar'}, {'type': 'pie'}],
           [{'type': 'scatter'}, {'type': 'bar'}]],
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

# Add traces manually with proper data
fig_customer.add_trace(
    go.Bar(x=sales_by_category.index, y=sales_by_category.values,
           marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],
           name='Sales', showlegend=False),
    row=1, col=1
)

fig_customer.add_trace(
    go.Pie(labels=sales_by_region.index, values=sales_by_region.values,
           marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']),
           name='Region', showlegend=False),
    row=1, col=2
)

fig_customer.add_trace(
    go.Scatter(x=sales_trend['Date'], y=sales_trend['Sales'],
               mode='lines+markers',
               line=dict(color='#00CC96', width=3),
               marker=dict(size=6),
               fill='tozeroy',
               name='Sales', showlegend=False),
    row=2, col=1
)

fig_customer.add_trace(
    go.Bar(x=quantity_by_category.index, y=quantity_by_category.values,
           marker_color='#EF553B',
           name='Quantity', showlegend=False),
    row=2, col=2
)

fig_customer.update_xaxes(title_text="Category", row=1, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=1, col=1)
fig_customer.update_xaxes(title_text="Month", row=2, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=2, col=1)
fig_customer.update_xaxes(title_text="Category", row=2, col=2)
fig_customer.update_yaxes(title_text="Quantity", row=2, col=2)

fig_customer.update_layout(
    title_text="📈 Customer Analytics Dashboard",
    height=900,
    showlegend=False,
    template='plotly_white',
    font=dict(size=12, family="Inter, Arial, sans-serif"),
    margin=dict(l=50, r=50, t=100, b=50)
)

# Export Customer Dashboard
customer_html_path = 'dashboard/customer_dashboard.html'
fig_customer.write_html(customer_html_path)
print(f"✅ Customer Analytics Dashboard saved to: {customer_html_path}")

# ============================================================================
# 2. FINANCIAL ANALYTICS DASHBOARD (FIXED & DEMO-READY)
# ============================================================================
print("\n📊 Generating Financial Analytics Dashboard...")

try:
    print("   Fetching AAPL stock data from Yahoo Finance...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Fetch data (NO silent failure)
    try:
        # For newer yfinance versions
        aapl_data = yf.download('AAPL', start=start_date, end=end_date, multi_level_index=False, progress=False)
    except TypeError:
        # Fallback for older yfinance versions
        aapl_data = yf.download('AAPL', start=start_date, end=end_date, progress=False)

    if aapl_data is None or aapl_data.empty:
        raise ValueError("No data received from Yahoo Finance")

    # Fix MultiIndex columns if present (safely handle various yfinance output formats)
    if isinstance(aapl_data.columns, pd.MultiIndex):
        # Flatten by getting the top level, or taking the price name if it's the second level
        levels = aapl_data.columns.levels
        if 'Close' in levels[0]:
            aapl_data.columns = aapl_data.columns.get_level_values(0)
        elif len(levels) > 1 and 'Close' in levels[1]:
            aapl_data.columns = aapl_data.columns.get_level_values(1)
        else:
            # Fallback string flattening
            aapl_data.columns = [col[0] if isinstance(col, tuple) else col for col in aapl_data.columns]

    aapl_data = aapl_data.reset_index()
    
    # Rename index to Date if necessary
    if 'Date' not in aapl_data.columns and 'Datetime' in aapl_data.columns:
        aapl_data = aapl_data.rename(columns={'Datetime': 'Date'})
    elif 'Date' not in aapl_data.columns and 'index' in aapl_data.columns:
        aapl_data = aapl_data.rename(columns={'index': 'Date'})

    # Ensure correct columns exist
    required_cols = ['Date', 'Close', 'Volume']
    for col in required_cols:
        if col not in aapl_data.columns:
            raise ValueError(f"Missing column: {col}")

    # Clean data: only select relevant columns first to avoid dropping rows due to unrelated NaNs
    aapl_data = aapl_data[['Date', 'Close', 'Volume']].copy()
    aapl_data['Date'] = pd.to_datetime(aapl_data['Date'])
    aapl_data['Close'] = pd.to_numeric(aapl_data['Close'], errors='coerce')
    aapl_data['Volume'] = pd.to_numeric(aapl_data['Volume'], errors='coerce')

    aapl_data = aapl_data.dropna()

    # Ensure sufficient data
    if len(aapl_data) < 100:
        raise ValueError(f"Too few data points: {len(aapl_data)}")

    print(f"   Downloaded {len(aapl_data)} trading days")

    # Moving averages (correct way: avoids misleading early values by leaving them as NaN)
    aapl_data['MA50'] = aapl_data['Close'].rolling(window=50).mean()
    aapl_data['MA100'] = aapl_data['Close'].rolling(window=100).mean()

    # Create subplot: shared_xaxes prevents duplication, properly proportioned
    fig_financial = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('AAPL Stock Price with Moving Averages', 'Trading Volume'),
        vertical_spacing=0.08,
        row_heights=[0.75, 0.25]
    )

    # Price line
    fig_financial.add_trace(
        go.Scatter(
            x=aapl_data['Date'],
            y=aapl_data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#1f77b4', width=2.5)
        ),
        row=1, col=1
    )

    # MA50
    fig_financial.add_trace(
        go.Scatter(
            x=aapl_data['Date'],
            y=aapl_data['MA50'],
            mode='lines',
            name='50-Day MA',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ),
        row=1, col=1
    )

    # MA100
    fig_financial.add_trace(
        go.Scatter(
            x=aapl_data['Date'],
            y=aapl_data['MA100'],
            mode='lines',
            name='100-Day MA',
            line=dict(color='#2ca02c', width=2, dash='dot')
        ),
        row=1, col=1
    )

    # Volume bars
    colors = ['#d62728' if aapl_data.iloc[i]['Close'] < aapl_data.iloc[i-1]['Close'] else '#2ca02c' 
              for i in range(len(aapl_data))]
    colors[0] = '#2ca02c' # First day fallback

    fig_financial.add_trace(
        go.Bar(
            x=aapl_data['Date'],
            y=aapl_data['Volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.8
        ),
        row=2, col=1
    )

    # Layout improvements (IMPORTANT)
    fig_financial.update_layout(
        title="💹 Financial Analytics Dashboard - AAPL (Last 12 Months)",
        height=900,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(size=12, family="Inter, Arial, sans-serif"),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Axis labels
    fig_financial.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig_financial.update_yaxes(title_text="Volume", row=2, col=1)
    
    # 🔥 RANGE SLIDER (properly configured so it doesn't compress the chart)
    fig_financial.update_layout(
        xaxis2=dict(
            title_text="Date",
            rangeslider=dict(
                visible=True,
                thickness=0.08, # Keeps slider small to avoid vertical squash
                bgcolor="#F3F4F6"
            ),
            type="date"
        )
    )

    # Remove rangeslider from top chart explicitly just in case
    fig_financial.update_xaxes(rangeslider_visible=False, row=1, col=1)

    # Export
    financial_html_path = 'dashboard/financial_dashboard.html'
    fig_financial.write_html(financial_html_path)

    print(f"✅ Financial Dashboard saved to: {financial_html_path}")

except Exception as e:
    print(f"⚠️ Error: {e}")
    print("   Using fallback synthetic data...")

    # Fallback data
    dates = pd.date_range(start='2023-01-01', periods=300)
    prices = np.cumsum(np.random.randn(len(dates))) + 150
    volumes = np.random.randint(50_000_000, 100_000_000, len(dates))

    fallback_data = pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Volume': volumes
    })

    fallback_data['MA50'] = fallback_data['Close'].rolling(50).mean()
    fallback_data['MA100'] = fallback_data['Close'].rolling(100).mean()

    fig_financial = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('Synthetic Stock Price (Fallback)', 'Trading Volume'),
        vertical_spacing=0.08,
        row_heights=[0.75, 0.25]
    )

    fig_financial.add_trace(
        go.Scatter(x=fallback_data['Date'], y=fallback_data['Close'], name='Close Price', line=dict(color='#1f77b4', width=2.5)),
        row=1, col=1
    )

    fig_financial.add_trace(
        go.Scatter(x=fallback_data['Date'], y=fallback_data['MA50'], name='50-Day MA', line=dict(color='#ff7f0e', width=2, dash='dash')),
        row=1, col=1
    )

    fig_financial.add_trace(
        go.Scatter(x=fallback_data['Date'], y=fallback_data['MA100'], name='100-Day MA', line=dict(color='#2ca02c', width=2, dash='dot')),
        row=1, col=1
    )

    fig_financial.add_trace(
        go.Bar(x=fallback_data['Date'], y=fallback_data['Volume'], name='Volume', marker_color='#8c564b', opacity=0.8),
        row=2, col=1
    )

    fig_financial.update_layout(
        title="💹 Financial Dashboard (Fallback Data)",
        height=900,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_financial.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig_financial.update_yaxes(title_text="Volume", row=2, col=1)
    
    fig_financial.update_layout(
        xaxis2=dict(
            title_text="Date",
            rangeslider=dict(visible=True, thickness=0.08, bgcolor="#F3F4F6"),
            type="date"
        )
    )
    fig_financial.update_xaxes(rangeslider_visible=False, row=1, col=1)

    financial_html_path = 'dashboard/financial_dashboard.html'
    fig_financial.write_html(financial_html_path)

    print(f"✅ Fallback dashboard saved to: {financial_html_path}")

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
