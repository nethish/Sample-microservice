from flask import Flask, request, g, jsonify
import os
import json
import sqlite3
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

@app.route('/api/products', methods=['GET'])
def get_products():
  result = db.get();
  return jsonify(result)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
