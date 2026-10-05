# main.py: entry point file
from dotenv import load_dotenv
from dotenv import dotenv_values
from pathlib import Path
import os
import globals
import inputengine
from controllers import env
from controllers import sqlite
from controllers import drives
from services import indexing
from services import asynchronous
from platforms import platswitch
from platforms import windows

def main():
    print("Main called")
    initSystems()
    inputengine.startInputHandling() # important, this is the main interface for the program at runtime
    print("\033[32mProcess Exited.\033[0m")
    return

def initSystems(): # call all functions in subdirectories for filesystem setup of a working instance
    env.loadEnv() # populates globals, keep on for debug
    return

main() #python is weird and doesnt automatically call entry point, so main gets called here after everything is defined 