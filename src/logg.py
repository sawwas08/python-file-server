import globals

TEXT_RESET = ""

COLOR_BLACK = "\033[30m"
COLOR_BLACK_BRIGHT = "\033[90m"
COLOR_RED = "\033[31m"
COLOR_RED_BRIGHT = "\033[91m"
COLOR_GREEN = "\033[32m"
COLOR_GREEN_BRIGHT = "\033[92m"
COLOR_YELLOW = "\033[33m"
COLOR_YELLOW_BRIGHT = "\033[93m"
COLOR_BLUE = "\033[34m"
COLOR_BLUE_BRIGHT = "\033[94m"
COLOR_MAGENTA = "\033[35m"
COLOR_MAGENTA_BRIGHT = "\033[95m"
COLOR_CYAN = "\033[36m"
COLOR_CYAN_BRIGHT = "\033[96m"
COLOR_WHITE = "\033[37m"
COLOR_WHITE_BRIGHT = "\033[97m"

FONT_BOLD = "\033[1m"
FONT_DIM = "\033[2m"
FONT_ITALIC = "\033[3m"
FONT_UNDERLINE = "\033[4m"


# log error function
def error(*args, **kwargs):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(timestamp, *args, **kwargs)



# log info function

# log warn function

# log debug function

