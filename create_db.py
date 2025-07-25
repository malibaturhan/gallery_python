import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               email TEXT NOT NULL UNIQUE,
               password_hash TEXT NOT NULL,
               created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
               is_active INTEGER NOT NULL DEFAULT = 1
               );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS images(
        id INTEGER PRIMARY KEY NOT NULL,
        filename TEXT NOT NULL,
        original_filename TEXT,
        title TEXT,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        deleted_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_reactions(
        user_id INTEGER NOT NULL,
        image_id INTEGER NOT NULL,
        reaction INTEGER NOT NULL CHECK (reaction IN (-1, 1)),
        reacted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, image_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
    );
""")