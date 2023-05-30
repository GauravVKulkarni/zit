# !C:\msys64\mingw64\bin\python.exe
import os
import sqlite3
import pathlib
# from yogesh import working_tree_insert, commitfolders_insert, folder_insert, files_insert


def init():
    #create .git folder
    os.mkdir('.zit')
    
    # check if the database already exists
    if os.path.exists('.zit/database.db'):
        print('error: zit already initialized')
        return
    
    # make database.db in that folder and create the tables
    # os.chdir('.zit')
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    
    # - working tree (commit_id unique primary  key, message, Branch_name, time TEXT)
    createtableCommand1 = '''CREATE TABLE working_tree(commit_id INTEGER PRIMARY KEY, message TEXT, branch_name TEXT DEFAULT 'master', time TEXT)'''
    # - commitfolders(commit_id, folder_id, file_id)
    createtableCommand2 = '''CREATE TABLE commitfolders(commit_id INTEGER, folder_file_id INTEGER)'''
    # - folder (folder_id, folder_name, folder_file_id, content)
    createtableCommand3 = '''CREATE TABLE folder(id INTEGER PRIMARY KEY, path TEXT, subfolder_file_id INTEGER, content TEXT)'''
    
    # excute the commands
    cursor.execute(createtableCommand1)
    cursor.execute(createtableCommand2)
    cursor.execute(createtableCommand3)
    
    # commiting changes
    db.commit()
    db.close()
    print('success: zit initialized')
    

def add(root):
    id_list = []
    if len(os.listdir(root)) == 0:
        #  add that folder to the database
        #  get the last row id
        #  append that id to the list
        return id_list
    for path in os.listdir(root):
        if os.path.isfile(os.path.join(root, path)):
            # add to file
            # get the last row id
            # append that id to the list
            ''''''
        else:
            ids = add(os.path.join(root, path))
            # add that id to with name of root, and subfolder as null and that id to file_id
            # get the last row id
            # append that id to the id_list
    return id_list
    


if __name__ == '__main__':
    # for path in add_helper(os.getcwdb(), []):
    #     print(path)
    add(os.getcwdb())