from flask import Flask, render_template, request, redirect, url_for, flash, session, g, abort, jsonify
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='HTML/templates')
app.secret_key = 'klinkekule'
app.config['DATABASE'] = 'Data/database.db'

# database stuff
database = "Data/database.db"
queryUsers = "SELECT * FROM users WHERE user_id = ?"
queryItems = "SELECT * FROM items WHERE item_id = ?"
queryOrders = "SELECT * FROM orders WHERE user_id = ?"
queryImages = "SELECT * FROM images WHERE product_id = ?"

# Functions
def valid_auth(username, password):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    user = cursor.fetchone()

    if user:
        hash = user[2]
        return check_password_hash(hash, password)

    return False

def get_user():
    try:
        conn = get_conn()
        cursor = conn.cursor()
        user_id = session['userid']
        cursor.execute(queryUsers, (user_id,))
        user_raw = cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        user = dict(zip(columns, user_raw))
        return user
    except:
        return None

def get_product(product_id):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(queryItems, product_id)
        product_raw = cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        product = dict(zip(columns, product_raw))
        return product
    except:
        return None
    
def get_orders(user_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT orders.*, items.title, items.description, images.path
            FROM orders
            INNER JOIN items ON orders.product_id = items.item_id
            INNER JOIN images ON items.item_id = images.product_id
            WHERE orders.user_id = ? AND images.displayOrder = 1
        """, (user_id,))
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        orders = []
        for row in rows:
            order = dict(zip(columns, row))
            orders.append(order)
        return orders
    except:
        return None

def get_images(product_id):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(queryImages, product_id)
        images_raw = cursor.fetchall()
        images = []
        for path in images_raw:
            images.append(path[0])
        return images
    except:
        return None

def generate_id():
    return random.randint(100000, 999999)

def get_conn():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(database)
    return conn



@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

@app.context_processor
def logged_in_user():
    user = get_user()
    if user:
        return dict(user=user)
    else:
        return dict(user=None)


# Routes

@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT items.item_id, items.title, images.path FROM items JOIN images ON items.item_id = images.product_id WHERE images.displayOrder = 1')
    items = cursor.fetchall()

    return render_template('index.html', items=items)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()

        username = request.form.get("username")
        password = request.form.get("password")
        
        hash = generate_password_hash(password)

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        id = generate_id()

        if user is None:
            cursor.execute('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)', (id, username, hash))
            conn.commit()
            session['userid'] = id
            return redirect(url_for('index'))
                
    return render_template('registration.html')

@app.route('/check_username')
def check_username():
    username = request.args.get("username")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if valid_auth(username, password): 
            conn = get_conn()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                session['userid'] = user[0]
                return jsonify({'success': True})
        else:
            return jsonify({'sucess': False})
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = get_user()
    if user != None:
        orders = get_orders(user_id)
        return render_template('profile.html', user=user, orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/transactions/<int:user_id>')
def transactions(user_id):
    user = get_user()
    if user != None:
        orders = get_orders(user_id)
        return render_template('transactions.html', user=user, orders=orders)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = get_user()
    if user:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        return redirect(url_for('logout'))
    else:
        return None

@app.route('/product/<product_id>') 
def product(product_id):
    conn = get_conn()
    cursor = conn.cursor()

    # Fetch product
    cursor.execute(queryItems, product_id)
    item_raw = cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    item = dict(zip(columns, item_raw))

    cursor.execute(queryImages, product_id)
    images_raw = cursor.fetchall()
    images = []
    for path in images_raw:
        images.append(path[0])

    return render_template('product.html', item=item, images=images)

@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()

        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']

        cursor.execute('INSERT INTO items (title, description, price, stock) VALUES (?, ?, ?, ?)', (title, description, price, stock))
        conn.commit()

        return redirect(url_for('index'))
    else:
        return render_template('new_product.html')

if __name__ == '__main__':
    app.run(debug=True)
