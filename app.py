from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, flash
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
used_ids = set()

app = Flask(__name__, template_folder='HTML/templates')
app.secret_key = 'klinkekule'
app.config['DATABASE'] = 'Data/database.db'

# Database SELECT queries
database = "Data/database.db"
queryUsers = "SELECT * FROM users WHERE user_id = ?"
queryItems = "SELECT * FROM items WHERE item_id = ?"
queryOrders = "SELECT * FROM orders WHERE user_id = ?"
queryImages = "SELECT * FROM images WHERE product_id = ?"

# General functions
def get_conn():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(database)
    return conn

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
        cursor.execute(queryItems, (product_id,))
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
        cursor.execute(queryImages, (product_id,))
        images_raw = cursor.fetchall()
        images = []
        for path in images_raw:
            images.append(path[0])
        return images
    except:
        return None

def get_cart(user_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT cart.*, images.path
            FROM cart
            INNER JOIN images ON cart.item_id = images.product_id
            WHERE cart.user_id = ? AND images.displayOrder = 1
        """, (user_id,))
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        cart_items = []
        for row in rows:
            cart_item = dict(zip(columns, row))
            cart_items.append(cart_item)
        return cart_items
    except:
        return None

def clear_cart(user_id):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM cart
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()
    except:
        pass
 
def generate_userid():
        while True:
            user_id = random.randint(100000, 999999)
            if user_id not in used_ids:
                used_ids.add(user_id)
                return user_id


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

# General routes
@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT items.item_id, items.title, images.path FROM items JOIN images ON items.item_id = images.product_id WHERE images.displayOrder = 1')
    items = cursor.fetchall()

    return render_template('index.html', items=items)

@app.route('/sort/<sortBy>', methods=['GET'])
def sort(sortBy):
    user = get_user()
    if user:
        if request.method == 'GET':
            conn = get_conn()
            cursor = conn.cursor()

            if sortBy == 'default':
                cursor.execute('SELECT items.item_id, items.title, images.path FROM items JOIN images ON items.item_id = images.product_id WHERE images.displayOrder = 1')
            elif sortBy == 'owner':
                cursor.execute('SELECT items.item_id, items.title, images.path, items.owner_id FROM items JOIN images ON items.item_id = images.product_id WHERE images.displayOrder = 1 AND items.owner_id = ?', (user['user_id'],))
            
            items = cursor.fetchall()
            
            return jsonify({'items': items})
    return jsonify({'items': None})

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

# User routes
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()

        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password or username == "" or password == "":
            return render_template('registration.html')
        if len(username.strip()) < 4 or len(password.strip()) < 5:
            return render_template('registration.html')
        

        hash = generate_password_hash(password)

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        user_id = generate_userid()

        if user is None:
            created_at = datetime.now().date().strftime("%d %B %Y")
            cursor.execute('INSERT INTO users (user_id, username, password, created_at) VALUES (?, ?, ?, ?)', (user_id, username, hash, created_at))
            conn.commit()
            session['userid'] = user_id
            return redirect(url_for('index'))
                
    return render_template('registration.html')

@app.route('/username')
def username():
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

@app.route('/logout', methods=['GET', 'DELETE'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route('/profile/<username>', methods=['GET', 'PUT', 'DELETE'])
def profile(username):
    if request.method == 'GET':
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

        user_raw = cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        user = dict(zip(columns, user_raw))

        orders = get_orders(user['user_id'])
        if session.get('userid') == user['user_id']:
            user['user_id'] = ""
            user['password'] = ""
            return render_template('profile.html', user_page=user, orders=orders, logged_in=True)
        
        user['user_id'] = ""
        user['password'] = ""
        return render_template('profile.html', user_page=user, orders=orders, logged_in=False)

    user = get_user()
    if user:
        if request.method == 'PUT':
            if user['username'] != username:
                return redirect(url_for('index'))
            
            conn = get_conn()
            cursor = conn.cursor()

            data = request.json
            if data is not None:
                bio = data['bio']
                address = data['address']
                phone = data['phone']
                
                if bio == "None" or bio == "":
                    bio = None
                if address == "None" or address == "":
                    address = None
                if phone == "None" or phone == "":
                    phone = None
                # Update current logged in user's profile which in itself is a security measure
                cursor.execute('UPDATE users SET bio = ?, address = ?, phone = ? WHERE user_id = ?', (bio, address, phone, user['user_id']))
                conn.commit()

                return jsonify({'message': 'Profile content updated successfully'})
            
        elif request.method == 'DELETE':
            if user['username'] != username:
                return redirect(url_for('index'))
            conn = get_conn()
            cur = conn.cursor()

            # Delete current logged in user's profile and everything inbetween
            cur.execute('DELETE FROM users WHERE user_id = ?', (user['user_id'],))
            cur.execute('DELETE FROM orders WHERE user_id = ?', (user['user_id'],))
            cur.execute('DELETE FROM cart WHERE user_id = ?', (user['user_id'],))
            cur.execute('DELETE FROM items WHERE owner_id = ?', (user['user_id'],))

            conn.commit()
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

# User specific product routes
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    user = get_user()
    if request.method == 'POST':
        if user:
            product_id = request.form['product_id']
            quantity = int(request.form['quantity'])
            existing_items = get_cart(user['user_id'])
            conn = get_conn()
            cursor = conn.cursor()
            product = get_product(product_id)

            in_cart = False
            if existing_items:
                for existing_item in existing_items:
                    if int(existing_item['item_id']) == int(product_id):
                        new_quantity = int(existing_item['quantity']) + quantity
                        new_price = float(existing_item['price']) * new_quantity
                        cursor.execute('''
                            UPDATE cart
                            SET quantity = ?, price = ?
                            WHERE user_id = ? AND item_id = ?
                        ''', (new_quantity, new_price, user['user_id'], existing_item['item_id']))
                        in_cart = True
                        break

            if not in_cart:
                quantity_price = float(product['price']) * quantity
                cursor.execute('''
                    INSERT INTO cart (user_id, item_id, title, description, price, image_path, quantity)
                    SELECT ?, items.item_id, items.title, items.description, ?, images.path, ?
                    FROM items
                    JOIN images ON items.item_id = images.product_id
                    WHERE items.item_id = ? AND images.displayOrder = 1
                ''', (user['user_id'], quantity_price, quantity, product_id))

            conn.commit()
            return jsonify({'message': 'Item added to cart successfully.'})
        else:
            return redirect(url_for('login'))
        
    if request.method == 'GET':
        if user:
            cart_items = get_cart(user['user_id'])
            total_price = 0
            for item in cart_items:
                total_price += item['price']
            return render_template('cart.html', cart_items=cart_items, total_price=total_price)
        else:  
            return redirect(url_for('login'))
        
    return redirect(url_for('index'))

@app.route('/cart/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    user = get_user()
    if user:
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute('DELETE FROM cart WHERE user_id = ? AND item_id = ?', (user['user_id'], item_id))
            conn.commit()
            cart_items = get_cart(user['user_id'])
            if cart_items:
                total_price = 0
                for item in cart_items:
                    total_price += item['price']
                return jsonify({'total_price': total_price})
            else:
                return jsonify({'total_price': 0})
        except:
            pass
    return redirect(url_for('login'))

@app.route('/orders')
def orders():
    user = get_user()
    if user != None:
        orders = get_orders(user['user_id'])
        return render_template('order_history.html', username=user['username'], orders=orders)
    else:
        return redirect(url_for('login'))

@app.route('/search_orders')
def search_orders():
    user = get_user()
    if user:
        query = request.args.get('query')
        orders = get_orders(user['user_id'])
        filtered_orders = []
        if orders != None:
            if query:
                for order in orders:
                    if query.lower() in order['title'].lower():
                        filtered_orders.append(order)
            else:
                filtered_orders = orders
        return jsonify(filtered_orders)
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    user = get_user()
    if user: 
        cart_items = get_cart(user['user_id'])
        if request.method == 'GET':
            total_price = 0
            for item in cart_items:
                total_price += item['price']
            return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
        if request.method == 'POST':
            purchase_date = datetime.now().date().strftime("%Y-%m-%d")
            if cart_items != None:
                conn = get_conn()
                cur = conn.cursor()
                for cart_item in cart_items:
                    cur.execute("""
                        INSERT INTO orders (order_date, user_id, product_id, quantity, total_amount)
                        VALUES (?, ?, ?, ?, ?)
                    """, (purchase_date, user['user_id'], cart_item['item_id'], cart_item['quantity'], cart_item['price']))

                conn.commit()
                clear_cart(user['user_id'])
                return redirect(url_for('index')) 
    else:
        return redirect(url_for('login'))
    return redirect(url_for('index'))


# Product routes
@app.route('/product/<product_id>', methods=['GET', 'DELETE']) 
def product(product_id):
    if request.method == 'GET':
        conn = get_conn()
        cursor = conn.cursor()

        # Fetch product
        cursor.execute(queryItems, (product_id,))
        item_raw = cursor.fetchone()
        if item_raw == None:
            return redirect(url_for('index'))
        columns = [column[0] for column in cursor.description]
        item = dict(zip(columns, item_raw))

        user = get_user()
        user_is_owner = False
        if user != None:
            if int(item['owner_id']) == int(user['user_id']):
                user_is_owner = True

        cursor.execute(queryImages, (product_id,))
        images_raw = cursor.fetchall()
        images = []
        for path in images_raw:
            images.append(path[0])
        owner = cursor.execute('SELECT username FROM users WHERE user_id = ?', (item['owner_id'],)).fetchone()[0]

        return render_template('product.html', item=item, images=images, owner=owner, user_is_owner=user_is_owner)
    elif request.method == 'DELETE':
        user = get_user()
        if user:
            conn = get_conn()
            cursor = conn.cursor()
            owner_id = cursor.execute('SELECT owner_id FROM items WHERE item_id = ?', (product_id,)).fetchone()
            if int(owner_id[0]) == int(user['user_id']):
                cursor.execute('DELETE FROM items WHERE item_id = ?', (product_id,))
                images = cursor.execute('SELECT path FROM images WHERE product_id = ?', (product_id,)).fetchall()
                for image in images:
                    filename = str(image[0])
                    filename = filename.lstrip('/')
                    if filename != 'static/images/ProductImages/no_image.jpg':
                        try:
                            os.remove(filename)
                        except:
                            print(f'\033[91mfile not found: + {filename}\033[0m')
                cursor.execute('DELETE FROM images WHERE product_id = ?', (product_id,))
                conn.commit()
                return redirect(url_for('index'))
            else:
                # If user not the owner, send him home
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    user = get_user()
    if user:
        if request.method == 'GET':
            return render_template('new_product.html')
        elif request.method == 'POST':
            title = request.form['title']
            description = request.form['description']

            if len(title) > 22 or len(description) > 500:
                return render_template('new_product.html')

            price = request.form['price']
            images = request.files.getlist('imageValues[]')

            if len(title.strip()) == 0 or len(str(price)) == 0:
                return render_template('new_product.html')

            imagePaths = []
            
            if len(images) == 0:
                imagePaths.append('static/images/ProductImages/no_image.jpg')
            else:
                n = 0
                for image in images:
                    imagePaths.append('static/images/ProductImages/' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + str(n) + str(image.filename))
                    image.save(imagePaths[n])
                    n += 1
            conn = get_conn()
            cursor = conn.cursor()
        
            owner_id = user['user_id'] if user else None
            item_id = cursor.execute('SELECT MAX(item_id) FROM items').fetchone()[0] + 1
            cursor.execute('INSERT INTO items (item_id, owner_id, title, description, price) VALUES (?, ?, ?, ?, ?)', (item_id, owner_id, title, description, price))

            i = 1
            n = 0
            for image in imagePaths:
                print(i, "i:", image)
                cursor.execute('INSERT INTO images (product_id, path, displayOrder) VALUES (?, ?, ?)', (item_id, "/" + image, i))
                i += 1
                n += 1
            conn.commit()
        
            return redirect(url_for('index'))
          
        else: return redirect(url_for('index')) # Just in case :)   
    else:
        return redirect(url_for('login'))

if __name__ == '__main__': 
    app.run(debug=True)