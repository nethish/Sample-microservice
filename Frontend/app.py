from flask import Flask, redirect, request, url_for, session, render_template
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import requests
import os
import json
from user import User

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

AUTH_URL = 'http://localhost:5001/api/user'
PRODUCT_URL = 'http://localhost:5004/api/products'
CART_URL = 'http://localhost:5002/api/cart'
PAYMENT_URL = 'http://localhost:5003/api/payments/'

@login_manager.user_loader
def load_user(email):
    u = requests.get(AUTH_URL + '/' + email).json()
    if 'email' not in u:
        return None
    user = User(u['email'], u['name'])
    return user

@app.route('/', methods=["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('shop'))
    else:
        return render_template('index.htm')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    user = requests.get(AUTH_URL + '/' + email).json()
    if not user:
        return redirect(url_for('index'))
    user = User(user['email'], user['name'])
    login_user(user)
    return redirect(url_for('shop'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    name = request.form['name']
    requests.post(AUTH_URL, data = {'email': email, 'name': name})
    return redirect(url_for('index'))

@app.route('/shop')
@login_required
def shop():
    products = requests.get(PRODUCT_URL).json()
    cart = requests.get(CART_URL + '/' + current_user.email).json()
    payments = []
    payments = requests.get(PAYMENT_URL + current_user.email).json()
    # print(payments, "PAY")
    return render_template('shop.htm', products=products, cart=cart, payments=payments)

@app.route('/add', methods=["POST"])
@login_required
def add():
    email = current_user.email
    for i in request.form.keys():
        product = i
    requests.post(CART_URL, {'email': email, 'product': product})
    return redirect(url_for('shop'))

@app.route('/placeorder', methods=["POST"])
@login_required
def placeorder():
    email = current_user.email
    products = requests.get(CART_URL + '/' + email).json()
    # print(products, "PP")
    prods = []
    for i in products:
        prods.append(i['product'])
    requests.post(PAYMENT_URL + email, {'email': email, 'products': prods})
    requests.delete(CART_URL + '/' + email)
    return redirect(url_for('shop'))


if __name__ == '__main__':
    app.run(port = 5000, debug=True)
