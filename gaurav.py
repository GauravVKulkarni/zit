import requests
import os
import sys
from basit import get_last_id, get_subid_by_id
from irfan import database_to_filesystem


def clone(url):
    #check config file exists and take the ip address with 5000 as port number
    urldata = url.split('/')
    username = urldata[-2]
    repo = urldata[-1]
    url = '/'.join(urldata[:-2])
    print(f"sending request to {url}")
    # take the ip address from the user
    # request for file from the server
    response = requests.get(url + '/search', data={"username": username, "repo_name": repo})
    print(f"searching for {repo} in {username}")
    if response.text.startswith('False'):
        print(response.text)
        print("Repo not found")
        return
    # if ok then add that file to .zit replaze the database file
    if response.status_code == 200:
        #create a folder named repo
        folder_name = repo
        extension = 0
        while True:
            try:
                if extension != 0:
                    folder_name = repo
                    folder_name += "_" + str(extension)
                print(f"Cloning into '{folder_name}'...")
                os.mkdir(folder_name) # if extension is 0 then don't add anything to the folder name
                break
            except FileExistsError:
                print("Folder already exists...")
                extension += 1
                pass
        #create a folder named .zit in repo directory
        print("Creating .zit folder...")
        os.mkdir(os.path.join(folder_name, '.zit'))
        #create a file named database.db
        print("Creating database.db file...")
        with open(os.path.join(folder_name, '.zit', 'database.db'), "wb") as file:
            file.write(response.content)
        

        # extracting files from the database
        print("Extracting file from the database ... ")
        os.chdir(folder_name)
        print(os.getcwd())
        working_tree_id = get_last_id("working_tree")
        # get the folder_file_id of the last row of working_tree
        folder_file_id = get_subid_by_id('working_tree', working_tree_id)
        # change dir
        database_to_filesystem(folder_file_id, os.getcwd(), [])
        # cd ..
        os.chdir('..')
        print("Cloned successfully.")
    # else:
    #     print("Error downloading file:", response.status_code, "may be check the ip address or port number or check if the flask app is running or not")


def push():
    # check if database exists
    if not os.path.exists('.zit/database.db'):
        sys.exit('error: zit is not initialized')

    if os.path.exists('.zit/config'):
        # read username and password from config file
        with open('.zit/config', 'r') as file:
            username = file.readline().strip()
            password = file.readline().strip()
            registerLogin = 'y'

        # get ip
        with open('.zit/ip.txt', 'r') as file:
            ip = file.readline().strip()

    while True:
        if not os.path.exists('.zit/config'):
            username = input("Your Username : ").strip()
            password = input("Your password : ").strip()

        if not os.path.exists('.zit/ip.txt'):
            ip = input("Ip: ").strip()
            while True:
                registerLogin = input("Do you already have an account (Y/N): ").strip()
                if registerLogin.lower() == 'y' or registerLogin.lower() == 'n':
                    break

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
            "registerLogin": "register" if registerLogin == "n" else "login",
        }
        # request for file from the server (get request)
        response = requests.post(ip + '/upload',data=user_data, files=form_data)


        if response.status_code == 200:
            if response.text.startswith('<!DOCTYPE html>'):
                print("pushed successfully.")
                # create config file
                with open('.zit/config', 'w') as file:
                    file.write(username + '\n')
                    file.write(password + '\n')
                    

                # saving ip in ip.txt
                with open('.zit/ip.txt', 'w') as file:
                    file.write(ip)
                break
            else: print(response.text)
        else:
            print("Failed uploading file:", response.status_code)
            break


def pull():
    #check if database exists
    if not os.path.exists('.zit/database.db'):
        sys.exit('error: zit is not initialized')
    # check if config file exists
    if not os.path.exists('.zit/config'):
        sys.exit('error: config file not found')

    # check if ip file exists
    if not os.path.exists('.zit/ip.txt'):
        sys.exit('error: ip.txt file not found')

    # read username and password from config file
    with open('.zit/config', 'r') as file:
        username = file.readline().strip()
        password = file.readline().strip()

    # read ip address
    with open('.zit/ip.txt') as file:
        ip = file.readline().strip()

    #get name of the repo
    folder_name = os.path.basename(os.getcwd()).replace(' ', '_')

    # request for file from the server
    response = requests.post(ip + '/download', data={"username": username, "password": password, "repo_name": folder_name})

    # if ok then add that file to .zit replaze the database file
    if response.status_code == 200:
        with open(".zit/database.db", "wb") as file:
            file.write(response.content)
        print("Pull ran successfully.")
        
    else:
        print("Error downloading file:", response.status_code, "may be check the ip address or port number or check if the flask app is running or not")