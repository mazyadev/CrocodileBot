import sqlite3

categories = [
    {"id": 1, "name": "Животные"},
    {"id": 2, "name": "Профессии"},
    {"id": 3, "name": "Еда"},
    {"id": 4, "name": "Предметы"},
    {"id": 5, "name": "Явления и понятия"},
    {"id": 6, "name": "Действия и занятия"},
    {"id": 7, "name": "Места и сооружения"},
    {"id": 8, "name": "Техника и транспорт"},
    {"id": 9, "name": "Искусство и культура"},
    {"id": 10, "name": "Разное"}
]

def generate_categories():
    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) UNIQUE
    );
    """)


    for i in range(len(categories)):
        placeholders = [categories[i]["id"],categories[i]["name"]]

        cursor.execute("""
            INSERT OR IGNORE  INTO categories (id, name) VALUES (?, ?)
        """, placeholders)
    
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