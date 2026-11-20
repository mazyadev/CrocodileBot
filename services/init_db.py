import sqlite3

def generate_categories():
    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255)
    );
    """)

    con.commit()
    con.close()

def generate_words():
    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS words
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word VARCHAR(255) NOT NULL,
        category_id INTEGER NOT NULL,
        difficulty VARCHAR(10) NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)

    con.commit()
    con.close()