#this code file is for functions that manage the sql database tables to store and query metadata about the files stored in disks
from controllers import sqlite
from controllers.sqlite import SqliteTypes
import sqlite3
#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

# region Schema
def initSchema(): # call only when database is being setup for the first time
    conn = sqlite3.connect(globals.PATH_MAIN_DB)
    conn.execute("BEGIN IMMEDIATE")
    sqlSchema = """
    --PRAGMA foreign_keys = ON;
    -- create database schema all at once in one sqlite/cursor call
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        full_name TEXT, -- names are separated by an underscore: LAST_FIRST. names are also hashed
        email TEXT NOT NULL UNIQUE,
        signup_date TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- partition/logical volume
    CREATE TABLE IF NOT EXISTS partitions (
        id INTEGER PRIMARY KEY,
        fs_label TEXT NOT NULL UNIQUE, -- drive letter in windows, mounted label in linux
        encryption_type TEXT, -- file or block encryption
        encryption_key TEXT,
        capacity INTEGER DEFAULT 0, -- in bytes
        free_space INTEGER DEFAULT 0, -- in bytes
        pts TEXT NOT NULL, -- partition table scheme (mbr/gpt)
        partition_type TEXT NOT NULL, -- fat32,fat12,ntfs,exfat,xenix,lynx,etc https://en.wikipedia.org/wiki/Partition_type
        operating_system TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        size INTEGER NOT NULL, -- in bytes
        is_encrypted INTEGER DEFAULT 0 NOT NULL,
        key_id INTEGER NOT NULL, 

        FOREIGN KEY (key_id) REFERENCES users (user_id)  
            ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS sharedkeys (
        id INTEGER PRIMARY KEY,
        key_text TEXT -- value of key, hashed with env secret. if null, files are stored in fs raw.        
    );

    -- JOIN TABLES (many-to-many)

    CREATE TABLE IF NOT EXISTS users_sharedkeys (
        user_id INTEGER,
        sharedkey_id INTEGER,
        PRIMARY KEY (user_id, sharedkey_id), -- Composite primary key prevents duplicate join records
        FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE,
        FOREIGN KEY (sharedkey_id) REFERENCES sharedkeys (id) ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS users_partitions ( -- TABLE IS USELESS FOR NOW, USERS NO LONGER HAVE PARTITION OWNERSHIP
        users_id INTEGER, 
        partitions_id INTEGER, 
        
        PRIMARY KEY (users_id, partitions_id), 
        FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (partitions_id) REFERENCES partitions(id) ON DELETE CASCADE);
    """
    conn.executescript(sqlSchema)
    conn.commit()
    conn.close()
    return
#endregion

#def initDbTables(): 
#    # table data is hardcoded here.
#    sqlite.createTable(globals.PATH_MAIN_DB, "users")
#    sqlite.createTable(globals.PATH_MAIN_DB, "files")
#    sqlite.createTable(globals.PATH_MAIN_DB, "partitions") # one to many telationship with files
#    sqlite.createManyToManyJoinTable(globals.PATH_MAIN_DB, "users", "partitions") # join table to relate users and files as a many-to-many relationship
#
#    #setup users
#    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "username", SqliteTypes.String)
#    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "email", SqliteTypes.String)
#    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "password_hash", SqliteTypes.String)
#    sqlite.insertColumn(globals.PATH_MAIN_DB, "users", "avatar", SqliteTypes.Blob)
#
#    #setup users_partitions
#    #sqlite.insertForeignKey(globals.PATH_MAIN_DB, "users_partitions", )