import os
import sqlite3
from basit import insert_file_folder, insert_commit, insert_add, get_last_id
from yogesh import get_file_content
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
    createtableCommand1 = '''CREATE TABLE working_tree(id INTEGER PRIMARY KEY, message TEXT, branch_name TEXT DEFAULT 'master', time TEXT, add_id INTEGER, folder_file_id)'''
    # - commitfolders(commit_id, folder_id, file_id)
    createtableCommand2 = '''CREATE TABLE add(id INTEGER PRIMARY KEY, folder_file_id INTEGER)'''
    # - folder (folder_id, folder_name, folder_file_id, content)
    createtableCommand3 = '''CREATE TABLE folder(id INTEGER PRIMARY KEY, add id path TEXT, subfolder_file_id TEXT, content TEXT)'''
    
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
        insert_file_folder()
        # #  get the last row id
        # id = get_last_id()
        # #  append that id to the list
        # id_list.append(id)

        return id_list
    for path in os.listdir(root):
        if os.path.isfile(os.path.join(root, path)):
            # add to file
            content = get_file_content(os.path.join(root, path))
            insert_file_folder(name=os.path.join(root, path),content=content)
            # get the last row id
            id = get_last_id()
            # append that id to the list
            id_list.append(id)
        else:
            ids = add(os.path.join(root, path))
            # add that id with name of root, and subfolder as null and that id to file_id
            insert_file_folder(name=os.path.join(root, path), subfolder_id=ids)
            # get the last row id
            id = get_last_id()
            # append that id to the id_list
            id_list.append(id)
    return id_list
    


if __name__ == '__main__':
    # for path in add_helper(os.getcwdb(), []):
    #     print(path)
    add(os.getcwdb())