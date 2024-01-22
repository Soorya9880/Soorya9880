from flask import *
import sqlite3

app = Flask(__name__)
conn=sqlite3.connect('billing.db')
cursor=conn.cursor()


# Database configuration
DATABASE = 'billing.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to get a database cursor
def get_cursor():
    return get_db().cursor()

# Teardown function to close the database connection at the end of the request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cursor = get_cursor()

        cursor.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)', (email, password, role))

        # Commit the changes to the database
        get_db().commit()

        # Close the cursor (optional, as the connection will be closed by the teardown function)
        cursor.close()

        return "User added successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users WHERE email=? and password=?",(email ,password))
    user_data=cursor.fetchone()
    if user_data:
        print(user_data)
        if user_data[3]=='admin':
            return render_template('dashboard.html')
        if user_data[3]=='user':
            return render_template('user_dashboard.html')

    return render_template('login.html')

@app.route('/Companyentry')
def Companyentry():
    return render_template('Companyentry.html')


@app.route('/submit_company', methods=['POST'])
def submit_company():
    if request.method == 'POST':
        name = request.form['companyName']
        address = request.form['companyAddress']
        gst = request.form['companyGST']
        mobile = request.form['companyMobile']

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        # Insert the form data into the Company table
        cursor.execute('''
            INSERT INTO Company (name, address, gst, mobile) VALUES (?, ?, ?, ?)
        ''', (name, address, gst, mobile))

        conn.commit()
        conn.close()

        return 'Data saved to the database successfully'
    else:
        return 'Invalid request'

