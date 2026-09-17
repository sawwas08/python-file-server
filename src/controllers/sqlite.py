# sqlite.py: the 1st level code file to directly interface with the database. If anything is to access the databases it is through the functions in this file only for debug and organizational reasons.
import sqlite3
import dotenv


#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src import globals

def initDbFiles():
    globals.PATH_SQLITE3_DB = Path(__file__).resolve().parent.parent.parent / "data"  # setup the var for the path identifier
    globals.PATH_USER_DB = globals.PATH_SQLITE3_DB / "user.sqlite3"
    globals.PATH_INDEX_DB = globals.PATH_SQLITE3_DB / "fs-index.sqlite3"              # append the filename to the location of the db file to complete its full path

    #check if files exist, and try to not overwrite them
    if globals.PATH_USER_DB.is_file() or globals.PATH_INDEX_DB.is_file():
        overwrite = input("The file exists, are you sure you want to reset them??? (Y/N):\n")
        if overwrite.casefold() == "n".casefold() or overwrite.casefold == "no".casefold():
            # end the execution of initDbFiles() so the dbs dont get erased
            print(f"Avoided overwriting files: {globals.PATH_INDEX_DB, globals.PATH_USER_DB}"); return  

    #if all other control flow blocks fail finally overwrite/create files
    globals.PATH_USER_DB.unlink(missing_ok=True)
    globals.PATH_INDEX_DB.unlink(missing_ok=True)
    globals.PATH_SQLITE3_DB.mkdir(parents=True, exist_ok=True)  # if its not already existing, create the data/ dir
    connection = sqlite3.connect(globals.PATH_USER_DB)          # open connection with file. if file is not present it creates one.
    connection.close()                                          # connection with file is not needed in this case
    connection = sqlite3.connect(globals.PATH_INDEX_DB)
    connection.close()

    print(f"successfully created files at: {globals.PATH_INDEX_DB, globals.PATH_USER_DB}")