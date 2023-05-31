import sqlite3
import os
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
DATABASE = 'users.db'  # Replace with the path to your SQLite database file

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        username = request.form.get('username')
        password = request.form.get('password')
        registerLogin = request.form.get('registerLogin')
        
        # get the current folder path
        folder_path = os.getcwd()

        # make upload folder if it does not exist
        if not os.path.exists(folder_path + '/uploads'):
            os.mkdir(folder_path + '/uploads')

        if registerLogin == 'register':
            if not os.path.exists(folder_path + '/uploads/' + username):
                # create a folder in the uploads folder with the username
                os.mkdir(folder_path + '/uploads/' + username)

                #create a password file in that folder as password.txt
                with open(folder_path + '/uploads/' + username + '/password.txt', 'w') as file:
                    file.write(password)
            else:
                return "username already exists"
            # inside the folder make a folder named as username if it does not exist
            # save the file inside the folder
            f.save(os.path.join(folder_path, 'uploads', username, f.filename))
        else:
            # check if the username exists
            if os.path.exists(folder_path + '/uploads/' + username):
                # check if the password is correct
                with open(folder_path + '/uploads/' + username + '/password.txt', 'r') as file:
                    if file.readline() == password:
                        # save the file inside the folder
                        f.save(os.path.join(folder_path, 'uploads', username, f.filename))
                    else:
                        return "wrong password"
            else:
                return "username does not exist"




        return render_template("ack.html", name=f.filename)

@app.route('/download', methods=['GET'])
def download_file():
    username = request.form.get('username')
    password = request.form.get('password')
    repo_name = request.form.get('repo_name')

    # Construct the file path
    user_folder = os.path.join(os.getcwd(), "uploads", username)
    file_path = os.path.join(user_folder, repo_name + '.db') 
    
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/octet-stream', as_attachment=True)
    else:
        return 'error: file not found'
    

@app.route('/clone', methods=['GET'])
def clone():
    username = request.form.get('username')
    repo_name = request.form.get('repo_name')

     # Construct the file path
    user_folder = os.path.join(os.getcwd(), "uploads", username)
    print(user_folder)
    file_path = os.path.join(user_folder, repo_name + '.db') 
    
    print(file_path)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/octet-stream', as_attachment=True)
    else:
        
        return 'error: file not found'
    
@app.route('/search', methods=['GET'])
def search():
    username = request.form.get('username')
    repo_name = request.form.get('repo_name')

    # check if uploads folder exists
    print(os.getcwd())
    if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
        return "False1"
    # change the directory to uploads
    os.chdir(os.path.join(os.getcwd(), "uploads"))
    #check if the username exists
    if not os.path.exists(username):
        os.chdir(os.path.join(os.getcwd(), '..'))
        return "False2"
    # change the directory to the username
    os.chdir(username)
    # check if the repo exists
    if not os.path.exists(repo_name+'.db'):
        os.chdir(os.path.join(os.getcwd(), '..', '..'))
        return "False3"
    #change the directory back to the original
    os.chdir(os.path.join(os.getcwd(), "..", ".."))
    
    return "True"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
