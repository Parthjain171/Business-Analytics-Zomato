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
# HTML TEMPLATE ENGINE
# ============================================================================
def generate_html_page(title, active_page, kpis_html, chart_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #2563EB;
            --bg: #F3F4F6;
            --card-bg: #FFFFFF;
            --text-main: #1F2937;
            --text-muted: #6B7280;
            --sidebar-bg: #111827;
            --sidebar-hover: #1F2937;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text-main); display: flex; min-height: 100vh; }}
        
        /* Sidebar */
        .sidebar {{
            width: 260px;
            background-color: var(--sidebar-bg);
            color: white;
            padding: 2rem 1.5rem;
            position: fixed;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .sidebar h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 2rem; color: white; display: flex; align-items: center; gap: 10px; }}
        .sidebar a {{
            display: flex;
            align-items: center;
            gap: 10px;
            color: #9CA3AF;
            text-decoration: none;
            padding: 0.875rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            font-weight: 500;
            transition: 0.2s;
        }}
        .sidebar a:hover {{ background-color: var(--sidebar-hover); color: white; }}
        .sidebar a.active {{ background-color: var(--primary); color: white; }}
        
        /* Main Content */
        .main-content {{
            margin-left: 260px;
            padding: 2.5rem 3rem;
            width: calc(100% - 260px);
        }}
        .header {{ margin-bottom: 2rem; }}
        .header h1 {{ font-size: 2rem; font-weight: 700; color: var(--text-main); letter-spacing: -0.025em; }}
        
        /* KPIs */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        .kpi-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border-left: 4px solid var(--primary);
            transition: transform 0.2s;
        }}
        .kpi-card:hover {{ transform: translateY(-3px); }}
        .kpi-title {{ font-size: 0.875rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; font-weight: 600; }}
        .kpi-value {{ font-size: 2rem; font-weight: 700; color: var(--text-main); }}
        
        /* Chart Container */
        .chart-container {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>📊 Analytics Pro</h2>
        <a href="../index.html">🏠 Home</a>
        <a href="customer_dashboard.html" class="{'active' if active_page == 'customer' else ''}">🛍️ Customer Analytics</a>
        <a href="financial_dashboard.html" class="{'active' if active_page == 'financial' else ''}">📈 Financial Analytics</a>
    </div>
    
    <div class="main-content">
        <div class="header">
            <h1>{title}</h1>
        </div>
        
        <div class="kpi-grid">
            {kpis_html}
        </div>
        
        <div class="chart-container">
            {chart_html}
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# 1. CUSTOMER ANALYTICS DASHBOARD
# ============================================================================
print("\n📊 Generating Customer Analytics Dashboard...")

# Generate synthetic retail dataset with more realistic data
np.random.seed(42)
num_records = 1000

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

# Build KPIs
total_sales_kpi = f"${df['Sales'].sum():,.0f}"
total_orders_kpi = f"{len(df):,}"
top_category_kpi = sales_by_category.index[0]

customer_kpis = f"""
<div class="kpi-card"><div class="kpi-title">Total Revenue</div><div class="kpi-value" style="color: #10B981;">{total_sales_kpi}</div></div>
<div class="kpi-card"><div class="kpi-title">Total Orders</div><div class="kpi-value">{total_orders_kpi}</div></div>
<div class="kpi-card"><div class="kpi-title">Top Category</div><div class="kpi-value">{top_category_kpi}</div></div>
"""

# Create Plotly Dashboard
fig_customer = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales by Category', 'Sales Distribution by Region',
                    'Monthly Sales Trend', 'Quantity by Category'),
    specs=[[{'type': 'bar'}, {'type': 'pie'}],
           [{'type': 'scatter'}, {'type': 'bar'}]],
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

