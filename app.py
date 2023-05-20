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

@app.context_processor
def init_bio_processor():
    def get_init_bio(user_created_at):
        init_bio = [
            f"Trading addict since {user_created_at}.",
            f"From {user_created_at}, I've been on a quest to outsmart the market.",
            f"Since {user_created_at}, I've been the self-proclaimed captain of the trading ship.",
            f"Warning! I've been trading since {user_created_at}.",
            f"Attention, world! Trading extraordinaire since {user_created_at} reporting for duty.",
            f"Trading aficionado since {user_created_at}.",
            f"From {user_created_at}, I've been on a quest to find the holy grail of trading strategies.",
            f"Trading magician in training since {user_created_at}.",
            f"Buckle up, trading novices! Since {user_created_at}, I've been honing my skills to perfection.",
            f"Calling myself a trader since {user_created_at}."
        ]
        return random.choice(init_bio)

    return {'get_init_bio': get_init_bio}


# Routes

@app.route('/', methods=['GET', 'POST', 'DELETE'])
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
            created_at = datetime.now().date().strftime("%d %B %Y")
            cursor.execute('INSERT INTO users (user_id, username, password, created_at) VALUES (?, ?, ?, ?)', (id, username, hash, created_at))
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

@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    user = get_user()
    if user:
        if request.method == 'PUT':
            conn = get_conn()
            cursor = conn.cursor()

            data = request.json
            bio = data['bio']
            address = data['address']
            phone = data['phone']

            cursor.execute('UPDATE users SET bio = ?, address = ?, phone = ? WHERE user_id = ?', (bio, address, phone, user['user_id']))
            conn.commit()

            return jsonify({'message': 'Profile content updated successfully'})

        else:
            orders = get_orders(user['user_id'])
            return render_template('profile.html', user=user, orders=orders)

    return redirect(url_for('login'))

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/order_history')
def order_history():
    user = get_user()
    if user != None:
        orders = get_orders(user['user_id'])
        return render_template('order_history.html', user=user, orders=orders)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    if request.method == 'DELETE':
        user = get_user()
        if user:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('DELETE FROM users WHERE user_id = ?', (user['user_id'],))
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

@app.route('/search_orders', methods=['GET'])
def search_orders():
    user = get_user()
    if user:
        if request.method == 'GET':
            query = request.args.get('query')

            orders = get_orders(user['user_id'])
            filtered_orders = []

            if query:
                for order in orders:
                    if query.lower() in order['title'].lower():
                        filtered_orders.append(order)
            else:
                filtered_orders = orders

            return jsonify(filtered_orders)
    

@app.route('/search/<search_query>', methods=['GET'])
def search(search_query):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
                SELECT items.item_id, items.title, items.price, images.path
                FROM items
                JOIN images ON items.item_id = images.product_id
                WHERE items.title LIKE ? AND images.displayOrder = 1
                ''', ('%' + search_query + '%',))
    items = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    items = [dict(zip(columns, item)) for item in items]
    return jsonify(items)

@app.route('/checkout')
def checkout():
    user = get_user()
    if user: 
        orders = get_orders(user['user_id'])
        return render_template('checkout.html', orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/settings')
def settings():
    user = get_user()
    if user:
        return render_template('settings.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__': 
    app.run(debug=True)
