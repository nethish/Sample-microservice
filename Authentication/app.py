from flask import Flask, request, g, jsonify
import os
import json
import sqlite3
import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

@app.route('/api/user', methods=['POST'])
def create_user():
  email = request.form['email']
  name = request.form['name']
  db.create_user(email, name)
  return jsonify({'success': True})

@app.route('/api/user/<email>', methods=["GET"])
def get_user(email):
  result = db.get_user(email)
  return jsonify({'email': result['email'], 'name': result['name']})

if __name__ == '__main__':
    app.run(port = 5001, debug=True)
