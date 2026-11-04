# when win and lin support are here, this file is a wrapper to define universal functins depending on current platform type
import sys
import globals
import queue

globals.CURRENT_OS = sys.platform # Darwin == MacOS

if globals.CURRENT_OS == "win32":
    from . import windows as interface
elif globals.CURRENT_OS == "linux":
    from . import linux as interface
elif globals.CURRENT_OS == "darwin":
    from . import darwin as interface
    raise NotImplementedError(f"Operating system {globals.CURRENT_OS} is not supported.")
else:
    raise NotImplementedError(f"Operating system {globals.CURRENT_OS} is not supported.")

# region ambiguous
def init():
    print("platswitch init ran")
    interface.init()
def isAdmin():
    interface.isAdmin()
# endregion
# region WIN ONLY
def createPartitionHelperProcess():
    interface.createPartitionHelperProcess()
def tryKillHelper(p):
    interface.tryKillHelper(p)
def pipeIsConnected(p):
    interface.pipeIsConnected(p)
def pipe_json(h, message=None, buffer_size=64 * 1024):
    interface.pipe_json(h, message=None, buffer_size=64 * 1024)
def testSubprocessRun():
    interface.testSubprocessRun()
def WorkerElevated(queue):
    interface.WorkerElevated(queue)
def startRemoteAdmin():
    interface.startRemoteAdmin()
def connect_pipe(pipe_name):
    interface.connect_pipe(pipe_name)
def pipeIsConnected(pipeHandle):
    interface.pipeIsConnected(pipeHandle)
def attachPipe():
    interface.attachPipe()
# endregion
#region LINUX ONLY

#endregion