# main.py: entry point file
import os
import globals
from controllers import env
from controllers import sqlite
from pathlib import Path
from dotenv import load_dotenv
from dotenv import dotenv_values

myvariable = None

def main():
    print("Main called")
    env.loadEnv()
    sqlite.initDbFiles()
    print("\033[32mProcess Exited.\033[0m")
    return

def initFileSystem(): # call all functions in subdirectories for filesystem setup of a working instance
    print("initializing filesystem")
    return

main() #python is weird and doesnt automatically call entry point, so main gets called here after everything is defined 