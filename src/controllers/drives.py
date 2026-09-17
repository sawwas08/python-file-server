import os


# SNIPPET: set max import path resolution one directory higher
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src import globals

connectedDrives = os.listdrives()
globals.CONNECTED_DRIVES = connectedDrives
print(globals.CONNECTED_DRIVES)
#if str(root_dir) not in sys.path:
#    sys.path.insert(0, str(root_dir))






