#this code file is for functions that manage the sql database tables to store and query metadata about the files stored in disks
from controllers import sqlite
from controllers.sqlite import SqliteTypes
#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

def initDbTables(): 
    # table data is hardcoded here.
    sqlite.createTable(globals.PATH_MAIN_DB, "users")
    sqlite.createTable(globals.PATH_MAIN_DB, "files")
    sqlite.createTable(globals.PATH_MAIN_DB, "partitions") # one to many telationship with files
    sqlite.createManyToManyJoinTable(globals.PATH_MAIN_DB, "users", "partitions") # join table to relate users and files as a many-to-many relationship

    #setup users
    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "username", SqliteTypes.String)
    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "email", SqliteTypes.String)
    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "password_hash", SqliteTypes.String)
    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "avatar", SqliteTypes.Blob)

    #setup users_partitions
    #sqlite.insertForeignKey(globals.PATH_MAIN_DB, "users_partitions", )

# FUNC create 