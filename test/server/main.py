import os
import socket

def index():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }

            h1 {
                color: #333;
            }

            .card {
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 20px;
            }

            .card h3 {
                margin-top: 0;
            }

            ul {
                margin: 0;
                padding: 0;
                list-style-type: none;
            }

            li {
                margin-bottom: 5px;
            }

            .copy-button {
                background-color: transparent;
                border: none;
                color: #4CAF50;
                padding: 0;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin-top: 10px;
                cursor: pointer;
            }
            .copy-button:hover {
                color:white;
                background-color:black;
            }

            .tick-mark {
                color: #4CAF50;
                display: none;
            }
        </style>

        <title>ZITHUB</title>
        <script>
            function copyToClipboard(ip,db,user) {
                var textToCopy = "http://"+ip+":5000/"+user+"/"+db;
                
                var tempInput = document.createElement("textarea");
                tempInput.value = textToCopy;
                document.body.appendChild(tempInput);
                
                tempInput.select();
                tempInput.setSelectionRange(0, 99999);
                
                document.execCommand("copy");
                
                document.body.removeChild(tempInput);
                
            }
        </script>
    </head>
    <body>
        <h1>ZITHUB</h1>
    """

    if not os.path.exists("uploads"):
        html += """
            </body>
            </html>
            """
        return html 

    for user in os.listdir(os.path.join(os.getcwd(), "uploads")):
        
        html += f"""
        <div class="card">
            <h3>{user}</h3>
            <ul>
        """
        for file in os.listdir(os.path.join(os.getcwd(), "uploads", user)):
            if not file.endswith(".db"):
                continue
            html += f"""
                <li>
                    <button class="copy-button" onclick="copyToClipboard('{ip_address}','{file[:-3]}','{user}')">Zit Clone</button>
                    {file}
                </li>
            """
        html += """
            </ul>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html