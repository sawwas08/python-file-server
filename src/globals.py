# globals.py: this file is for storing global variables. It serves a similar purpose to .env, but it can hold things like lists and python data objects.

# Forward declare the existence of this variable so it's lifetime is always tied to this location forever
PASSWORD_HASH_SECRET = None
JWT_SECRET = None

PATH_DBDIR = None
PATH_USER_DB = None
PATH_INDEX_DB = None
PATH_MAIN_DB = None 
PATH_LIST = [PATH_MAIN_DB, PATH_USER_DB, PATH_INDEX_DB]

CONNECTED_DRIVES = []