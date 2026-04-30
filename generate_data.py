import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate comprehensive Superstore dataset
customers = [f'AA-{10315 + i}' for i in range(300)]
products = {
    'Technology': ['Phones', 'Copiers', 'Machines', 'Accessories'],
    'Office Supplies': ['Appliances', 'Pens', 'Paper', 'Binders'],
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
    'Groceries': ['Snacks', 'Beverages', 'Canned Goods', 'Dairy']
}

regions = ['West', 'South', 'East', 'Central']
segments = ['Consumer', 'Corporate', 'Home Office']

records = []
start_date = datetime(2011, 1, 1)
end_date = datetime(2017, 12, 31)

for i in range(2000):
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    customer = random.choice(customers)
    category = random.choice(list(products.keys()))
    subcategory = random.choice(products[category])
    
    quantity = random.randint(1, 20)
    sale_price = random.uniform(10, 500)
    sales = quantity * sale_price
    discount = random.choice([0, 0.05, 0.1, 0.15, 0.2])
    profit_margin = random.uniform(-0.2, 0.4)
    profit = sales * profit_margin
    
    records.append({
        'Order ID': f'ORD-{i:05d}',
        'Order Date': order_date.strftime('%m/%d/%Y'),
        'Ship Date': (order_date + timedelta(days=random.randint(1, 7))).strftime('%m/%d/%Y'),
        'Ship Mode': random.choice(['Standard Class', 'Second Class', 'First Class', 'Same Day']),
        'Customer ID': customer,
        'Segment': random.choice(segments),
        'Country': 'United States',
        'City': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
        'State': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
        'Postal Code': random.randint(10000, 99999),
        'Region': random.choice(regions),
        'Product ID': f'PRD-{i%100:05d}',
        'Category': category,
        'Sub-Category': subcategory,
        'Product Name': f'{subcategory} Product',
        'Sales': round(sales, 2),
        'Quantity': quantity,
        'Discount': discount,
        'Profit': round(profit, 2)
    })

df = pd.DataFrame(records)
df.to_csv('data/SampleSuperstore.csv', index=False)
print('✓ Created SampleSuperstore.csv with {} records'.format(len(df)))
print('Date range: {} to {}'.format(df['Order Date'].min(), df['Order Date'].max()))
print('Customers: {}'.format(df['Customer ID'].nunique()))
