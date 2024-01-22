import sqlite3
conn=sqlite3.connect('billing.db')
#conn.execute('''CREATE TABLE items (id INTEGER PRIMARY KEY,item_code TEXT NOT NULL,item_name TEXT NOT NULL,item_barcode TEXT NOT NULL,item_gst REAL NOT NULL,item_price REAL NOT NULL,item_qty INTEGER NOT NULL);''')
"""conn.execute('''
    CREATE TABLE IF NOT EXISTS Company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        gst TEXT,
        mobile TEXT
    )
''')
def create_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            customer_name TEXT,
            customer_GST TEXT,
            customer_mobile TEXT,
            customer_address TEXT
        )
    ''')
    conn.commit()
    conn.close()
def create_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id TEXT,
            vendor_name TEXT,
            vendor_address TEXT,
            vendor_GST TEXT,
            vendor_mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()
def create_table():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            bill_date TEXT,
            customer_id TEXT,
            customer_name TEXT,
            customer_mobile TEXT,
            customer_address TEXT,
            customer_GST TEXT
        )
    ''')
    conn.commit()
    conn.close()
def create_table():
    conn =sqlite3.connect("billing.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            bill_date TEXT,
            vendor_id TEXT,
            vendor_name TEXT,
            vendor_mobile TEXT,
            vendor_address TEXT,
            vendor_GST TEXT
        )
    ''')
    conn.commit()
    conn.close()
def create_table():
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE  purchases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name VARCHAR(255),
        bill_date DATE,
        customer_name VARCHAR(255),
        customer_id INT,
        item_code VARCHAR(255),
        item_name VARCHAR(255),
        price DECIMAL(10, 2),
        gst DECIMAL(5, 2),
        qty INT,
        total DECIMAL(10, 2)
    )''')
    conn.commit()
    conn.close()"""


def create_table():
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE  users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        role TEXT
    )''')
    conn.commit()
    conn.close()

create_table()