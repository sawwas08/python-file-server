# globals.py: this file is for storing global variables. It serves a similar purpose to .env, but it can hold things like lists and python data objects.
from enum import Enum
import queue

# Forward declare the existence of this variable so it's lifetime is always tied to this location forever
PASSWORD_HASH_SECRET = None
JWT_SECRET = None

PATH_ROOT = None
PATH_DBDIR = None
PATH_USER_DB = None
PATH_INDEX_DB = None
PATH_MAIN_DB = None
PATH_LIST = [PATH_MAIN_DB, PATH_USER_DB, PATH_INDEX_DB]

QUE_WORKER_ELEVATED = queue.Queue()
PROC_ELEVATED_PY = None
PIPE_ELEVATED_STDIN = None
PIPE_ELEVATED_STDOUT = None
PIPE_ELEVATED_STDERR = None



CONNECTED_DRIVES = []

class SqliteTypes(Enum): # Data type meant to contstrain a string type parameter field to one of five valid strings 
    Null = "NULL"
    Int = "INTEGER"
    Float = "REAL"
    String = "TEXT"
    Blob = "BLOB"