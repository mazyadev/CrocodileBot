import sqlite3
from services.create_game import create_game
from services.categories import categories_id

def get_random_word(telegramchat_id, categories, difficult, fallback=True):

    if len(categories) == 0:
        categories = categories_id

    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    placeholders = ", ".join("?" for _ in categories) 
    word = cursor.execute(f""" 
        SELECT * FROM words
        WHERE (category_id in ({placeholders}) AND difficulty == ?)
        ORDER BY RANDOM() LIMIT 1
    """, categories+[difficult])

    need_word = word.fetchone()

    con.close()

    if need_word is not None:
        idtable = create_game(telegramchat_id,need_word[1])
        return [need_word[1], idtable]
    else:
        if fallback:
            return get_random_word(telegramchat_id,categories_id, difficult, fallback=False)
        else:
            return None