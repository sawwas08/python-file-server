# main.py: entry point file
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