#win-elevated.py
import sys
import time
import ctypes
from ctypes import wintypes
import json

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)

PIPE_ACCESS_DUPLEX = 0x00000003 # Constants
PIPE_TYPE_MESSAGE = 0x00000004
PIPE_READMODE_MESSAGE = 0x00000002
PIPE_WAIT = 0x00000000
ERROR_PIPE_CONNECTED = 535
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
ARG_PIPENAME = sys.argv[1]

class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", ctypes.c_void_p),
        ("bInheritHandle", wintypes.BOOL),
    ]

user32.MessageBoxA.argtypes = [
    wintypes.HWND,
    wintypes.LPCSTR,
    wintypes.LPCSTR,
    wintypes.UINT
]

user32.MessageBoxA.restype = ctypes.c_int

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

kernel32.CreateNamedPipeW.argtypes = [
    wintypes.LPCWSTR,                  # pipe name
    wintypes.DWORD,                    # open mode
    wintypes.DWORD,                    # pipe mode
    wintypes.DWORD,                    # max instances
    wintypes.DWORD,                    # out buffer size
    wintypes.DWORD,                    # in buffer size
    wintypes.DWORD,                    # default timeout
    ctypes.POINTER(SECURITY_ATTRIBUTES) # security attributes
]

kernel32.CreateNamedPipeW.restype = wintypes.HANDLE
advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD)]
advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL

kernel32.LocalFree.argtypes = [ctypes.c_void_p]

kernel32.LocalFree.restype = ctypes.c_void_p

kernel32.ConnectNamedPipe.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
]
kernel32.ConnectNamedPipe.restype = wintypes.BOOL

# non-boilerplate code: ##################################################################

def create_security_attributes():
    security_descriptor = ctypes.c_void_p()
    descriptor_size = wintypes.DWORD()
    sddl = "D:(A;;GA;;;AU)" # windows SDDL formatted security code string
    success = advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        sddl,
        1,
        ctypes.byref(security_descriptor),
        ctypes.byref(descriptor_size),
    )
    if not success:
        raise ctypes.WinError(ctypes.get_last_error())
    security_attributes = SECURITY_ATTRIBUTES()
    security_attributes.nLength = ctypes.sizeof(SECURITY_ATTRIBUTES)
    security_attributes.lpSecurityDescriptor = security_descriptor
    security_attributes.bInheritHandle = False
    return security_attributes, security_descriptor

def create_pipe(pipeName): # Create the named pipe
    security_attributes, security_descriptor = create_security_attributes()
    try:
        handle = kernel32.CreateNamedPipeW(
            pipeName,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            1,
            4096,
            4096,
            0,
            ctypes.byref(security_attributes)
        )
        if handle == INVALID_HANDLE_VALUE:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)
        return handle
    finally:
        # attribute added, free temp descriptor
        kernel32.LocalFree(security_descriptor)

def pipe_json(handle, message=None, buffer_size=64 * 1024): # second two params may be omitted, setting message as none performs a message read instead of write
    # write
    if message is not None:
        data = json.dumps(message, separators=(",", ":")).encode("utf-8")
        written = wintypes.DWORD()
        ok = kernel32.WriteFile( handle, data, len(data), ctypes.byref(written), None )

        if not ok:
            raise ctypes.WinError(ctypes.get_last_error())

        if written.value != len(data): # handle buffer overflows
            raise RuntimeError( f"Partial pipe write: {written.value}/{len(data)} bytes" )

    # read
    buffer = ctypes.create_string_buffer(buffer_size)
    read = wintypes.DWORD()
    ok = kernel32.ReadFile( handle, buffer, buffer_size, ctypes.byref(read), None )

    if not ok:
        error = ctypes.get_last_error() 
        if error == 234:  # win32 int ERROR_MORE_DATA: message was larger than read str buffer.
            chunks = [buffer.raw[:read.value]]

            while True: # while data is too big for buffer, process in parts
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
            raise ctypes.WinError(error)
    else:
        data = buffer.raw[:read.value]
    return json.loads(data.decode("utf-8"))

def pipe_read(handle, buffer_size=64 * 1024): # third param may be omitted, setting message as none performs a message read instead of write
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
            raise ctypes.WinError(error)
    else:
        data = buffer.raw[:read.value]
    return json.loads(data.decode("utf-8"))

def pipe_write(handle, message=None, buffer_size=64 * 1024): # second two params may be omitted, setting message as none performs a message read instead of write
    if message is not None:
        data = json.dumps(message, separators=(",", ":")).encode("utf-8")
        written = wintypes.DWORD()
        ok = kernel32.WriteFile( handle, data, len(data), ctypes.byref(written), None )
        if not ok:
            raise ctypes.WinError(ctypes.get_last_error())
        if written.value != len(data): # handle buffer overflows
            raise RuntimeError( f"Partial pipe write: {written.value}/{len(data)} bytes" )

print(f"Creating pipe: {ARG_PIPENAME}"); PIPE_MAIN_PROC = create_pipe(ARG_PIPENAME)
print("Pipe created:", PIPE_MAIN_PROC)
connected = kernel32.ConnectNamedPipe( PIPE_MAIN_PROC , None ) 
if not connected: # if error occurs, crash process with error
    error = ctypes.get_last_error()
    if error != ERROR_PIPE_CONNECTED:
        raise ctypes.WinError(error)
print("Connected to pipe successfully, waiting for remote process message...")
firstMessage = pipe_read(PIPE_MAIN_PROC)
if firstMessage.get("signal") != "isconnected": # parse key from json object
    raise ValueError("Main proc does not communicate success, terminating")
pipe_write(PIPE_MAIN_PROC, {"connected": "1"})
print("recieved handshake, sending handshake to finish setup")



# main code:
while True: 
    result = pipe_read(PIPE_MAIN_PROC)
    print("command recieved: ", result)
    pipe_write(PIPE_MAIN_PROC, {"status": 0})

    if result["signal"] == "msgbox":
        user32.MessageBoxA(
            None,
            b"Hello from Python!",
            b"My Application",
            0
        )

    if result["signal"] == "close": # no matter for this code, the process throws an exception and terminates anyway when it calls pipeing functions on a pipe with no reciever
        break