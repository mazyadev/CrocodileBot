import sqlite3

categories_id = []
categories_dict = {}

def get_categories() -> list:
    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    categories = cursor.execute(""" 
        SELECT id, name FROM categories
        """).fetchall()

    
    con.close()

    for i in categories:
        categories_dict[int(i[0])] = i[1]
        categories_id.append(i[0])

    return categories
