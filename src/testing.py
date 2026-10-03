import os
import shutil
from pathlib import Path



import sys
from pathlib import Path
import globals

#Direct access to python-file-server

def functions1():
    
    Storage = globals.PATH_DBDIR / "storage-buffer/"
    print(Storage)

    goto = Path(r"C:\Users\Mark Hopkins\Documents\python-file-server") 
    finished = goto / r"readme-extra\testfolder1\movetest"   #Moving a file
    print(finished)
#destination = r"C:\Users\Mark Hopkins\Documents\python-file-server\readme-extra\testfolder2"
#dest = shutil.move(source, destination)

#print("Successfully moved file ", dest)

