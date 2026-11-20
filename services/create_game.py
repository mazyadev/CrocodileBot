import sqlite3

def create_game(telegram_chat_id, word):
    con = sqlite3.connect('database/crocodile.db')
    con.execute("PRAGMA foreign_keys = ON")
    cursor = con.cursor()

    placeholders = [telegram_chat_id, word]
    cursor.execute(f""" 
        INSERT INTO games (chat_id, word) VALUES (?,?)

    """, placeholders)

    lastrowid = cursor.lastrowid

    con.commit()
    con.close()

    return lastrowid


def get_word_gameid(id):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [id]
    cursor.execute(""" 
        SELECT word FROM games WHERE id = ?

    """, placeholders)
    
    word = cursor.fetchone()

    
    con.close()

    if word != None:
        return word[0]
    else:
        return None

def get_telegram_id(userid,idgame):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [idgame]

    id = cursor.execute(""" 
    SELECT telegram_id FROM games WHERE id=?
    
    """, placeholders).fetchone()

    s = -1

    if id is None:
        s = None
    elif id[0] is None:
        s = userid
        set_telegram_id(userid, idgame)
        
    else:
        s = id[0]


    con.close()

    return s

# waiting — бот создал игру и ждёт, пока кто-нибудь нажмёт «Получить слово».
# playing — показывающий назначен, остальные угадывают.
# ended — кто-то угадал слово.
# cancelled — игру остановили командой или другим действием.

def change_status_gameid(game_id, status):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [status, game_id]

    cursor.execute(""" 
    UPDATE games
    SET status = ?
    where id = ?
    """, placeholders)

    result = cursor.rowcount

    con.commit()
    con.close()

    return result>0

def get_status_gameid(game_id):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [game_id]

    status = cursor.execute(""" 
    SELECT status
    FROM games
    where id = ?
    """, placeholders).fetchone()

    con.close()

    result = None

    if status is not None:
        result = status[0]
    
    return result

def get_game_id(chat_id):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [chat_id]

    id = cursor.execute(""" 
    SELECT id FROM games WHERE chat_id=?
    ORDER BY id DESC
    LIMIT 1
    """, placeholders).fetchone()

    con.close()

    result = None
    
    if id is not None:
        result = id[0] 

    return result

def set_telegram_id(telegramid, idgame):
    con = sqlite3.connect('database/crocodile.db')
    cursor = con.cursor()

    placeholders = [telegramid, idgame]
    cursor.execute(""" 
    UPDATE games
    SET telegram_id = ?
    where id = ?
    """, placeholders)

    con.commit()

    con.close()