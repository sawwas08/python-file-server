# main.py: entry point file
import os
import globals
from controllers import env
from controllers import sqlite
from controllers import drives
from platforms import windows
from services import indexing
from pathlib import Path
from dotenv import load_dotenv
from dotenv import dotenv_values

myvariable = None

def main():
    print("Main called")
    env.loadEnv() # populates globals, keep on for debug
    #sqlite.createFile() # generates database file
    #indexing.initDbTables()
    
    #drives.getConnectedDrives()
    #print(globals.CONNECTED_DRIVES)
    
    #windows.createPartition()

    print("\033[32mProcess Exited.\033[0m")
    return

def initFileSystem(): # call all functions in subdirectories for filesystem setup of a working instance
    print("initializing filesystem")
    return

main() #python is weird and doesnt automatically call entry point, so main gets called here after everything is defined 