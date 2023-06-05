import os
import sqlite3
from basit import insert_file_folder, insert_staging_area, insert_working_tree, get_last_id, get_subid_by_id, delete_row_by_id
from yogesh import get_file_content, delete_files_from_database
# from yogesh import working_tree_insert, commitfolders_insert, folder_insert, files_insert


def init():
    
    # check if the database already exists
    print(os.path.exists('.zit//database.db'))
    if os.path.exists('.zit//database.db'):
        print('error: zit already initialized')
        return
    
    #create .git folder
    os.mkdir('.zit')
    # make database.db in that folder and create the tables
    # os.chdir('.zit')
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    
    # - working tree (commit_id unique primary  key, message, Branch_name, time TEXT)
    createtableCommand1 = '''CREATE TABLE working_tree(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, branch_name TEXT DEFAULT 'master', time TEXT, folder_file_id TEXT)'''
    # - commitfolders(commit_id, folder_id, file_id)
    createtableCommand2 = '''CREATE TABLE staging_area(id INTEGER PRIMARY KEY AUTOINCREMENT, folder_file_id Text)'''
    # - folder (folder_id, folder_name, folder_file_id, content)
    createtableCommand3 = '''CREATE TABLE folder(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, folder_file_id TEXT, content TEXT, isfile TEXT DEFAULT 'NO')'''
    
    # excute the commands
    cursor.execute(createtableCommand1)
    cursor.execute(createtableCommand2)
    cursor.execute(createtableCommand3)
    
    # commiting changes
    db.commit()
    db.close()
    print('zit initialized successfully')
    

def add(root):

    def add_files(root, zitignore):
        id_list = []
        if len(os.listdir(root)) == 0:
            # #  add that folder to the database
            # insert_file_folder(name=root)
            # #  get the last row id
            # id = get_last_id()
            # #  append that id to the list
            # id_list.append(id)
            return id_list
        
        for name in os.listdir(root):
            fullPath = os.path.join(root, name)
            if fullPath in zitignore or name == b'.zit' or name == b'.git':
                print("ignoring", name)
                continue
            
            if os.path.isfile(fullPath):
                # add to file
                content = get_file_content(fullPath)
                # to identify the the row in folder is 
                insert_file_folder(name=name,isfile='YES',content=content)
                # get the last row id
                id = get_last_id()
                # append that id to the list
                id_list.append(id)
            else:
                ids = add_files(fullPath, zitignore)
                # add this ids to subfolder and the name with the fullpath
                subfolderid = ','.join(map(str, ids))
                insert_file_folder(name=name, subfolder=subfolderid)
                # get the last row id
                id = get_last_id()
                # append that id to the id_list
                id_list.append(id)
        return id_list
    

    # checking the commit is done or not
    last_id_of_working_tree = get_last_id('working_tree')
    last_id_of_staging_area = get_last_id('staging_area')
    #if the commmit is not done yet delete the files from the database
    if last_id_of_working_tree < last_id_of_staging_area:
        #delete the files from the database
        print("Replacing files")
        subfolders = list(map(int, get_subid_by_id('staging_area', last_id_of_staging_area).split(',')))
        for id in subfolders:
            delete_files_from_database("folder", id)
        delete_row_by_id('staging_area', last_id_of_staging_area)

     
    # add the files to the database
    zitignore = []
    if os.path.exists('.zitignore'):
        try:
            pathofzitignore = os.path.join(root, b'.zitignore')
            with open(pathofzitignore) as f:
                zitignore = list(map(lambda x: os.path.join(root, x.strip().encode('utf-8')), f.readlines()))
        except TypeError:
            print("error: can not read .zitignore file")
    else:
        print("no .zitignore file found")
    ids = add_files(root, zitignore)
    subfolders = ','.join(map(str, ids))
    # insert in the folder table with the name of the root folder
    insert_file_folder(name=os.path.basename(root), subfolder=subfolders)
    # get the last row id   
    id = get_last_id()
    # insert in the staging_area table with the id of the folder table
    insert_staging_area(subfolder=id)



def commit(message):
    last_id_of_working_tree = get_last_id('working_tree')
    last_id_of_staging_area = get_last_id('staging_area')
    # print(last_id_of_working_tree, last_id_of_staging_area)
    if last_id_of_working_tree == last_id_of_staging_area:
        print("nothing to commit working tree is clean")
        return

    # get the last row of staging_area
    id = get_last_id('staging_area')
    folders = get_subid_by_id('staging_area', id)
    # insert the last row of staging_area to working_tree
    insert_working_tree(message=message, folders=folders)
    print("committed")

# def status():
#     modified = []
#     deleted = []
#     added = []

#     # get the last row of working_tree
#     id = get_last_id('working_tree')

#     # get the folder_file_id of the last row of working_tree
#     folder_file_id = get_row_by_id('working_tree', id)
    
#     # recursively compare the file with the folder
#     compare(folder_file_id, modified, deleted, added, folder_file_id)

def database_to_filesystem(id, path, ignoreFiles):
    # get the folder_file_id of the last row of working_tree
    folder_file_id = get_subid_by_id('folder', id)
    if folder_file_id == '':
        return

    # itterate over the folder_file_id
    for subfilesid in list(map(int, folder_file_id.split(','))):
        files = get_row_by_id(subfilesid)
        isfile = files[4]
        content = files[3]
        name = files[1][2:-1]
        folder_file_id = files[2]
        print(f'Extracting {os.path.join(path, name)}')
        if isfile == 'YES':
            # write the content to the file
            with open(os.path.join(path,name), 'wb') as file:
                file.write(content)
        else:
            # create a folder
            os.mkdir(os.path.join(path, name))
            database_to_filesystem(subfilesid, os.path.join(path, name), ignoreFiles)


def get_row_by_id(id):
    db = sqlite3.connect('.zit/database.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM folder WHERE id=? ORDER BY id LIMIT 1', (id,))
    result = cursor.fetchall()
    db.commit()
    db.close()
    if not result:
        return None
    return result[0]


if __name__ == '__main__':
    # add(os.getcwdb())
    print(get_row_by_id(0))