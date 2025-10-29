import pandas as pd
from faker import Faker
import sqlite3
import numpy as np
import os

# Initialize Faker for synthesizing data
fake = Faker()

# Load the data from CSV (assumed in root; download from Kaggle)
df = pd.read_csv('data.csv', encoding='ISO-8859-1')

# Data Cleaning
df = df.dropna(subset=['CustomerID'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# Customers Table
unique_customers = df['CustomerID'].unique().astype(int)
signup_dates = df.groupby('CustomerID')['InvoiceDate'].min().reset_index()['InvoiceDate']
customers_df = pd.DataFrame({
    'id': unique_customers,
    'name': [fake.name() for _ in unique_customers],
    'email': [fake.email() for _ in unique_customers],
    'city': [fake.city() for _ in unique_customers],
    'signup_date': signup_dates
})

# Products Table
unique_products = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates('StockCode')
product_prices = df.groupby('StockCode')['UnitPrice'].max().reset_index()['UnitPrice']
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Toys', 'Books', 'Beauty', 'Sports']
unique_products['category'] = np.random.choice(categories, size=len(unique_products))
unique_products['price'] = product_prices
unique_products['stock'] = np.random.randint(50, 500, size=len(unique_products))
products_df = unique_products.rename(columns={'StockCode': 'id', 'Description': 'name'})[['id', 'name', 'category', 'price', 'stock']]

# Orders Table (header)
unique_orders = df['InvoiceNo'].unique()
order_customers = df.groupby('InvoiceNo')['CustomerID'].first().reset_index()['CustomerID'].astype(int)
order_dates = df.groupby('InvoiceNo')['InvoiceDate'].first().reset_index()['InvoiceDate']
order_totals = df.groupby('InvoiceNo')['Revenue'].sum().reset_index()['Revenue']
orders_df = pd.DataFrame({
    'id': unique_orders,
    'customer_id': order_customers,
    'order_date': order_dates,
    'total': order_totals
})

# Order Items Table (bridge for line items)
# Map InvoiceNo to order id (use string id for orders)
df['order_id'] = df['InvoiceNo']
order_items_df = pd.DataFrame({
    'id': range(1, len(df) + 1),
    'order_id': df['order_id'],
    'product_id': df['StockCode'],
    'quantity': df['Quantity'],
    'price_at_purchase': df['UnitPrice'],
    'line_total': df['Revenue']
})

# Sales Table (per order)
sales_df = pd.DataFrame({
    'id': range(1, len(orders_df) + 1),
    'order_id': orders_df['id'],
    'revenue': orders_df['total'],
    'profit_margin': np.random.uniform(0.1, 0.4, len(orders_df)),
    'sales_date': orders_df['order_date']
})

# Database Creation
db_path = 'business_data.sqlite'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables with keys
cursor.execute('''
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    signup_date DATETIME
)
''')

cursor.execute('''
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
''')

cursor.execute('''
CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    customer_id INTEGER,
    order_date DATETIME,
    total REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')

cursor.execute('''
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    price_at_purchase REAL,
    line_total REAL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
''')

cursor.execute('''
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    order_id TEXT,
    revenue REAL,
    profit_margin REAL,
    sales_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(id)
)
''')

# Insert data
customers_df.to_sql('customers', conn, if_exists='append', index=False)
products_df.to_sql('products', conn, if_exists='append', index=False)
orders_df.to_sql('orders', conn, if_exists='append', index=False)
order_items_df.to_sql('order_items', conn, if_exists='append', index=False)
sales_df.to_sql('sales', conn, if_exists='append', index=False)

# Add indexes
cursor.execute("CREATE INDEX idx_orders_customer_id ON orders(customer_id)")
cursor.execute("CREATE INDEX idx_order_items_order_id ON order_items(order_id)")
cursor.execute("CREATE INDEX idx_order_items_product_id ON order_items(product_id)")
cursor.execute("CREATE INDEX idx_sales_order_id ON sales(order_id)")

conn.commit()
conn.close()

print("Database setup complete: business_data.sqlite created with tables, keys, and indexes.")