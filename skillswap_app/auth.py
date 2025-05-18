# auth.py
import sqlite3
import bcrypt

def signup_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, hashed_password))
    conn.commit()
    conn.close()
    return True, "User registered successfully!"

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hashed_password = result[0]

        # Agar stored password string hai toh usay bytes mein convert karo
        if isinstance(stored_hashed_password, str):
            stored_hashed_password = stored_hashed_password.encode('utf-8')

        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)
    
    return False
