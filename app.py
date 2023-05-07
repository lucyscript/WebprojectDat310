from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__, template_folder='HTML/templates')
# conn = sqlite3.connect("/Data/database.db")
# cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/product/<product_id>')
def product(product_id):
    return render_template('product')


if __name__ == '__main__':
    app.run(debug=True)
