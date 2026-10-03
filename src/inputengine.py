# input-engine.py handles runtime cli commands and command reception
import datetime
import argparse
import os
import globals
import inputengine
from services import asynchronous
from controllers import env
from controllers import sqlite
from controllers import drives
from platforms import windows
from services import indexing
from pathlib import Path
from dotenv import load_dotenv
from dotenv import dotenv_values
from platforms import platswitch

def randomfuncusedtobemain():
    env.loadEnv() # populates globals, keep on for debug
    sqlite.createFile() # generates database file
    indexing.initSchema()
    windows.createPartitionHelperProcess()
    inputfsdfsdf = input("press enter to list volumes")
    result = windows.pipe_json(globals.PROC_ELEVATED_PY, {"signal": "lstvol"})
    print(result.get("ltrs"))
    print(result.get("ltrs")[1]) # get second drive letter
    sdhfjkhk = input("press enter once more to send close command to foreign process")
    windows.pipe_json(globals.PROC_ELEVATED_PY, {"signal": "close"})
    finish = input("press enter to exit main function") # execution on main thread stops here so log can be read until user input is given
    #asynchronous.startElevatedWorker()
    #asynchronous.pushtasks()
    #asynchronous.killElevatedWorker()
    return

def startInputHandling(): # 
    os.system('cls' if os.name == 'nt' else 'clear') # clear console for server cli interface
    # Handle cli start arguments
    parser = argparse.ArgumentParser(description="CLI tool")
    parser.add_argument("-d", "--debug", action="store_true", help="Whether to run the application in debug mode for development or diagnosis.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Flag to enable verbose output.")
    parser.add_argument("-p", "--partition", action="store_true", help="Flag to enable privileged file system partitioning")
    parser.add_argument("-s", "--showhelperconsole", action="store_true", help="Flag to enable the console on the privileged remote helper process")

    args = parser.parse_args()
    
    activeFlags = [] # inform user which flags were on
    if args.verbose:
        activeFlags.append("verbose")
    if args.debug:
        activeFlags.append("debug")
    if args.partition:
        activeFlags.append("partition")
    if args.showhelperconsole:
        activeFlags.append("showhelperconsole"); globals.FLAG_SHOW_HELPER_CONSOLE = 1
    if len(activeFlags) > 0:
        print("process started with flags:\n", activeFlags)
    else:
        print("process started with flags:\nNone")
    
    while True: # main user input loop. use caution here.
        uInput = input("\033[32mPY-SERVER > \033[0m")
        if uInput in ("exit", "q", "quit", "kill"): # if uinput is any of these strings
            print("SAFELY CLOSING PROCESS")
            closeProcess()
            break # break from infinite loop, and safely begin program kill procedure
        elif uInput == "help":
            print("TODO: help guide")
        elif uInput == "listdrives":
            result = windows.pipe_json(globals.PROC_ELEVATED_PY, {"signal": "lstvol"})
            print(result)
        elif uInput == "init":
            print("TODO: first time init procedure here")
        elif uInput == "platinit":
            platswitch.init()
        elif uInput == "os":
            print("Current operating system is: ", globals.CURRENT_OS)
        elif uInput == "partitioner":
            windows.createPartitionHelperProcess()
        elif uInput == "killpart":
            windows.tryKillHelper(globals.PROC_ELEVATED_PY)
        elif uInput == "pipestatus":
            result = windows.pipeIsConnected(globals.PROC_ELEVATED_PY)
            if result == True:
                print("Pipe connected")
            else:
                print("Pipe not connected")
        else: # if no commands matched
            print("ERROR: command unknown")
    
def closeProcess(): # function to reaplce contents of uinput exit command. it tracks all sensitive state and handles it before closure
    return # TODO