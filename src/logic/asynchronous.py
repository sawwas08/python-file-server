# managing async tasks and worker threads
#global async data remains in globals
import threading
import time
# SNIPPET: set max import path resolution one directory higher
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent.parent; root_dir = current_dir.parent     # NOTE: if you want to increase directory visibility of this file even more, add .parent to the end of the preceding line.
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

from platforms import windows

def startElevatedWorker():
    worker_thread = threading.Thread(target=windows.WorkerElevated, args=(globals.QUE_WORKER_ELEVATED,), daemon=True)
    worker_thread.start()

def killElevatedWorker():
    globals.QUE_WORKER_ELEVATED.put(None) # send kys task to elevated worker

def pushtasks(): # DELETE
    print("Pushing tasks to queue...")
    globals.QUE_WORKER_ELEVATED.put("stringvaluetest")
    time.sleep(4)
    globals.QUE_WORKER_ELEVATED.put(125)
    # Allow time to see them process asynchronously
    time.sleep(2)
    print("stopping worker")
    killElevatedWorker()
    