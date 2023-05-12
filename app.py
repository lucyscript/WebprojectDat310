from flask import Flask, render_template, request, redirect, url_for, flash, session, g, abort
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='HTML/templates')
app.secret_key = 'klinkekule'
app.config['DATABASE'] = 'Data/database.db'

# database stuff
database = "Data/database.db"
queryUsers = "SELECT * FROM users WHERE id = ?"
queryItems = "SELECT * FROM items WHERE id = ?"
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
    return dict(user=user)



# Routes

@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT items.id, items.title, images.path FROM items JOIN images ON items.id = images.product_id WHERE images.displayOrder = 1')
    items = cursor.fetchall()

    return render_template('index.html', items=items)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()

        username = request.form.get("username").strip()
        if len(username) < 4:
            error = 'Username must be more than 3 characters!'
            return render_template("registration.html", error=error)

        password = request.form.get("password")
        if len(password) < 5:
            error = 'Password must be more than 4 characters!'
            return render_template('registration.html', error=error) 
        
        hash = generate_password_hash(password)

        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('registration.html', error=error)
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user:
            error = 'Username already exists.'
            return render_template('registration.html', error=error)
        
        id = generate_id()
        cursor.execute('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', (id, username, hash))
        conn.commit()
        session['userid'] = id
        return redirect(url_for('index'))
    
    return render_template('registration.html')

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
                return redirect(url_for('index'))
        else:
            error = 'Invalid login credentials.'
            return render_template('login.html', error=error)
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    user = get_user()
    if user != None:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/cart')
def cart():
    return render_template('cart.html')

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


if __name__ == '__main__':
    app.run(debug=True)
