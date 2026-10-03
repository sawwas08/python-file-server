# windows.py code that only works on windows (aka partitioning)
import subprocess
import os
import sys
import queue
from pathlib import Path
import ctypes
from subprocess import Popen #uncomment line if subprocess import doesnt work
import time
import secrets
from ctypes import wintypes
import json

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
shell32 = ctypes.windll.shell32

# SNIPPET: set max import path resolution one directory higher
import sys
from pathlib import Path
current_dir = Path(__file__).resolve().parent.parent; root_dir = current_dir.parent     # NOTE: if you want to increase directory visibility of this file even more, add .parent to the end of the preceding line.
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import globals

cwd = Path(__file__).resolve().parent
scriptCreatePartition = cwd / "create-partition-windows.bat"

# region C Definiitions
kernel32.ReadFile.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.LPVOID,
]
kernel32.ReadFile.restype = wintypes.BOOL
kernel32.WriteFile.argtypes = [
    wintypes.HANDLE,
    wintypes.LPCVOID,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.LPVOID,
]
kernel32.WriteFile.restype = wintypes.BOOL

GENERIC_READ  = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING  = 3

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,   # lpFileName
    wintypes.DWORD,     # dwDesiredAccess
    wintypes.DWORD,     # dwShareMode
    ctypes.c_void_p,    # lpSecurityAttributes
    wintypes.DWORD,     # dwCreationDisposition
    wintypes.DWORD,     # dwFlagsAndAttributes
    wintypes.HANDLE     # hTemplateFile
]
kernel32.CreateFileW.restype = wintypes.HANDLE
ATTACH_PARENT_PROCESS = -1
# endregion
#region Pipe Functions
def pipe_json(handle, message=None, buffer_size=64 * 1024): # second two params may be omitted, setting message as none performs a message read instead of write    
    try:
        # ---- Write ----
        if message is not None:
            data = json.dumps(message, separators=(",", ":")).encode("utf-8")
            written = wintypes.DWORD()
            ok = kernel32.WriteFile( handle, data, len(data), ctypes.byref(written), None )
            if not ok:
                raise ctypes.WinError(ctypes.get_last_error())
            if written.value != len(data): # handle buffer overflows
                raise RuntimeError( f"Partial pipe write: {written.value}/{len(data)} bytes" )

        # ---- Read ----
        buffer = ctypes.create_string_buffer(buffer_size)
        read = wintypes.DWORD()
        ok = kernel32.ReadFile( handle, buffer, buffer_size, ctypes.byref(read), None )
        if not ok:
            error = ctypes.get_last_error() 
            if error == 234:  # win32 int ERROR_MORE_DATA: message was larger than read str buffer.
                chunks = [buffer.raw[:read.value]]
                while True: # when data is too big for buffer, read multiple times until buffer is constructed
                    buffer = ctypes.create_string_buffer(buffer_size)
                    read = wintypes.DWORD()
                    ok = kernel32.ReadFile( handle, buffer, buffer_size, ctypes.byref(read), None )
                    chunks.append(buffer.raw[:read.value])
                    if ok:      
                        break
                    error = ctypes.get_last_error()
                    if error != 234:
                        raise ctypes.WinError(error)
                data = b"".join(chunks)
            else:
                raise ctypes.WinError(error) # likely foreign process has closed pipe
        else:
            data = buffer.raw[:read.value]
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        print("\033[31m", e, "\033[0m")

# endregion
###################################################
# region Internal functions

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

def isAdmin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def WorkerElevated(taskQueue: queue.Queue): # completely unnecessary DELETE unless saving for thread stuff
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

def startRemoteAdmin():
    try:
        if pipeIsConnected(globals.PROC_ELEVATED_PY) == 1:
            print("foreign process already connected, cannot spawn twice")
            return
        else:
            print("pipe does not exist, creating foreign proc")
        pythonExe = sys.executable # get handle/path/something to the current working python runtime
        scriptPath = globals.PATH_ROOT / "src/platforms/win-elevated.py"
        pipeId = globals.SECRET_PIPEID_WINADMINPROC; pipeName = rf"\\.\pipe\MyApp-{pipeId}" # use generated identifier for this particular IPC session.
        result = ctypes.windll.shell32.ShellExecuteW( None, "runas", pythonExe, f'"{scriptPath}" "{pipeName}"', None, globals.FLAG_SHOW_HELPER_CONSOLE )
        print("Started elevated helper. pipeName: ", pipeName)    
    except WindowsError as e:
        print(e); print("Error occurred remotely starting elevated helper procress")
    except Exception as e:
        print(e); print("Error occurred remotely starting elevated helper procress")

def connect_pipe(pipe_name): # loop on pipe connection until success or timeout
    counterVar = 0
    while True:
        handle = kernel32.CreateFileW( pipe_name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None )
        counterVar += 1
        if handle != INVALID_HANDLE_VALUE: # error check for an invalid pipe handle
            print("createfilew handle created:")
            print(handle)
            return handle
        time.sleep(0.1)
        if counterVar == 100:
            print("Timed out while waiting for foreign pipe to open, restart server or run without partitioning feature")
            break

def pipeIsConnected(pipeHandle):
    print("sending pipe status request to: ", pipeHandle)
    result = pipe_json(pipeHandle, {"signal": "status"})
    if result == None:
        globals.BOOL_HELPER_IS_ALIVE = 0
        return False
    elif result["status"] == "1":
        globals.BOOL_HELPER_IS_ALIVE = 1
        return True
    return False
    globals.BOOL_HELPER_IS_ALIVE = 0

def attachPipe():
    pipe_id = globals.SECRET_PIPEID_WINADMINPROC
    pipe_name = rf"\\.\pipe\MyApp-{pipe_id}"

    handlethatcouldbenull = connect_pipe(pipe_name)
    if handlethatcouldbenull != None:
        globals.PROC_ELEVATED_PY = handlethatcouldbenull # set win32 handle to the internal pipe number

    print("Connected!"); print("Handle:", globals.PROC_ELEVATED_PY); print("Waiting for status-check...")
    connected = pipeIsConnected(globals.PROC_ELEVATED_PY)
    if connected == 1:
        print("Foreign process handshake successful")
        globals.BOOL_HELPER_IS_ALIVE = 1
    else:
        print("Careful, there may be a rogue admin process alive on this device")

def createPartitionHelperProcess():
    if globals.BOOL_HELPER_IS_ALIVE == 1:
        connected = pipeIsConnected(globals.PROC_ELEVATED_PY)
        if connected == 0:
            print("stopped attempt to start helper proc: foreignprocisaliveflag = 1")
            return
    startRemoteAdmin()
    attachPipe()

def tryKillHelper(pipeHandle): # func is named try because the helper is its own remote admin process and we can only hope it plays nicely
    result = pipe_json(pipeHandle, {"signal": "close"})
    if result == None:
        print("No response, partitioner does not exist or isn't connected")
    elif result["status"] == "0":
        print("helper terminated")

# endregion
###################################################
# region Interface
# the following function signatures should be identical across windows.py, linux.py, and darwin.py

def init():
    print("platswitch function ran on windows.py")
    startRemoteAdmin()
    attachPipe()