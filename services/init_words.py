import json
import sqlite3


def init_words():
    with open('words.json' , 'r', encoding='utf-8') as file:
        data_dict = json.load(file)

    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()


    for data in data_dict:
        cursor.execute("""
        INSERT INTO words (word, category_id, difficulty)
        VALUES (?, ?, ?)
        """, (data["word"], data["category_id"], data["difficulty"]))

    duplicates = cursor.execute(""" 
        SELECT word, category_id, difficulty, COUNT(*)
        FROM words
        GROUP BY word, category_id, difficulty
        HAVING COUNT(*) > 1;
        """)

    print(f"DELETED {len(duplicates.fetchall())}")

    cursor.execute(""" 
        DELETE FROM words
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM words
            GROUP BY word, category_id, difficulty
        );
    """)


    con.commit()
    con.close()