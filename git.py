import sqlite3
import os
import sys
from irfan import init


def main():
    # check len is greater than 1
        
    if len(sys.argv) < 2:
        sys.exit('Invalid command => Usage: git.py <command> <options>')
    # commands for now
    # git.py init
    # git.py add <file>
    # git.py commit -m <message>
    # git.py status
    # git.py log
    command = sys.argv[1]
    match command:
        case 'init':
            init()
        # case 'add':
        #     #  check the len of the sys.argv
        #     if len(sys.argv) != 3:
        #         sys.exit('Invalid command => Usage: git.py add <file>')
            
        #     # check if atleast one file is given
        #     add()
        #     sys.exit('File added successfully')
        # case 'commit':
        #     # check len of the sys.argv
        #     # check m flag
        #     if len(sys.argv) > 3 and sys.argv[2] != '-m' and len(sys.argv[3]) == 0:
        #         sys.exit('Invalid command => Usage: git.py commit -m <message>')
        #     message = sys.argv[3]
        #     commit(message)
        # case 'status':
        #     status()
        # case 'log':
        #     log()
        case _:
            print('Invalid command => Usage: git.py <command> <options>')
            
if __name__ == '__main__':
    main()