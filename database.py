import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("users.db")

def init_db():
    conn = connect()
    sql = conn.cursor()
    sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,name TEXT,phone_number TEXT,lang TEXT,reg_date DATETIME);")
    conn.commit()
    conn.close()

init_db()

def add_user(user_id, name, phone_number, lang='ru'):
    conn = connect()
    sql = conn.cursor()
    sql.execute("INSERT OR REPLACE INTO users (user_id, name, phone_number, lang, reg_date) VALUES (?, ?, ?, ?, ?);",
                (user_id, name, phone_number, lang, datetime.now()))
    conn.commit()
    conn.close()

def check_user(user_id):
    conn = connect()
    sql = conn.cursor()
    check = sql.execute("SELECT 1 FROM users WHERE user_id=?;", (user_id,)).fetchone()
    conn.close()
    return bool(check)

def get_all_users():
    conn = connect()
    sql = conn.cursor()
    result = sql.execute("SELECT * FROM users;").fetchall()
    conn.close()
    return result

def get_user_info(user_id):
    conn = connect()
    sql = conn.cursor()
    result = sql.execute("SELECT name, phone_number FROM users WHERE user_id=?;", (user_id,)).fetchone()
    conn.close()
    return result

def get_user_lang(user_id):
    conn = connect()
    sql = conn.cursor()
    result = sql.execute("SELECT lang FROM users WHERE user_id=?;", (user_id,)).fetchone()
    conn.close()
    return result[0] if result else 'ru'

def set_user_lang(user_id, lang):
    conn = connect()
    sql = conn.cursor()
    if check_user(user_id):
        sql.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
    else:
        sql.execute("INSERT INTO users (user_id, lang) VALUES (?, ?, ?);", (user_id, lang))
    conn.commit()
    conn.close()

def get_all_id():
    conn = connect()
    sql = conn.cursor()
    result = sql.execute("SELECT user_id FROM users;").fetchall()
    conn.close()
    return result
