import requests
import os
import sys
from basit import get_last_id, get_subid_by_id
from irfan import database_to_filesystem


ip = "http://127.0.0.1:5000"  # Replace with the appropriate URL

def clone():
     #check if database exists
    # if os.path.exists('.zit/database.db'):
    #     sys.exit('error: zit is initialized')
    # check if config file exists
    
    username = input("Enter username: ")
    repo = input("Enter repo name: ")

    # request for file from the server
    response1 = requests.get(ip + '/search', data={"username": username, "repo_name": repo})
    if 'True' == response1.text:
        print("Repo found")
    else:
        print("Repo not found")
        return
    response = requests.get(ip + '/clone', data={"username": username, "repo_name": repo})
    # if ok then add that file to .zit replaze the database file
    if response.status_code == 200:
        #create a folder named repo
        os.mkdir(repo)
        #change the directory to repo
        os.chdir(repo)
        #create a folder named .zit
        os.mkdir('.zit')
        # change the directory to .zit
        os.chdir('.zit')
        #create a file named database.db
        with open('database.db', "wb") as file:
            file.write(response.content)
        
        #change the directory to repo
        os.chdir('..')
        working_tree_id = get_last_id("working_tree")
        # get the folder_file_id of the last row of working_tree
        folder_file_id = get_subid_by_id('working_tree', working_tree_id)
        database_to_filesystem(folder_file_id, os.getcwd(), [])
        print("Cloned successfully.")
    # else:
    #     print("Error downloading file:", response.status_code, "may be check the ip address or port number or check if the flask app is running or not")


def push():
    # check if database exists
    if not os.path.exists('.zit/database.db'):
        sys.exit('error: zit is not initialized')

    if not os.path.exists('.zit/config'):
        # ask for username and password
        username = input("Enter username: ")
        password = input("Enter password: ")
        registerLogin = input("Register or Login (r/l): ").lower()
        # create config file
        with open('.zit/config', 'w') as file:
            file.write(username + '\n')
            file.write(password + '\n')
            file.write(registerLogin + '\n')
    else:
        # read username and password from config file
        with open('.zit/config', 'r') as file:
            username = file.readline().strip()
            password = file.readline().strip()
            registerLogin = file.readline().strip()

    # reading file content
    with open(".zit/database.db", "rb") as file:
        file_content = file.read()

    # repo name
    folder_name = os.path.basename(os.getcwd())
    folder_name = folder_name.replace(" ", "_")
    form_data = {"file": (folder_name + ".db", file_content)}
    user_data = {
        "username": username,
        "password": password,
        "registerLogin": "register" if registerLogin == "r" else "login",
    }
    # request for file from the server (get request)
    response = requests.post(ip + '/upload',data=user_data, files=form_data)


    if response.status_code == 200:
        print("pushed successfully.")
    else:
        print("Error uploading file:", response.status_code)


def pull():
    #check if database exists
    if not os.path.exists('.zit/database.db'):
        sys.exit('error: zit is not initialized')
    # check if config file exists
    if not os.path.exists('.zit/config'):
        sys.exit('error: config file not found')
    # read username and password from config file
    with open('.zit/config', 'r') as file:
        username = file.readline().strip()
        password = file.readline().strip()
    #get name of the repo
    folder_name = os.path.basename(os.getcwd())
    # request for file from the server
    response = requests.get(ip + '/download', data={"username": username, "password": password, "repo_name": folder_name})
    # if ok then add that file to .zit replaze the database file
    if response.status_code == 200:
        with open(".zit/database.db", "wb") as file:
            file.write(response.content)
        print("Pulled successfully.")
    else:
        print("Error downloading file:", response.status_code, "may be check the ip address or port number or check if the flask app is running or not")