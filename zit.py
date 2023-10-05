import os
import sys
from commands import init, add, commit
from zithubcommands import clone, push, pull
import re
from zitlog import log


def main():
    command = sys.argv[1]
    match command:
        # git.py init
        case "init":
            if len(sys.argv) != 2:
                sys.exit("Invalid command => Usage: git.py init")
            init()
        # git.py add <file>
        case "add":
            #  check the len of the sys.argv
            if len(sys.argv) != 3:
                sys.exit("Invalid command => Usage: git.py add <file>")

            #  check if database exists
            if not os.path.exists(".zit/database.db"):
                sys.exit("error: zit is not initialized")

            # check if atleast one file is given
            # try:
            print(os.getcwdb())
            add(os.getcwdb())
            # except Exception as e:
            #     print(e)
            #     sys.exit('error: something went wrong')
            print("File added successfully")
        # git.py commit -m <message>
        case "commit":
            if len(sys.argv) != 4:
                sys.exit("Invalid command => Usage: git.py commit -m <message> 1")
            if sys.argv[2] != "-m":
                sys.exit("Invalid command => Usage: git.py commit -m <message> 2")
            message = sys.argv[3]
            commit(message)
        case "push":
            if len(sys.argv) != 2:
                sys.exit("Invalid command => Usage: git.py push 1")
            push()

            pass
        case "pull":
            if len(sys.argv) != 2:
                sys.exit("Invalid command => Usage: git.py pull 1")
            pull()
            pass
        case "clone":
            if len(sys.argv) != 3:
                sys.exit("Invalid command => Usage: git.py clone <url> 1")
            url = sys.argv[2]
            if (
                re.match(r"^http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:5000/.+/.+$", url)
                is None
            ):
                print("Your url is not valid : ", url)
                sys.exit("Invalid command => Usage: git.py clone <url> 2")
            clone(url)
        # git.py status
        # case 'status':
        #     status()

        # git.py log
        case "log":
            if len(sys.argv) != 2:
                sys.exit("Invalid command => Usage: git.py log 1")
            log()

        case _:
            print("Invalid command => Usage: git.py <command> <options>")


if __name__ == "__main__":
    main()
