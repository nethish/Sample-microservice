from flask import Flask, request, g, jsonify
import os
import json
import sqlite3
import requests
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

@app.route('/api/payments/<email>', methods=['POST'])
def make_payment(email):
  products = request.form['products']
  print(request.form, products, "P")
  for product in products:
    db.log(email, product)
  return jsonify({'success': True})

@app.route('/api/payments/<email>', methods=["GET"])
def get(email):
  result = db.get(email)
  return jsonify(result)

if __name__ == '__main__':
    app.run(port=5003, debug=True)
