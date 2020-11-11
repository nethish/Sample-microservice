import sqlite3
from flask import g
import datetime
import os

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "/home/nethish/Desktop/Projects/SP/Microservices/Authentication/users" , detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = get_db()
    db = g.pop("db", None)
    if db is not None:
        db.close()

def get_user(email):
    db = get_db()
    result = db.execute('SELECT * FROM users WHERE email="{}";'.format(email)).fetchone()
    return result

def create_user(email, name):
    db = get_db()
    db.execute('INSERT INTO users VALUES ("{}", "{}");'.format(email, name))
    db.commit()
