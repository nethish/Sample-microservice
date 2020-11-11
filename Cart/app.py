from flask import Flask, request, g, jsonify
import os
import json
import sqlite3
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

@app.route('/api/cart', methods=['POST'])
def add_product():
  email = request.form['email']
  product = request.form['product']
  db.add_product(email, product)
  return jsonify({'success': True})

@app.route('/api/cart/<email>', methods=["GET"])
def get_products(email):
  result = db.get_products(email)
  return jsonify(result)

@app.route('/api/cart/<email>', methods=["DELETE"])
def delete_products(email):
  db.delete(email)
  return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(port=5002, debug=True)
