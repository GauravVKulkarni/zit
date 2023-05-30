
# def function jo insert karta

# - working tree (commit_id unique primary key, message, Branch_name, time Text)
#  - commitfolders(commit_id, folder_id, file_id)
#  - folder (folder_id, folder_name, subfolder_id, file_id)
#  - files (id, file_name, content){ import os, os me se path lo; .zit folder me jao jis me database hai. agar databse raha to insert karo nahi raha to error raise karo, 

import sqlite3
import turtle

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Imaginary data for the working_tree table
commits = [
    (1, "Initial commit", "main", "2023-05-01 10:00:00"),
    (2, "Add feature A", "feature-A", "2023-05-02 15:30:00"),
    (3, "Fix bug in feature A", "feature-A", "2023-05-03 09:45:00"),
    (4, "Merge feature-A into main", "main", "2023-05-04 11:20:00"),
    (5, "Add feature B", "feature-B", "2023-05-05 14:10:00"),
    (6, "Refactor code", "main", "2023-05-06 16:55:00"),
]

screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor('white')
t = turtle.Turtle()
t.penup()
t.goto(-250, 250)
t.pendown()
t.width(2)

def draw_commit(commit_id, message, branch_name, time):
    t.write(f'Commit ID: {commit_id}\nMessage: {message}\nBranch: {branch_name}\nTime: {time}', align='left', font=('Arial', 12))
    t.penup()
    t.goto(-250, t.ycor() - 100)  # Adjust the distance between logs here
    t.pendown()

def draw_git_log():
    t.write('Git Log', align='center', font=('Arial', 16, 'bold'))
    t.penup()
    t.goto(-250, t.ycor() - 50)
    t.pendown()
    
    for i in range(len(commits)):
        commit = commits[i]
        commit_id, message, branch_name, time = commit
        draw_commit(commit_id, message, branch_name, time)

draw_git_log()
turtle.done()

cursor.close()
conn.close()



