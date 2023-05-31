
# def function jo insert karta

# - working tree (commit_id unique primary key, message, Branch_name, time Text)
#  - commitfolders(commit_id, folder_id, file_id)
#  - folder (folder_id, folder_name, subfolder_id, file_id)
#  - files (id, file_name, content){ import os, os me se path lo; .zit folder me jao jis me database hai. agar databse raha to insert karo nahi raha to error raise karo, 



def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found.")
        return None



