import flask
from flask import url_for
import sqlite3
import random

app = flask.Flask(__name__, template_folder='HTML/templates')
app.secret_key = 'klinkekule'
app.config['DATABASE'] = 'Data/database.db'

# database stuff
database = "Data/database.db"
queryUsers = "SELECT * FROM users WHERE id = ?"
queryItems = "SELECT * FROM items WHERE id = ?"
queryImages = "SELECT * FROM images WHERE product_id = ?"

def generate_id():
    return random.randint(100000, 999999)

def get_conn():
    conn = getattr(flask.g, '_database', None)
    if conn is None:
        conn = flask.g._database = sqlite3.connect(database)
    return conn

@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(flask.g, '_database', None)
    if conn is not None:
        conn.close()

@app.context_processor 
def logged_in_user():
    user = flask.session.get('username')
    return dict(user=user)

# Routes

@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT items.id, items.title, images.path FROM items JOIN images ON items.id = images.product_id WHERE images.displayOrder = 1')
    items = cursor.fetchall()

    return flask.render_template('index.html', items=items)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if flask.request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()

        username = flask.request.form['username']
        password = flask.request.form['password']
        confirm_password = flask.request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match'
            return flask.render_template('registration.html', error=error)
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user:
            error = 'Username already exists.'
            return flask.render_template('registration.html', error=error)
        
        id = generate_id()
        cursor.execute('INSERT INTO users (id, username, password) VALUES (?, ?, ?)', (id, username, password))
        conn.commit()
        flask.session['username'] = username
        return flask.redirect(flask.url_for('index'))
    
    return flask.render_template('registration.html')

@app.route('/login', methods=["GET", 'POST'])
def login():
    if flask.request.method == 'POST':
        conn = get_conn()
        cursor = conn.cursor()
        
        username = flask.request.form['username']
        password = flask.request.form['password']

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            flask.session['username'] = user[1]
            return flask.redirect(flask.url_for('index'))
        else:
            error = 'Invalid login credentials.'
            return flask.render_template('login.html', error=error)
        
    return flask.render_template('login.html')

@app.route('/logout')
def logout():
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('index'))

@app.route('/cart')
def cart():
    return flask.render_template('cart.html')

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

    return flask.render_template('product.html', item=item, images=images)


if __name__ == '__main__':
    app.run(debug=True)
