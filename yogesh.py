import sqlite3
from basit import get_subid_by_id, delete_row_by_id

import tkinter as tk
import turtle

# def function jo insert karta

# - working tree (commit_id unique primary key, message, Branch_name, time Text)
#  - commitfolders(commit_id, folder_id, file_id)
#  - folder (folder_id, folder_name, subfolder_id, file_id)
#  - files (id, file_name, content){ import os, os me se path lo; .zit folder me jao jis me database hai. agar databse raha to insert karo nahi raha to error raise karo, 



def get_file_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found.", file_path)
        return None

def delete_files_from_database(table, id):
    print(table, id)
    subfolders = get_subid_by_id('folder', id)
    delete_row_by_id(table, id)
    if subfolders is None:
        return
    print(subfolders)
    for subfolder in map(int, subfolders.split(',')):
        delete_files_from_database(table, subfolder)

# if __name__ == '__main__':


def log():
    conn = sqlite3.connect('.zit/database.db')
    cursor = conn.cursor()

    # Retrieve data from the database
    # Retrieve data from the database
    cursor.execute("SELECT commit_id, message, branch_name, time FROM working_tree")
    commits = cursor.fetchall()


    def create_scrollable_window():
        root = tk.Tk()
        root.title("Git Log")
        root.geometry("800x600")

        # Create a canvas widget
        canvas = tk.Canvas(root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar widget
        scrollbar = tk.Scrollbar(root, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the content
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        # Create a canvas widget within the frame
        turtle_canvas = tk.Canvas(frame, width=800, height=600)
        turtle_canvas.pack()

        # Pass the turtle canvas to the RawTurtle constructor
        t = turtle.RawTurtle(turtle_canvas)
        t.width(2)

        def draw_bullet_point():
            t.penup()
            t.pendown()
            t.fillcolor('black')
            t.dot(12)
            t.penup()
            t.pendown()

        def draw_commit(commit_id, message, branch_name, time):
            draw_bullet_point()
            t.penup()
            t.goto(-200, t.ycor())  # Adjust the horizontal position of the bullet point
            t.pendown()
            t.penup()
            t.goto(-200, t.ycor() - 25)  # Adjust the horizontal position of the text
            t.pendown()
            t.write(f'Message: {message}\nBranch: {branch_name}\nTime: {time}', align='left', font=('Arial', 12))
            t.penup()
            t.goto(-250, t.ycor() - 75)  # Adjust the distance between logs here
            t.pendown()

        def draw_git_log():
            t.speed(5)  # Adjust the turtle speed here
            t.penup()
            t.goto(-250, 250)
            t.pendown()
            t.write('Git Log', align='center', font=('Arial', 16, 'bold'))
            t.penup()
            t.goto(-240, t.ycor() - 50)  # Adjust the horizontal position of the first bullet point
            t.pendown()

            if len(commits) == 0:
                t.write("No Data", align='left', font=('Arial', 12))
            else:
                for commit in commits:
                    commit_id, message, branch_name, time = commit
                    draw_commit(commit_id, message, branch_name, time)

            # Update the scrollable region
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        draw_git_log()

        root.mainloop()

    # Create the scrollable window
    create_scrollable_window()

    cursor.close()
    conn.close()
