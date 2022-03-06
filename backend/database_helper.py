import sqlite3
from flask import g

DATABASE = 'database.db'

# Amizing resources can be found at https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv

def get_specific_user(email, password):
    """
    Return the user with the specified email and password
    """
    return query_db("select * from users WHERE email=? AND password=?", [email, password], one=True)

def add_user(token, email):
    """
    Inserts the user into the logged in users table.
    """
    query_db("INSERT INTO loggedinusers(token, email) VALUES(?, ?)", [token, email])

def select_user_by_email(email):
    """
    Return the user with the specified email.
    """
    return query_db("select * from users WHERE email=?", [email], one=True)

def create_user(email, city, country, familyName, firstName, gender, password):
    """
    Create a new user.
    """
    query_db("INSERT INTO users(email, city, country, familyname, firstname, gender, password) VALUES(?, ?, ?, ?, ?, ?, ?)", [email, city, country, familyName, firstName, gender, password])
    
def remove_user(token):
    """
    Removes the user from the logged logged in users table.
    """
    query_db("DELETE FROM loggedinusers WHERE token=?", [token])

def select_user_by_token(token):
    """
    Get user by token
    """
    return query_db("select * from loggedinusers WHERE token=?", [token], one=True)

def set_password(email, password):
    """
    Set user password
    """
    query_db("UPDATE users SET password=? WHERE email=?", [password, email])

def get_email_by_token(token):
    """
    Get user email by token
    """
    return query_db("SELECT email from loggedinusers WHERE token=?", [token], one=True)

def get_user_by_email(email):

    return query_db("SELECT email from users WHERE email=?", [email], one=True)


def create_message(email, message):
    query_db("INSERT INTO messages(writer, content) VALUES(?, ?)", [email, message])

def get_messages_by_email(email):
    return query_db("select * from messages WHERE writer=?", [email])