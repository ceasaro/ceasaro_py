BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
LIGHT_GRAY = 37
GRAY = 90
LIGHT_RED = 91
LIGHT_GREEN = 92
LIGHT_YELLOW = 93
LIGHT_BLUE = 94
LIGHT_MAGENTA = 95
LIGHT_CYAN = 96
WHITE = 97

ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def color_str(color, msg):
    return f"\033[{color}m{msg}{ENDC}"


def background_color_str(color, msg):
    return f"\033[{color+10}m{msg}{ENDC}"


def red(msg):
    return color_str(RED, msg)


def light_red(msg):
    return color_str(LIGHT_RED, msg)


def yellow(msg):
    return color_str(YELLOW, msg)


def green(msg):
    return color_str(GREEN, msg)
