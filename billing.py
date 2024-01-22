import sqlite3

def create_database():
    # Connect to or create the SQLite database
    conn = sqlite3.connect('my_store_database.db')
    cursor = conn.cursor()

    # Create table for Customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY,
            CustomerName TEXT,
            CustomerMobileNumber TEXT,
            CustomerAddress TEXT,
            CustomerGST TEXT
        )
    ''')

    # Create table for Items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            ItemCode INTEGER PRIMARY KEY,
            ItemName TEXT,
            ItemBarcodeNumber TEXT,
            ItemGSTNo TEXT,
            ItemPrice REAL,
            ItemQty INTEGER
        )
    ''')

    # Create table for Company Entry
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            CompanyID INTEGER PRIMARY KEY,
            CompanyName TEXT,
            CompanyAddress TEXT,
            CompanyGST TEXT,
            CompanyMobileNumber TEXT
        )
    ''')

    # Create table for Vendor Entry
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vendors (
            VendorID INTEGER PRIMARY KEY,
            VendorName TEXT,
            VendorAddress TEXT,
            VendorGST TEXT,
            VendorMobileNumber TEXT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def insert_data(table_name,data):
    conn = sqlite3.connect('my_store_database.db')
    cursor = conn.cursor()

    # Insert data into the specified table
    placeholders = ', '.join(['?'] * len(data))
    cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', data)

    conn.commit()
    conn.close()
create_database()
# Example data insertion for Customers
customer_data = (1, 'John Doe', '1234567890', '123 Main St, City, Country', 'GSTIN12345678')
insert_data('Customers', customer_data)