fig_customer.add_trace(go.Bar(x=sales_by_category.index, y=sales_by_category.values, marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'], name='Sales', showlegend=False), row=1, col=1)
fig_customer.add_trace(go.Pie(labels=sales_by_region.index, values=sales_by_region.values, marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']), name='Region', showlegend=False), row=1, col=2)
fig_customer.add_trace(go.Scatter(x=sales_trend['Date'], y=sales_trend['Sales'], mode='lines+markers', line=dict(color='#00CC96', width=3), marker=dict(size=6), fill='tozeroy', name='Sales', showlegend=False), row=2, col=1)
fig_customer.add_trace(go.Bar(x=quantity_by_category.index, y=quantity_by_category.values, marker_color='#EF553B', name='Quantity', showlegend=False), row=2, col=2)

fig_customer.update_xaxes(title_text="Category", row=1, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=1, col=1)
fig_customer.update_xaxes(title_text="Month", row=2, col=1)
fig_customer.update_yaxes(title_text="Sales ($)", row=2, col=1)
fig_customer.update_xaxes(title_text="Category", row=2, col=2)
fig_customer.update_yaxes(title_text="Quantity", row=2, col=2)

fig_customer.update_layout(
    height=800,
    showlegend=False,
    template='plotly_white',
    font=dict(size=12, family="Inter, Arial, sans-serif"),
    margin=dict(l=40, r=40, t=60, b=40)
)

# Render HTML
customer_chart_html = fig_customer.to_html(full_html=False, include_plotlyjs='cdn')
customer_full_html = generate_html_page("Customer Analytics", "customer", customer_kpis, customer_chart_html)

customer_html_path = 'dashboard/customer_dashboard.html'
with open(customer_html_path, "w", encoding="utf-8") as f:
    f.write(customer_full_html)
print(f"✅ Customer Analytics Dashboard saved to: {customer_html_path}")

# ============================================================================
# 2. FINANCIAL ANALYTICS DASHBOARD
# ============================================================================
print("\n📊 Generating Financial Analytics Dashboard...")

try:
    print("   Fetching AAPL stock data from Yahoo Finance...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    try:
        aapl_data = yf.download('AAPL', start=start_date, end=end_date, multi_level_index=False, progress=False)
    except TypeError:
        aapl_data = yf.download('AAPL', start=start_date, end=end_date, progress=False)

    if aapl_data is None or aapl_data.empty:
        raise ValueError("No data received from Yahoo Finance")

    if isinstance(aapl_data.columns, pd.MultiIndex):
        levels = aapl_data.columns.levels
        if 'Close' in levels[0]:
            aapl_data.columns = aapl_data.columns.get_level_values(0)
        elif len(levels) > 1 and 'Close' in levels[1]:
            aapl_data.columns = aapl_data.columns.get_level_values(1)
        else:
            aapl_data.columns = [col[0] if isinstance(col, tuple) else col for col in aapl_data.columns]

    aapl_data = aapl_data.reset_index()
    
    if 'Date' not in aapl_data.columns and 'Datetime' in aapl_data.columns:
        aapl_data = aapl_data.rename(columns={'Datetime': 'Date'})
    elif 'Date' not in aapl_data.columns and 'index' in aapl_data.columns:
        aapl_data = aapl_data.rename(columns={'index': 'Date'})

    required_cols = ['Date', 'Close', 'Volume']
    for col in required_cols:
        if col not in aapl_data.columns:
            raise ValueError(f"Missing column: {col}")

    aapl_data = aapl_data[['Date', 'Close', 'Volume']].copy()
    aapl_data['Date'] = pd.to_datetime(aapl_data['Date'])
    aapl_data['Close'] = pd.to_numeric(aapl_data['Close'], errors='coerce')
    aapl_data['Volume'] = pd.to_numeric(aapl_data['Volume'], errors='coerce')
    aapl_data = aapl_data.dropna()

    if len(aapl_data) < 100:
        raise ValueError(f"Too few data points: {len(aapl_data)}")

    print(f"   Downloaded {len(aapl_data)} trading days")

    aapl_data['MA50'] = aapl_data['Close'].rolling(window=50).mean()
    aapl_data['MA100'] = aapl_data['Close'].rolling(window=100).mean()

    # Build Financial KPIs
    current_price = aapl_data['Close'].iloc[-1]
    prev_price = aapl_data['Close'].iloc[-2]
    price_change = current_price - prev_price
    change_color = "#10B981" if price_change >= 0 else "#EF4444"
    price_display = f"${current_price:.2f} <span style='font-size:1.1rem;color:{change_color}'>({'%+.2f' % price_change})</span>"
    avg_vol = f"{aapl_data['Volume'].mean():,.0f}"
    
    financial_kpis = f"""
    <div class="kpi-card" style="border-left-color: {change_color};"><div class="kpi-title">AAPL Current Price</div><div class="kpi-value">{price_display}</div></div>
    <div class="kpi-card"><div class="kpi-title">Avg Daily Volume</div><div class="kpi-value">{avg_vol}</div></div>
    <div class="kpi-card"><div class="kpi-title">Trading Days Tracked</div><div class="kpi-value">{len(aapl_data)}</div></div>
    """

    fig_financial = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=('AAPL Stock Price with Moving Averages', 'Trading Volume'),
        vertical_spacing=0.08, row_heights=[0.75, 0.25]
    )

    fig_financial.add_trace(go.Scatter(x=aapl_data['Date'], y=aapl_data['Close'], mode='lines', name='Close Price', line=dict(color='#1f77b4', width=2.5)), row=1, col=1)
    fig_financial.add_trace(go.Scatter(x=aapl_data['Date'], y=aapl_data['MA50'], mode='lines', name='50-Day MA', line=dict(color='#ff7f0e', width=2, dash='dash')), row=1, col=1)
    fig_financial.add_trace(go.Scatter(x=aapl_data['Date'], y=aapl_data['MA100'], mode='lines', name='100-Day MA', line=dict(color='#2ca02c', width=2, dash='dot')), row=1, col=1)

    colors = ['#EF4444' if aapl_data.iloc[i]['Close'] < aapl_data.iloc[i-1]['Close'] else '#10B981' for i in range(len(aapl_data))]
    colors[0] = '#10B981'
    fig_financial.add_trace(go.Bar(x=aapl_data['Date'], y=aapl_data['Volume'], name='Volume', marker_color=colors, opacity=0.8), row=2, col=1)

    fig_financial.update_layout(
        height=750,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(size=12, family="Inter, Arial, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig_financial.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig_financial.update_yaxes(title_text="Volume", row=2, col=1)
    fig_financial.update_layout(xaxis2=dict(title_text="Date", rangeslider=dict(visible=True, thickness=0.08, bgcolor="#F3F4F6"), type="date"))
    fig_financial.update_xaxes(rangeslider_visible=False, row=1, col=1)

    fin_chart_html = fig_financial.to_html(full_html=False, include_plotlyjs='cdn')
    fin_full_html = generate_html_page("Financial Analytics", "financial", financial_kpis, fin_chart_html)

    financial_html_path = 'dashboard/financial_dashboard.html'
    with open(financial_html_path, "w", encoding="utf-8") as f:
        f.write(fin_full_html)
    print(f"✅ Financial Dashboard saved to: {financial_html_path}")

except Exception as e:
    print(f"⚠️ Error: {e}")
    print("   Using fallback synthetic data...")
    # Minimal fallback just to keep it running
    financial_html_path = 'dashboard/financial_dashboard.html'
    with open(financial_html_path, "w", encoding="utf-8") as f:
        f.write("<h1>Error loading financial data</h1>")
    print(f"✅ Fallback dashboard saved to: {financial_html_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("🎉 DASHBOARD GENERATION COMPLETE!")
print("="*70)
print(f"\n🌐 To view dashboards:")
print(f"   - Open the HTML files directly in your browser")
print("="*70)
