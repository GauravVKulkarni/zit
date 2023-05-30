
# def function jo insert karta

# - working tree (commit_id unique primary key, message, Branch_name, time Text)
#  - commitfolders(commit_id, folder_id, file_id)
#  - folder (folder_id, folder_name, subfolder_id, file_id)
#  - files (id, file_name, content){ import os, os me se path lo; .zit folder me jao jis me database hai. agar databse raha to insert karo nahi raha to error raise karo, 


import turtle

#setup the window
window = turtle.Screen()
window.bgcolor("black")
window.title("Zit Log")
window.setup(width=550,height=300)


#arrow head
master_arrow = turtle.Turtle()
master_arrow.hideturtle()
master_arrow.shape("arrow")
master_arrow.pensize(6)
master_arrow.color("white")
master_arrow.penup()
master_arrow.hideturtle
master_arrow.goto(-200,80)
master_arrow.showturtle()
master_arrow.pendown()
master_arrow.write("commit", align='left', font=("Arial", 12, "bold"))
master_arrow.goto(0,80)




turtle.mainloop()







