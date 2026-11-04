import os
from pathlib import Path
import shutil

# SNIPPET: set max import path resolution one directory higher
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent; root_dir = current_dir.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals
from . import sqlite

def getConnectedDrives(): # put the code into a function so it can be ran from main()
    if globals.CURRENT_OS == "win32":
        connectedDrives = os.listdrives() # function scoped variable
        globals.CONNECTED_DRIVES.clear() # clear once before the loop so it populates correctly
        for drive in connectedDrives: # instead of overwriting global value, clear and rewrite the new detected drives into global var as a pathlib Path object ("C://" -> WindowsPath('C:/'))
            globals.CONNECTED_DRIVES.append(Path(drive)) # os.listdrives returns strings, so each string is turned into pathlib object
    elif globals.CONNECTED_DRIVES == "linux":
        labelDir = Path("/dev/disk/by-label")
        if labelDir.is_dir() and not any(labelDir.iterdir()):
            print("Drive labels directory is empty or does not exist")
        connectedDrives = list(labeldir.iterdir())
        print(connectedDrives)


def legacySetRepoDir(ntDriveLetter: Path): # path object must be an available drive letter
    u = input("Enter drive letter, one character only:\n")
    if len(u) is not 1:
        print("Enter ONE character, re-run command")
    else:
        u = u + ":"
        path = Path(uInput1)
        print("DEBUG: ", path)
        drives.legacySetRepoDir(path)


    globals.LEGACY_PATH_DATA_DIR = path / ".pfsdata"
    globals.LEGACY_PATH_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("path: ", globals.LEGACY_PATH_DATA_DIR)

# defining the move folders
test1 = Path("E:/python-file-server/src/backend/testfolder1")
test2 = Path("E:/python-file-server/src/backend/testfolder2")    

def moveFile(source, destination): # Making the function to move files and recording information
    file_name = source.name
    file_size = source.stat().st_size

    shutil.move(source, destination)

    new_path = destination / file_name

    sqlite.createFile(
        file_name,
        str(new_path),
        file_size
    )


#for item in test1.iterdir():
    #if item.is_file():
        #moveFile(item, test2)

#TODO:
# detect disks function: use python to detect all available disk drives and add their handles (paths or id or something useful) to globals

# create partition function [intermediate]: WITHOUT DAMAGING DISK CONTENTS, setup a new partition for the contents of the server, then add a sql database entry using sqlite.py to store the drive id, handles, contents, available space, and status.
#   Use ext4 filesystem (efficient linux-based fs model)
#   for function parameters, param 1 should be which drive label/drive-id to add a partition to. param 2 should be the desired size of the partition.
#   because this is a first level file, keep it extremely basic and NON context dependent. (hence the parameters) 

# create named partition function [advanced]: after creating the secure web interface and user privacy architecture, this should be a copy of create partition that accepts extra parameters to register a custom partition name and an optional password string in the sql database.

# store file function [start basic]: move a single file into a storage disk. this should require a parameter that determines which drive id the file lands in. the function should also interface with sqlite.py to create a file entry and track its location, permissions, and properties.

# transaction worker [advanced]: spawn a separate thread to execute drives.py functions from a task que (UNSAFE TO EXECUTE RAW FUNCTIONS, PASS TOKENIZED AND SANITIZED JOBS ONLY) 

# resize partition function: given a function parameter for size and partition id/handle, change the size of the given partition

