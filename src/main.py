from pathlib import Path


dir_path = Path("../data/")
dir_path.mkdir(parents=True, exist_ok=True)

def main():
    print("MAIN CALLED")
    retrieveEnv()
    initFileSystem()
    return

def retrieveEnv():
    print("retrieving env")
    return

def initFileSystem():
    print("initializing filesystem")
    return

#python is weird and doesnt automatically call entry point, so main gets called here after everything is defined
main()
