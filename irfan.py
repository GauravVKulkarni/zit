import os
import sqlite3

def init():
    #create .git folder
    os.mkdir('.zit')
    
    # make database.db in that folder and create the tables
    # os.chdir('.zit')
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    
    # - working tree (commit_id unique primary  key, message, branch_id, Branch_name)
    createtableCommand1 = '''CREATE TABLE IF NOT EXISTS working_tree(commit_id INTEGER PRIMARY KEY, message TEXT, branch_id INTEGER, branch_name TEXT)'''
    # - commitfolders(commit_id, folder_id, file_id)
    createtableCommand2 = '''CREATE TABLE IF NOT EXISTS commitfolders(commit_id INTEGER, folder_id INTEGER, file_id INTEGER)'''
    # - folder (folder_id, folder_name, folder_id, file_id)
    createtableCommand3 = '''CREATE TABLE IF NOT EXISTS folder(id INTEGER PRIMARY KEY, folder_id INTEGER, folder_name TEXT,ssub_file INTEGER, file_id INTEGER)'''
    # - files (id, file_name, content)
    createtableCommand4 = '''CREATE TABLE IF NOT EXISTS files(file_id INTEGER PRIMARY KEY, file_name TEXT, content TEXT)'''
    
    # excute the commands
    cursor.execute(createtableCommand1)
    cursor.execute(createtableCommand2)
    cursor.execute(createtableCommand3)
    cursor.execute(createtableCommand4)
    
    # commiting changes
    db.commit()
    db.close()