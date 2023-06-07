import os
from flask import Flask, request, render_template, send_file
import re
import socket
import main

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)
@app.route('/')
def index():
    return main.index(ip_address)
    


@app.route('/generalupload', methods=['GET'])
def general():
    sendingTestpath = os.path.join(os.getcwd(), "sended")
    # save the file send by the user
    f = request.files['file']
    f.save(os.path.join(sendingTestpath, f.filename))
    return render_template("ack.html", name=f.filename)


    
@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
        # create a folder in the uploads folder
        os.mkdir(os.path.join(os.getcwd(), "uploads"))
    if request.method == 'POST':
        # info
        f = request.files['file']
        print(f)
        username = request.form.get('username')
        password = request.form.get('password')
        registerLogin = request.form.get('registerLogin')
        
        print(registerLogin)
        if registerLogin == 'register':
            # check if the username is valid
            if not re.match(r"^[a-zA-Z0-9_]+$", username):
                return "invalid username"
            # check if the password is valid
            if not re.match(r"^[a-zA-Z0-9_]+$", password):
                return "invalid password"
            # username already exists
            if os.path.exists(os.path.join(os.getcwd(), "uploads", username)):
                return "username already exists"
            else:
                # create a folder in the uploads folder with the username
                os.mkdir(os.path.join(os.getcwd(), "uploads", username))

                #create a password file in that folder as password.txt
                with open(os.path.join(os.getcwd(), "uploads", username, 'password.txt'), 'w') as file:
                    file.write(password)
        else: 
            # check username and password
            if not os.path.exists(os.path.join(os.getcwd(), "uploads", username)):
                return "username does not exist"
            with open(os.path.join(os.getcwd(), "uploads", username, 'password.txt'), 'r') as file:
                if file.read() != password:
                    return "wrong password"
        
        f.save(os.path.join(os.getcwd(), 'uploads', username, f.filename))
        return render_template("ack.html", name=f.filename)

@app.route('/download', methods=['POST'])
def download_file():
    username = request.form.get('username')
    password = request.form.get('password')
    repo_name = request.form.get('repo_name')
    # check the password
    with open('uploads\\'+username+'\\password.txt') as f:
        if password != f.readline():
            return 'Incorrect password'
    # Construct the file path
    user_folder = os.path.join(os.getcwd(), "uploads", username)
    file_path = os.path.join(user_folder, repo_name + '.db')
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/octet-stream', as_attachment=True)
    else:
        return 'error: file not found'
    
@app.route('/search', methods=['GET'])
def search():
    username = request.form.get('username')
    repo_name = request.form.get('repo_name')

    # check if uploads folder exists
    if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
        return "False1"
    #check if the username exists
    if not os.path.exists(os.path.join(os.getcwd(), "uploads", username)):
        return "False2"
    # check if the repo exists
    if not os.path.exists(os.path.join(os.getcwd(), "uploads", username, repo_name + '.db')):
        return "False3"
    return send_file(os.path.join(os.getcwd(), "uploads", username, repo_name + '.db'), mimetype='application/octet-stream', as_attachment=True)

if __name__ == '__main__': 
          # run the app
    
    app.run(host=ip_address, port=5000, debug=True)
    print("running on ip_address: " + ip_address)
        
