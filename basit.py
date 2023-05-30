import sqlite3

def insert_file_folder(name,content=None, subfolder=None):
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    cursor.execute("INSERT into folder (path,subfolder_file_id,content) VALUES (?,?,?)",(name,subfolder,content))
    db.commit()
    db.close()

def insert_commit():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()

def insert_add():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()

def get_last_id():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    cursor.execute("SELECT id from folder ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    db.commit()
    db.close()
    return result[0]

if __name__ == '__main__':
    get_last_id()
    