import json
import sqlite3

with open('words.json' , 'r', encoding='utf-8') as file:
    data_dict = json.load(file)

con = sqlite3.connect('database/crocodile.db')
con.execute("PRAGMA foreign_keys = ON")
cursor = con.cursor()

print(len(data_dict))
print(len(set(item["word"] for item in data_dict)))

# for data in data_dict:
#     cursor.execute("""
#     INSERT INTO words (word, category_id, difficulty)
#     VALUES (?, ?, ?)
#     """, (data["word"], data["category_id"], data["difficulty"]))



# con.commit()
# con.close()