# globals.py: this file is for storing global variables. It serves a similar purpose to .env, but it can hold things like lists and python data objects.

# Forward declare the existence of this variable so it's lifetime is always tied to this location forever
PASSWORD_HASH_SECRET = None
JWT_SECRET = None
DATA_ROOT_PATH = None 