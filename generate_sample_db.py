import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        country TEXT,
        signup_date DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date DATE,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    # Sample Data
    customers = [
        ('Alice Smith', 'alice@example.com', 'USA'),
        ('Bob Johnson', 'bob@example.com', 'UK'),
        ('Charlie Brown', 'charlie@example.com', 'Canada'),
        ('Diana Prince', 'diana@example.com', 'USA'),
        ('Evan Wright', 'evan@example.com', 'Australia')
    ]

    products = [
        ('Laptop', 'Electronics', 1200.00),
        ('Smartphone', 'Electronics', 800.00),
        ('Headphones', 'Electronics', 150.00),
        ('Desk Chair', 'Furniture', 200.00),
        ('Coffee Maker', 'Appliances', 100.00),
        ('Notebook', 'Stationery', 5.00),
        ('Backpack', 'Accessories', 50.00)
    ]

    # Insert Customers
    for name, email, country in customers:
        signup_date = (datetime.now() - timedelta(days=random.randint(10, 365))).date()
        cursor.execute('INSERT OR IGNORE INTO customers (name, email, country, signup_date) VALUES (?, ?, ?, ?)', 
                       (name, email, country, signup_date))

    # Insert Products
    for name, category, price in products:
        cursor.execute('INSERT OR IGNORE INTO products (name, category, price) VALUES (?, ?, ?)', 
                       (name, category, price))
        
    conn.commit()

    # Generate random orders
    cursor.execute('SELECT id FROM customers')
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT id, price FROM products')
    product_data = cursor.fetchall()
    
    statuses = ['Completed', 'Pending', 'Shipped', 'Cancelled']

    # Insert 50 random orders
    for _ in range(50):
        c_id = random.choice(customer_ids)
        o_date = (datetime.now() - timedelta(days=random.randint(1, 180))).date()
        status = random.choice(statuses)
        
        cursor.execute('INSERT INTO orders (customer_id, order_date, status) VALUES (?, ?, ?)',
                       (c_id, o_date, status))
        order_id = cursor.lastrowid
        
        # Add 1 to 4 items per order
        for _ in range(random.randint(1, 4)):
            p_id, price = random.choice(product_data)
            quantity = random.randint(1, 3)
            cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                           (order_id, p_id, quantity, price))

    conn.commit()
    conn.close()
    print("Database 'sample.db' generated successfully with sample data.")

if __name__ == '__main__':
    create_database()
