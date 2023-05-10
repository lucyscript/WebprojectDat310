import flask
from flask import url_for
import sqlite3

app = flask.Flask(__name__, template_folder='HTML/templates')

# database stuff
database = "Data/database.db"
queryUsers = "SELECT * FROM users WHERE id = ?"
queryItems = "SELECT * FROM items WHERE id = ?"
queryImages = "SELECT * FROM images WHERE product_id = ?"

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



# Routes

@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT items.id, items.title, images.path FROM items JOIN images ON items.id = images.product_id WHERE images.displayOrder = 1')
    items = cursor.fetchall()

    return flask.render_template('index.html', items=items)

@app.route('/cart')
def cart():
    return flask.render_template('cart.html')

@app.route('/product/<product_id>') 
def product(product_id):
    conn = get_conn()
    cursor = conn.cursor()

    # Fetch product
    cursor.execute(queryItems, product_id)
    item = cursor.fetchone()

    cursor.execute(queryImages, product_id)
    images_raw = cursor.fetchall()
    images = []
    for path in images_raw:
        images.append(path[0])

    return flask.render_template('product.html', item=item, images=images)


if __name__ == '__main__':
    app.run(debug=True)
