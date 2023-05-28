import requests

url = "http://127.0.0.1:5000/success"  # Replace with the appropriate URL

file_path = "hey.txt"  # Replace with the actual path of the file you want to upload

# Open the file in binary mode and read its contents
with open(file_path, "rb") as file:
    file_content = file.read()

# Create a dictionary to store the file content as a byte stream
form_data = {"file": (file_path, file_content)}

# Send the POST request with the file attached
response = requests.post(url, files=form_data)

# Check the response
if response.status_code == 200:
    print("File uploaded successfully.")
else:
    print("Error uploading file:", response.status_code)
