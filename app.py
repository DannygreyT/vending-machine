from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions

def get_products():
    conn = sqlite3.connect('vending.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return products

def get_product(product_id):
    conn = sqlite3.connect('vending.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    conn.close()
    return product

@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    cart_products = []
    total = 0

    for product_id in cart:
        product = get_product(product_id)
        if product:
            cart_products.append(product)
            total += product['price']

    return render_template('cart.html', cart_products=cart_products, total=total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/admin')
def admin():
    products = get_products()
    return render_template('admin.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)

