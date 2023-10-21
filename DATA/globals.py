# CONSOLE COLOURS
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

# PROJECT PATH
PATH = None
SS = None


def set_slash():
    global SS
    if '/' in PATH:
        SS = '/'

    if '\\' in PATH:
        SS = '\\'