@app.route('/addcustomer')
def addcustomer():
    return render_template('addcustomer.html')

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        customer_id = request.form['customerid']
        customer_name = request.form['customername']
        customer_GST = request.form['customerGST']
        customer_mobile = request.form['customerMobile']
        customer_address = request.form['customeraddress']

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        # Insert the form data into the database
        cursor.execute('''
            INSERT INTO customers (customer_id, customer_name, customer_GST, customer_mobile, customer_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, customer_name, customer_GST, customer_mobile, customer_address))

        conn.commit()
        conn.close()
        msg='Customer details added in the database'
        return render_template('addcustomer.html',msg=msg)

@app.route('/Vendorentry')
def Vendorentry():
    return render_template('Vendorentry.html')


@app.route('/submit_vendor', methods=['POST'])
def submit_vendor():
    if request.method == 'POST':
        vendor_id = request.form['vendorID']
        vendor_name = request.form['vendorName']
        vendor_address = request.form['vendorAddress']
        vendor_GST=request.form['vendorGST']
        vendor_mobile=request.form['vendorMobile']
        # Retrieve other form data similarly

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        # Insert the form data into the database
        cursor.execute('''
            INSERT INTO vendors (vendor_id, vendor_name, vendor_address, vendor_GST, vendor_mobile)
            VALUES (?, ?, ?, ?, ?)
        ''', (vendor_id, vendor_name, vendor_address, vendor_GST, vendor_mobile))

        conn.commit()
        conn.close()
        msg='vendor details added successfully'

        return render_template('Vendorentry.html', msg=msg)

@app.route('/additem')
def additem():
    return render_template('additem.html')



@app.route('/additom1', methods=['GET', 'POST'])
def add_itom():
    if request.method == 'POST':
        item_code = request.form['itemCode']
        item_name = request.form['itemName']
        item_barcode = request.form['itemBarcode']
        item_gst = request.form['itemGST']
        item_price = request.form['itemPrice']
        item_qty = request.form['itemQty']

        # Save the data to a SQLite database
        conn = sqlite3.connect('billing.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO items (item_code, item_name, item_barcode, item_gst, item_price, item_qty) VALUES (?, ?, ?, ?, ?, ?)',
            (item_code, item_name, item_barcode, item_gst, item_price, item_qty))
        conn.commit()
        conn.close()
        msg="Data saved successfully"

        return render_template('additem.html', msg=msg)

    return render_template('dashboard.html')


@app.route('/submit_sale', methods=['POST'])
def submit_sale():
    if request.method == 'POST':
        company_name = request.form['companyName']
        bill_date = request.form['billDate']
        customer_id = request.form['customerID']
        customer_name = request.form['customerName']
        customer_mobile = request.form['customerMobile']
        customer_address = request.form['customerAddress']
        customer_gst = request.form['customerGST']

        # Initialize items_data list
        items_data = []

        # Establish a connection to the database
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        item_codes = request.form.getlist('item_code')
        item_names = request.form.getlist('item_name')
        qtys = request.form.getlist('qty')
        prices = request.form.getlist('price')
        gsts = request.form.getlist('gst')
        totals = request.form.getlist('total')

        # Iterate through the lists and insert each set of values
        for i in range(len(item_codes)):
            if item_codes[i]:
                conn = sqlite3.connect('billing.db')
                cursor = conn.cursor()
                item_data = {
                    'item_code': item_codes[i],
                    'item_name': item_names[i],
                    'qty': qtys[i],
                    'price': prices[i],
                    'gst': gsts[i],
                    'total': totals[i],
                }
                items_data.append(item_data)

                # SQL INSERT statement
                sql_insert = """
                INSERT INTO purchases (company_name, bill_date, customer_id, customer_name, item_code, item_name, qty, price, gst, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                # Execute the SQL statement with the provided values
                cursor.execute(sql_insert, (
                    company_name, bill_date, customer_id, customer_name,
                    item_codes[i], item_names[i], qtys[i], prices[i], gsts[i], totals[i]
                ))

                # Commit the changes to the database
                conn.commit()

                # Close the database connection
                conn.close()

        # Calculate subtotal, totalgst, grandTotal (you may already have this logic)
        subtotal = request.form['subtotal']
        totalgst = request.form['totalgst']
        grandTotal = request.form['grandTotal']

        # Render the invoice template with the form data
        return render_template('sale_invoice.html',
                               company_name=company_name,
                               bill_date=bill_date,
                               customer_id=customer_id,
                               customer_name=customer_name,
                               customer_mobile=customer_mobile,
                               customer_address=customer_address,
                               customer_gst=customer_gst,
                               items_data=items_data,
                               subtotal=subtotal,
                               totalgst=totalgst,
                               grandTotal=grandTotal)


@app.route('/Purchaseentry')
def Purchaseentry():
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT vendor_id FROM vendors')
    vendor_ids = [row[0] for row in cursor.fetchall()]
    print(vendor_ids)
    cursor.execute('SELECT item_code FROM items')
    item_codes = [row[0] for row in cursor.fetchall()]
    print(item_codes)
    return render_template('Purchaseentry.html', vendor_ids=vendor_ids, item_codes=item_codes)

@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    if request.method == 'POST':
        company_name = request.form['companyName']
        bill_date = request.form['billDate']
        vendor_id = request.form['vendorID']
        vendor_name = request.form['vendorName']
        vendor_mobile = request.form['vendorMobile']
        vendor_address = request.form['vendorAddress']
        vendor_GST = request.form['vendorGST']
        # Initialize items_data list
        items_data = []

        # Establish a connection to the database
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        item_codes = request.form.getlist('item_code')
        item_names = request.form.getlist('item_name')
        qtys = request.form.getlist('qty')
        prices = request.form.getlist('price')
        gsts = request.form.getlist('gst')
        totals = request.form.getlist('total')

        # Iterate through the lists and insert each set of values
        for i in range(len(item_codes)):
            if item_codes[i]:
                conn = sqlite3.connect('billing.db')
                cursor = conn.cursor()
                item_data = {
                    'item_code': item_codes[i],
                    'item_name': item_names[i],
                    'qty': qtys[i],
                    'price': prices[i],
                    'gst': gsts[i],
                    'total': totals[i],
                }
                items_data.append(item_data)

                # SQL INSERT statement
                sql_insert = """
                       INSERT INTO sales (company_name, bill_date, vendor_id, vendor_name, item_code, item_name, qty, price, gst, total)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """

                # Execute the SQL statement with the provided values
                cursor.execute(sql_insert, (
                    company_name, bill_date, vendor_id, vendor_name,
                    item_codes[i], item_names[i], qtys[i], prices[i], gsts[i], totals[i]
                ))

                # Commit the changes to the database
                conn.commit()

                # Close the database connection
                conn.close()

        # Calculate subtotal, totalgst, grandTotal (you may already have this logic)
        subtotal = request.form['subtotal']
        totalgst = request.form['totalgst']
        grandTotal = request.form['grandTotal']

        # Render the invoice template with the form data
        return render_template('sale_invoice.html',
                               company_name=company_name,
                               bill_date=bill_date,
                               vendor_id=vendor_id,
                               vendor_name=vendor_name,
                               vendor_mobile=vendor_mobile,
                               vendor_address=vendor_address,
                               vendor_GST=vendor_GST,
                               items_data=items_data,
                               subtotal=subtotal,
                               totalgst=totalgst,
                               grandTotal=grandTotal)


# Route to display company data
@app.route('/company_data')
def company_data():
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM Company")
    data = cursor.fetchall()

    conn.close()

    # Pass the data to the HTML template for rendering
    return render_template('companydetails.html', data=data)

# Route for editing a specific company record
@app.route('/edit_company/<int:id>')
def edit_data(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Fetch the specific record based on the ID
    cursor.execute("SELECT * FROM Company WHERE id=?", (id,))
    data = cursor.fetchone()

    conn.close()

    # Pass the data to the HTML template for editing
    return render_template('edit_company.html', data=data)


@app.route('/update_company/<int:id>', methods=['POST'])
def update_data(id):
    if request.method == 'POST':
        conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
        cursor = conn.cursor()

        # Get form data from the POST request
        company_name = request.form['companyName']
        company_address = request.form['companyAddress']
        company_gst = request.form['companyGST']
        company_mobile = request.form['companyMobile']

        # Update the specific record based on the ID
        cursor.execute("UPDATE Company SET Name=?, Address=?, GST=?, Mobile=? WHERE id=?",
                       (company_name, company_address, company_gst, company_mobile, id))
        conn.commit()

        conn.close()

        # Redirect to a page after updating (You can redirect to the company display page)
        return redirect(url_for('company_data'))


# Route for deleting a specific company record
@app.route('/delete/<int:id>')
def delete_data(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Delete the specific record based on the ID
    cursor.execute("DELETE FROM Company WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return "Record deleted successfully"


@app.route('/display_customers')
def display_customers():
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()

    conn.close()

    # Pass the data to the HTML template for rendering
    return render_template('customer_details.html', data=data)

@app.route('/edit_customer/<int:id>')
def edit_customer(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Fetch the specific record based on the ID
    cursor.execute("SELECT * FROM customers WHERE id=?", (id,))
    data = cursor.fetchone()

    conn.close()

    # Pass the data to the HTML template for editing
    return render_template('edit_customer.html', data=data)

@app.route('/delete_customer/<int:id>')
def delete_customer(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Delete the specific record based on the ID
    cursor.execute("DELETE FROM customers WHERE id=?", (id,))
    conn.commit()

    conn.close()

    # Redirect to the display customers page after deletion
    return redirect(url_for('display_customers'))

@app.route('/update_customer/<int:id>', methods=['POST'])
def update_customer(id):
    if request.method == 'POST':
        conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
        cursor = conn.cursor()

        # Get form data from the POST request
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        customer_GST = request.form['customer_GST']
        customer_mobile = request.form['customer_mobile']
        customer_address = request.form['customer_address']

        # Update the specific record based on the ID
        cursor.execute("UPDATE customers SET customer_id=?, customer_name=?, customer_GST=?, customer_mobile=?, customer_address=? WHERE id=?",
                       (customer_id, customer_name, customer_GST, customer_mobile, customer_address, id))
        conn.commit()

        conn.close()

        # Redirect to the display customers page after updating
        return redirect(url_for('display_customers'))


@app.route('/display_vendors')
def display_vendors():
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your database name
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM vendors")
    data = cursor.fetchall()

    conn.close()

    return render_template('display_vendors.html', data=data)


@app.route('/edit_vendor/<int:id>', methods=['GET', 'POST'])
def edit_vendor(id):
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        vendor_address = request.form['vendor_address']
        vendor_GST = request.form['vendor_GST']
        vendor_mobile = request.form['vendor_mobile']

        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE vendors SET vendor_id=?, vendor_name=?, vendor_address=?, vendor_GST=?, vendor_mobile=? WHERE id=?", (vendor_id, vendor_name, vendor_address, vendor_GST, vendor_mobile, id))
        conn.commit()

        conn.close()

        return redirect(url_for('display_vendors') )

    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vendors WHERE id=?", (id,))
    vendor = cursor.fetchone()

    conn.close()

    return render_template('edit_vendor.html', vendor=vendor)

@app.route('/delete_vendor/<int:id>', methods=['POST','GET'])
def delete_vendor(id):
    try:
        conn = sqlite3.connect('billing.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM vendors WHERE id=?", (id,))
        conn.commit()

        flash('Vendor deleted successfully', 'success')
    except sqlite3.Error as e:
        conn.rollback()
        flash(f'Error deleting vendor: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('display_vendors'))
@app.route('/display_items')
def display_items():
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    # Fetch all items from the database
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    conn.close()

    return render_template('display_items.html', items=items)

@app.route('/edit_item/<int:id>')
def edit_item(id):
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    # Fetch the item from the database by ID
    cursor.execute('SELECT * FROM items WHERE id=?', (id,))
    item = cursor.fetchone()

    conn.close()

    return render_template('edit_item.html', item=item)

# Update item route
@app.route('/update_item/<int:id>', methods=['POST'])
def update_item(id):
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    # Update the item in the database based on the form data
    cursor.execute('''
        UPDATE items
        SET item_code=?, item_name=?, item_barcode=?, item_gst=?, item_price=?, item_qty=?
        WHERE id=?
    ''', (
        request.form['item_code'],
        request.form['item_name'],
        request.form['item_barcode'],
        request.form['item_gst'],
        request.form['item_price'],
        request.form['item_qty'],
        id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for('display_items'))

# Delete item route
@app.route('/delete_item/<int:id>')
def delete_item(id):
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    # Delete the item from the database by ID
    cursor.execute('DELETE FROM items WHERE id=?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('display_items'))

# Route to display sales details
@app.route('/display_sales')
def display_sales():
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sale_details")
    sales = cursor.fetchall()
    conn.close()
    return render_template('display_sales.html', sales=sales)


# Route to edit a sale
@app.route('/edit_sale/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    if request.method == 'POST':
        company_name = request.form['company_name']
        bill_date = request.form['bill_date']
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        customer_mobile = request.form['customer_mobile']
        customer_address = request.form['customer_address']
        customer_GST = request.form['customer_GST']

        conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
        cursor = conn.cursor()

        cursor.execute("UPDATE sale_details SET company_name=?, bill_date=?, customer_id=?, "
                       "customer_name=?, customer_mobile=?, customer_address=?, customer_GST=? WHERE id=?",
                       (company_name, bill_date, customer_id, customer_name, customer_mobile, customer_address,
                        customer_GST, id))
        conn.commit()

        conn.close()

        return redirect(url_for('display_sales'))

    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sale_details WHERE id=?", (id,))
    sale = cursor.fetchone()
    conn.close()
    return render_template('edit_sale.html', sale=sale)

# Route to delete a sale
@app.route('/delete_sale/<int:id>')
def delete_sale(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sale_details WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect(url_for('display_sales'))

@app.route('/display_purchases')
def display_purchases():
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM purchase")
    purchases = cursor.fetchall()
    conn.close()
    return render_template('display_purchases.html', purchases=purchases)

# Route to edit a purchase
@app.route('/edit_purchase/<int:id>', methods=['GET', 'POST'])
def edit_purchase(id):
    if request.method == 'POST':
        company_name = request.form['company_name']
        bill_date = request.form['bill_date']
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        vendor_mobile = request.form['vendor_mobile']
        vendor_address = request.form['vendor_address']
        vendor_GST = request.form['vendor_GST']

        conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
        cursor = conn.cursor()

        cursor.execute("UPDATE purchase SET company_name=?, bill_date=?, vendor_id=?, "
                       "vendor_name=?, vendor_mobile=?, vendor_address=?, vendor_GST=? WHERE id=?",
                       (company_name, bill_date, vendor_id, vendor_name, vendor_mobile, vendor_address,
                        vendor_GST, id))
        conn.commit()

        conn.close()

        return redirect(url_for('display_purchases'))
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM purchase WHERE id=?", (id,))
    purchase = cursor.fetchone()
    conn.close()
    return render_template('edit_purchase.html', purchase=purchase)

# Route to delete a purchase
@app.route('/delete_purchase/<int:id>')
def delete_purchase(id):
    conn = sqlite3.connect('billing.db')  # Replace 'your_database.db' with your actual database name
    cursor = conn.cursor()

    cursor.execute("DELETE FROM purchase WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect(url_for('display_purchases'))


@app.route('/Salesentry')
def Salesentry():
    conn=sqlite3.connect('billing.db')
    cursor=conn.cursor()
    cursor.execute('SELECT customer_id FROM customers')
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT item_code FROM items')
    item_codes = [row[0] for row in cursor.fetchall()]
    print(item_codes)
    return render_template('Salesentry.html', customer_ids=customer_ids,item_codes=item_codes)


@app.route('/get_customer_details', methods=['POST'])
def get_customer_details():
    customer_id = request.form['customer_id']
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
    customer = cursor.fetchone()

    if customer:
        customer_details = {
            'name': customer[2],
            'mobile': customer[3],
            'address': customer[4],
            'gst': customer[5]
        }
    else:
        customer_details = {}

    return jsonify(customer_details)

@app.route('/get_vendor_details', methods=['POST'])
def get_vendor_details():
    vendor_id = request.form['vendor_id']
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendors WHERE vendor_id = ?', (vendor_id,))
    vendor = cursor.fetchone()
    print(vendor)

    if vendor:
        vendor_details = {
            'name': vendor[2],
            'mobile': vendor[5],
            'address': vendor[3],
            'gst': vendor[4]
        }
    else:
        vendor_details = {}

    return jsonify(vendor_details)



@app.route('/get_item_details', methods=['POST'])
def get_item_details():
    item_code = request.form['item_code']
    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM items WHERE item_code = ?', (item_code,))
    item = cursor.fetchone()

    if item:
        item_details = {
            'item_name': item[2],
            'price': item[5],
            'gst': item[4]
        }
    else:
        item_details = {}
    print(item_details)

    return jsonify(item_details)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
