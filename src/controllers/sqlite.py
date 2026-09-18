# sqlite.py: the 1st level code file to directly interface with the database. If anything is to access the databases it is through the functions in this file only for debug and organizational reasons.
import sqlite3
import dotenv
from enum import Enum
from dataclasses import dataclass

#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

#import globals

class SqliteTypes(Enum): # create a data type to enforce that DbColumn has one of the few valid type IDs for sqlite
    Null = "NULL"
    Int = "INTEGER"
    Float = "REAL"
    String = "TEXT"
    Blob = "BLOB"

@dataclass # create a combined data structure to pass as compact parameters. (dataclass means this class is strictly a type definition for static data, not executable code)
class DbColumn:
    Name: str
    Type: SqliteTypes

def createFile():
    globals.PATH_DBDIR.mkdir(parents=True, exist_ok=True)   # make the root/data dir
    temp = [globals.PATH_MAIN_DB]                           # create iterative list for iteration of sql file restoration
    for path in temp:                                       # perform iteration (path is a variable name that accesses the contents of temp[current loop index])
        if path.is_file():
            whetherToOverwrite = input(f"\033[33mThe following file exists, are you sure you want to overwrite it?\033[0m\n{path}\n(Y/N):\n")
            if whetherToOverwrite.casefold() == "y".casefold() or whetherToOverwrite.casefold() == "yes".casefold():
                path.unlink(missing_ok=True)        # remove existing file if user chooses to overwrite
                connection = sqlite3.connect(path)  # connecting sqlite automatically creates a db file if it isnt already present at the given path
                connection.close()                  # handle to database is not used here, so it is cleaned from memory
                print(f"\033[32mFile overwritten: \033[0m{path}")
            else: 
                print("\033[31mOverwrite denied.\033[0m")
        else:   # if current file does not exist
            print(f"\033[32mFile doesn't exist, writing to: \033[0m{path}")
            path.unlink(missing_ok=True)        
            connection = sqlite3.connect(path)
            connection.close()
        # now the loop repeates for next path in temp[]

def createTable(dbFile: Path, tableName: str):
    connection = sqlite3.connect(dbFile)    # get a handle to the database
    cursor = connection.cursor()            # create a pythono cursor object (not the ai one) to operate on the database    
    create_table_query = f"""               
    CREATE TABLE IF NOT EXISTS {tableName} (
        id INTEGER PRIMARY KEY
    );"""
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

# FUNCTION create table: creates a table in the sql database

# FUNCTION 