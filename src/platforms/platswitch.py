# when win and lin support are here, this file is a wrapper to define universal functins depending on current platform type
import sys
import globals

globals.CURRENT_OS = sys.platform # Darwin == MacOS

if globals.CURRENT_OS == "win32":
    from . import windows as interface
elif globals.CURRENT_OS == "linux":
    from . import linux as interface
elif globals.CURRENT_OS == "darwin":
    from . import darwin as interface

def init():
    print("platswitch init ran")
    interface.init()

