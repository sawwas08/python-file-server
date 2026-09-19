# windows.py code that only works on windows (aka partitioning)

import subprocess
import sys
import queue
from pathlib import Path
import ctypes
from subprocess import Popen #uncomment line if subprocess import doesnt work

cwd = Path(__file__).resolve().parent
scriptCreatePartition = cwd / "create-partition-windows.bat"

def testSubprocessRun(): # run an error
    arg1 = "hello"; arg2 = "world"
    result = subprocess.run(
        ["cmd", "/C", cwd / "windows-subprocess-test.bat", arg1, arg2], # construct cli run command
        capture_output=True, #python settings for console / data involved
        text=True
    )
    if result.returncode != 0: # to make a return code in bat use EXIT /B 1 where 1 is numeric code
        print(f"ERROR in create-partition-windows.bat at:\n{cwd}")
    out = result.stdout.strip()

def createPartition(): #letter: str, sizeGb: float, 
    try:
        p = subprocess.run(
            ["diskpart", "/s", "commands.txt"],
            capture_output=True, #python settings for console / data involved
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW # no terminal visible
        )
        if result.returncode != 0: # to make a return code in bat use EXIT /B 1 where 1 is numeric code
            print(f"ERROR in create-partition-windows.bat at:\n{cwd}")
        out = result.stdout.strip()
        print(out)
    except WindowsError as e:
        print(e)
        print("Try running the server again with admin!")

def createElevatedPython():
    print("createpython")
    globals.PROC_ELEVATED_PY = subprocess.Popen(
        ['python', 'win-elevated.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Treats streams as text/strings instead of bytes
    )
    #process.stdin.write("Hello from Parent\n")
    #process.stdin.flush() 
    #response = process.stdout.readline().strip()
    #print(f"[Parent] Received: {response}")

    #process.stdin.close()
    #process.stdout.close()
    globals.PROC_ELEVATED_PY.wait()

def WorkerElevated(taskQueue: queue.Queue): # completely unnecessary DELETE
    print("[Elevated-Worker] Starting thread...")
    while True:
        currentTask = taskQueue.get() # get the next queued task
        
        #check if the task is to shut down worker
        if currentTask is None:
            print("[Elevated-Worker] Terminating thread...")
            taskQueue.task_done()
            break

        #proceed to execute code from task
        try:
            if type(currentTask) is str:
                print(f"[Elevated-Worker] task is a string!!!")
            else:
                print(f"[Elevated-Worker] task is NOT a string >:(")
        except Exception as e:
            print(f"[Elevated-Worker] Error executing task: {e}")
        finally:
            # Always mark the task as done
            taskQueue.task_done()