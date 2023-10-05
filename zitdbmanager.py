import sqlite3
from datetime import datetime
import os


def insert_file_folder(name, content=None, isfile="NO", subfolder=None):
    print(f"Inserting {name} in the folder")
    name = str(name)
    db = sqlite3.connect(".zit/database.db")
    cursor = db.cursor()
    cursor.execute(
        "INSERT into folder (path,folder_file_id,content, isfile) VALUES (?,?,?,?)",
        (name, subfolder, content, isfile),
    )
    db.commit()
    db.close()


def insert_staging_area(subfolder):
    print(f"Inserting into staging area with subfolder {subfolder}")
    db = sqlite3.connect(".zit/database.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO staging_area (folder_file_id) VALUES (?)", (subfolder,))
    db.commit()
    db.close()


# createtableCommand1 = '''CREATE TABLE working_tree(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, branch_name TEXT DEFAULT 'master', time TEXT, folder_file_id TEXT)'''
def insert_working_tree(message, folders, branch_name="master"):
    db = sqlite3.connect(".zit/database.db")
    cursor = db.cursor()

    # get the current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # insert into the working tree
    cursor.execute(
        "INSERT INTO working_tree (message, branch_name, time, folder_file_id) VALUES (?, ?, ?, ?)",
        (message, branch_name, current_time, folders),
    )
    db.commit()
    db.close()

    print(f"[{branch_name} (root-commit) {get_last_id('working_tree')}] {message}")


def get_last_id(table="folder"):
    db = sqlite3.connect(".zit/database.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT id from {table} ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    db.commit()
    db.close()
    if result is None:
        return 0
    return result[0]


def delete_row_by_id(table_name, id):
    # Connect to the database
    print(f"Deleting {table_name} with id {id}")
    conn = sqlite3.connect(".zit/database.db")
    cursor = conn.cursor()

    # Execute the delete statement
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))

    # Commit the changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()


def get_subid_by_id(table_name, id):
    # Connect to the database
    conn = sqlite3.connect(".zit/database.db")
    cursor = conn.cursor()

    # Execute the select statement
    cursor.execute(f"SELECT folder_file_id FROM {table_name} WHERE id = ?", (id,))

    try:
        row = cursor.fetchone()[0]
    except TypeError:
        return None
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

    return row


# def delete_files_from_database():


if __name__ == "__main__":
    get_last_id()
