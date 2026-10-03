import shutil
import os
import ctypes
import subprocess

#PATH_DISKPART = shutil.which("diskpart")
#if PATH_DISKPART:
#    PATH_DISKPART = os.path.abspath(PATH_DISKPART)
#else:
#    print("diskpart not found on the system.")

#result = ctypes.windll.shell32.ShellExecuteW( None, "runas", PATH_DISKPART, f'list volume', None, 1 )
#print(result)





def removeLine(string: str):
    newline_index = string.find("\n")
    # If a newline is found, slice the string right after it
    if newline_index != -1:
        clean_text = string[newline_index + 1:]
    else:
        clean_text = string  # Fallback if no newline exists

def main(): 
    process = subprocess.Popen( ["diskpart"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True )
    stdout, stderr = process.communicate(input="list volume\n")

    volumes = [] # parse diskpart output text for drive letters
    for line in stdout.splitlines():
        if "Volume" in line and any(char.isdigit() for char in line):
            parts = line.split()
            if len(parts) > 1:
                if len(parts[2]) == 1:
                    volumes.append(parts[2])  # token 2 equivalent
    return volumes
main()