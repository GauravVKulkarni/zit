import sqlite3
import os
import sys
from irfan import init, add, commit


def main():
    # check len is greater than 1
        
    if len(sys.argv) < 2:
        sys.exit('Invalid command => Usage: git.py <command> <options>')
    command = sys.argv[1]
    match command:
        # git.py init
        case 'init':
            init()
        # git.py add <file>
        case 'add':
            #  check the len of the sys.argv
            if len(sys.argv) != 3:
                sys.exit('Invalid command => Usage: git.py add <file>')
            
            #  check if database exists
            if not os.path.exists('.zit/database.db'):
                sys.exit('error: zit is not initialized')

            # check if atleast one file is given
            try:
                print(os.getcwdb())
                add(os.getcwdb())
            except:
                sys.exit('error: something went wrong')
            print('File added successfully')
        # git.py commit -m <message>
        case 'commit':
            if len(sys.argv) > 5:
                sys.exit('Invalid command => Usage: git.py commit -m <message>')
            if sys.argv[2] != '-m':
                sys.exit('Invalid command => Usage: git.py commit -m <message>')
            if type(sys.argv[3]) != "string":
                sys.exit('Invalid command => Usage: git.py commit -m <message>')
            message = sys.argv[3]
            commit(message)
        # git.py status
        # case 'status':
        #     status()
        # git.py log
        # case 'log':
        #     log()
        case _:
            print('Invalid command => Usage: git.py <command> <options>')
            
if __name__ == '__main__':
    main()