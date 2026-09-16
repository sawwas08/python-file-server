# the scripts folder is for files that can be called instead of main, simply executing the functions create the db and exiting the program

import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.controllers import sqlite
sqlite.initDbFiles()