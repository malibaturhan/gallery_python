import sqlite3

def create_database():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()

    # İlişkili silme ve güvenlikler için foreign key açılır
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        original_filename TEXT,
        title TEXT,
        description TEXT,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        deleted_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_reactions (
        user_id INTEGER NOT NULL,
        image_id INTEGER NOT NULL,
        reaction INTEGER NOT NULL CHECK (reaction IN (1, -1)),
        reacted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, image_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER NOT NULL,
        user_id INTEGER,
        viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip_hash TEXT,
        FOREIGN KEY (image_id) REFERENCES images(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    conn.commit()
    conn.close()
    print("Veritabanı başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_database()
