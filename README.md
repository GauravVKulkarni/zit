# Python-mini-project
## git's clone

## Tables
 - working tree (id, commit message, branch name)
 - commitfolder(workingtree_id, folder_id, files_id)
 - folders (id, folder_id, folder_name, sub_folder/file_id)
 - mediam b/w folder and files
 - files (id, file_id, file_name, content)

 ## imporved idea 
 - working tree (commit_id unique primary key, message, Branch_name, time Text)
 - commitfolders(commit_id, folder_id, file_id)
 - folder (folder_id, folder_name, subfolder_id, file_id)
 - files (id, file_name, content)

## imporved idea 
 - working tree (commit_id unique primary key, message, Branch_name, time Text)
 - commitfolders(commit_id, folder_file_id)
 - folder_file(id, path, subfolder_file_id, content)

## imporved idea 
    working_tree(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, branch_name TEXT DEFAULT 'master', time TEXT, add_id INTEGER, folder_file_id TEXT)

    Staging_area(id INTEGER PRIMARY KEY AUTOINCREMENT, )

    Files(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, subfolder_file_id TEXT, content TEXT)

# Functions

## git add .
- sab file/folder add karne hai + content database me store karna hai
- .gitignore maybe

## git commit
- update working tree
- just take the folder_id and and commit_id and merge it

## git log
- git graph

# GitHub
- lets say pi me ek flask server host to wo localhost access kar sakte kya
- 


```
# TODO

- [x] Table Layout
- [x] Add function algorithm
- [x] Add function k liye helper function
- [x] implementation Add function
- [x] Commit function
- [x] Git log implementaion
- [] isFileChange function
- [] gitstatus function
- [x] flask app
- [x] pi setup
- [x] git push
- [x] git pull

```
