import sqlite3
import bcrypt

# ======== USERS DATABASE (users.db) ========

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class Database:
    def __init__(self):
        create_user_table()

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

# ======== SKILLS DATABASE (skills.db) ========

def create_skill_table():
    conn = sqlite3.connect('skills.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL,
            provider_username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_skill_to_db(title, description, price, provider_username):
    conn = sqlite3.connect('skills.db')
    c = conn.cursor()
    c.execute('INSERT INTO skills (title, description, price, provider_username) VALUES (?, ?, ?, ?)',
              (title, description, price, provider_username))
    conn.commit()
    conn.close()

def get_all_skills():
    conn = sqlite3.connect('skills.db')
    c = conn.cursor()
    c.execute('SELECT title, description, price, provider_username FROM skills')
    skills = c.fetchall()
    conn.close()
    return skills
