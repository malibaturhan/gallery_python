import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               email TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL
               )
""")
cursor.execute("""
    INSERT OR IGNORE INTO users(username, email, password) 
               VALUES  (?,?,?)""", ("admin,aa@bb,123"))

conn.commit()
conn.close()