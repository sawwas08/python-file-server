# sqlite.py: the 1st level code file to directly interface with the database. If anything is to access the databases it is through the functions in this file only for debug and organizational reasons.
import sqlite3
from pathlib import Path

def initDbFiles():
    dbDir = Path(__file__).resolve().parent.parent.parent / "data"  # setup the var for the path identifier
    dbDir.mkdir(parents=True, exist_ok=True)                        # if its not already existing, create the data/ dir
    dbFile = dbDir / "databasefilename.db"                          # append the filename to the location of the db file to complete its full path
    
    connection = sqlite3.connect(dbFile)    # open connection with file. if file is not present it creates one.
    connection.close()                      # close connection with file to not waste system resources and block code execution from db
    print(f"successfully created at: {dbFile}")