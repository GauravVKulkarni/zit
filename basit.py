import sqlite3

def insert_file_folder(path,subfolder,content):
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    cursor.execute("INSERT into folder values(path=?,subfolder_file_id=?,content=?)",(path,subfolder,content))
    cursor.commit()
    cursor.close()

def insert_commit():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()

def insert_add():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()

def get_last_id():
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    return cursor.execute("SELECT id from folder where path=?",(path))
    