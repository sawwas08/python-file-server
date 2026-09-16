# main.py: entry point file
import os
import globals
from controllers import sqlite
from pathlib import Path
from dotenv import load_dotenv
from dotenv import dotenv_values

myvariable = None

def main():
    print("Main called")
    retrieveEnv()
    sqlite.initDbFiles()
    return

def retrieveEnv(): # load environment vars from .env to globals.py [MIGHT MOVE TO ENV CONTROLLER PY FILE]
    load_dotenv()
    globals.DATA_ROOT_PATH = os.getenv('DATA_ROOT_PATH')
    print("retrieving env")
    return

def initFileSystem(): # call all functions in subdirectories for filesystem setup of a working instance
    print("initializing filesystem")
    return

main() #python is weird and doesnt automatically call entry point, so main gets called here after everything is defined 