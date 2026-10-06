# sqlite.py: the 1st level code file to directly interface with the database. If anything is to access the databases it is through the functions in this file only for debug and organizational reasons.
import sqlite3
import dotenv
from enum import Enum
from dataclasses import dataclass
from dataclasses import fields

#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

from globals import SqliteTypes
from services import indexing
import schema

@dataclass # create a combined data structure to pass as compact parameters. (dataclass means this class is strictly a type definition for static data, not executable code)
class DbColumn:
    Name: str
    Type: SqliteTypes

# region DB Initialization
def createFile():
    globals.PATH_DBDIR.mkdir(parents=True, exist_ok=True)   # make the root/data dir
    bufferDir = globals.PATH_DBDIR / "storage-buffer/"; bufferDir.mkdir(parents=True, exist_ok=True)
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
    create_table_query = f"""CREATE TABLE IF NOT EXISTS {tableName} (id INTEGER PRIMARY KEY);"""
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

def createManyToManyJoinTable(dbFile: Path, tableOne: str, tableTwo: str):
    tableName = tableOne + "_" + tableTwo   #name of join table is t1_t2
    idOne = tableOne + "_id"; idTwo = tableTwo + "_id"
    connection = sqlite3.connect(dbFile)    # get a handle to the database
    cursor = connection.cursor()            # create a pythono cursor object (not the ai one) to operate on the database    
    create_table_query = f"""CREATE TABLE IF NOT EXISTS {tableName} (
        {idOne} INTEGER, 
        {idTwo} INTEGER, 
        PRIMARY KEY ({idOne}, {idTwo}), 
        FOREIGN KEY ({idOne}) REFERENCES {tableOne}(id) ON DELETE CASCADE,
        FOREIGN KEY ({idTwo}) REFERENCES {tableTwo}(id) ON DELETE CASCADE);"""
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

def insertColumn(dbFile: Path, tableName: str, columnName: str, columnType: SqliteTypes): # NOTE: SqliteTypes is an ENUM CLASS, which constrains valid inputs for this variable to the enumerated values in sqlitetypes
    connection = sqlite3.connect(dbFile)    # get a handle to the database
    cursor = connection.cursor()            # create a pythono cursor object (not the ai one) to operate on the database    
    
    cursor.execute(f"PRAGMA table_info({tableName});")  # PRAGMA sql command reads all data into python memory to check if the column exists
    columns = [row[1] for row in cursor.fetchall()]     # index 1 contains the column name
    if columnName not in columns:
        # hardcode sql command into string
        create_column_query = f"""ALTER TABLE {tableName} ADD COLUMN {columnName} {columnType.value};"""
        cursor.execute(create_column_query)
        connection.commit()
    else:
        print(f"\x1b[4m{columnName}\x1b[0m column already exists in table \x1b[4m{tableName}\x1b[0m at file:\n{dbFile}\n\033[33mSKIPPING COLUMN INSERTION\033[0m")
    connection.close()

# endregion

# region DB Management

def deleteRecordSingle(record: schema.SqliteRow): # the SqliteRow fields are used as conditions for the sql WHERE clause. PROBLEM: null fields can select columns that are null
    conn = sqlite3.connect(globals.PATH_MAIN_DB)
    cursor = conn.cursor()

    tableName = type(record).__name__  # derive the table to insert into from the type name of the record class parameter
    fieldsDict = {}                     # setup list for each sqlite value to go into database query
    colNames: list[str] = []
    values: list[object] = []
    for f in fields(record):        # place the fields into a key-value pair array
        v = getattr(record, f.name)
        if v is schema.MISSING:
            continue
        fieldsDict[f.name] = getattr(record, f.name)
        colNames.append(f.name)
        values.append(v)
    
    if not colNames: # safeguard
        raise ValueError("No fields provided for WHERE clause — refusing to delete everything.")
    
    print("SQLITE DELETION:\n", tableName, "\nWHERE: ", fieldsDict)

    whereClause = " AND ".join(f"{c} = ?" for c in colNames)
    command = f"DELETE FROM {tableName} WHERE {whereClause}"

    try:
        cursor.execute(command, tuple(values))
        conn.commit()
        print("rows deleted:", cursor.rowcount)
    except sqlite3.IntegrityError as e: # foreign keys may restrict deletion
        print(f"Data integrity issue: {e}"); raise
    except sqlite3.OperationalError as e: # database is locked or full
        print("Database might be locked or full", e); raise
    except sqlite3.ProgrammingError as e:
        print("DB query might have mismatching arg count", e); raise

def insertRecord(record: schema.SqliteRow):
    conn = sqlite3.connect(globals.PATH_MAIN_DB)
    cursor = conn.cursor()
    
    tableName = type(record).__name__  # derive the table to insert into from the type name of the record class parameter
    fieldsDict = {}                     # setup list for each sqlite value to go into database query
    colNames: list[str] = []
    values: list[object] = []
    
    for f in fields(record):        # place the fields into a key-value pair array and check for null values
        if getattr(record, f.name) == None:
            print("ERROR: cannot create record with null field: ", f.name, " in table: ", tableName)
            return
        fieldsDict[f.name] = getattr(record, f.name)
        colNames.append(f.name)
        values.append(getattr(record, f.name))
    
    # sqlite command: 
    print("SQLITE INSERTION:\n", tableName, "\n", fieldsDict)
    placeholders = ", ".join("?" for _ in colNames)
    command = f"INSERT INTO {tableName} ({', '.join(colNames)}) VALUES ({placeholders})"
    try:
        cursor.execute(command, values)
        conn.commit()
    except sqlite3.IntegrityError as e: # duplicate entry or constraint failure
        print(f"Data integrity issue: {e}"); raise
    except sqlite3.OperationalError as e: # database is locked or full
        print("Database might be locked or full", e); raise
# endregion