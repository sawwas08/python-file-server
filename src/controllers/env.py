# PURPOSE: load env data into globals.py
import sqlite3
import os
from dotenv import load_dotenv

#snippet to up the module scanning root
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

def loadEnv():
    load_dotenv()
    rootDir = Path(__file__).resolve().parent.parent.parent     # get path of root for building other paths at beginning of main function
    globals.PATH_DBDIR = rootDir / os.getenv('PATH_DBDIR')              # path extension from env
    globals.PATH_MAIN_DB = rootDir / os.getenv('PATH_MAIN_DB')          # path extension from env
    globals.PATH_INDEX_DB = rootDir / os.getenv('PATH_INDEX_DB')        # path extension from env
    globals.PATH_USER_DB = rootDir / os.getenv('PATH_USER_DB')          # path extension from env