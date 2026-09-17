import os

# SNIPPET: set max import path resolution one directory higher
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

connectedDrives = os.listdrives()
globals.CONNECTED_DRIVES = connectedDrives
print(globals.CONNECTED_DRIVES)

#TODO:
# detect disks function: use python to detect all available disk drives and add their handles (paths or id or something useful) to globals

# create partition function [intermediate]: WITHOUT DAMAGING DISK CONTENTS, setup a new partition for the contents of the server, then add a sql database entry using sqlite.py to store the drive id, handles, contents, available space, and status.
#   Use ext4 filesystem (efficient linux-based fs model)
#   for function parameters, param 1 should be which drive label/drive-id to add a partition to. param 2 should be the desired size of the partition.
#   because this is a first level file, keep it extremely basic and NON context dependent. (hence the parameters) 

# create named partition function [advanced]: after creating the secure web interface and user privacy architecture, this should be a copy of create partition that accepts extra parameters to register a custom partition name and an optional password string in the sql database.

# store file function [start basic]: move a single file into a storage disk. this should require a parameter that determines which drive id the file lands in. the function should also interface with sqlite.py to create a file entry and track its location, permissions, and properties.

# transaction worker [advanced]: spawn a separate thread to execute drives.py functions from a task que (UNSAFE TO EXECUTE RAW FUNCTIONS, PASS TOKENIZED AND SANITIZED JOBS ONLY) 