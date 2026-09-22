# main.py: entry point file
import os
import globals
from services import asynchronous
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
    #windows.restartAsElevated()
    
    windows.createPartitionHelperProcess()
    for i in range(5):
        inputfsdfsdf = input("press enter for a new win32 messagebox from foreign process")
        windows.pipe_json(globals.PROC_ELEVATED_PY, {"signal": "msgbox"})
    
    sdhfjkhk = input("press enter once more to send close command to foreign process")
    windows.pipe_json(globals.PROC_ELEVATED_PY, {"signal": "close"})

    finish = input("press enter to exit main function") # execution on main thread stops here so log can be read until user input is given
        

    #asynchronous.startElevatedWorker()
    #asynchronous.pushtasks()
    #asynchronous.killElevatedWorker()

    print("\033[32mProcess Exited.\033[0m")
    return

def initFileSystem(): # call all functions in subdirectories for filesystem setup of a working instance
    print("initializing filesystem")
    return

main() #python is weird and doesnt automatically call entry point, so main gets called here after everything is defined 