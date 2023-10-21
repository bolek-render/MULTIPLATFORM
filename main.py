import os
import DATA.globals as cg
from TELEGRAM.BotMain import start_telegram_bot


if __name__ == '__main__':
    cg.PATH = os.getcwd()
    cg.set_slash()

    start_telegram_bot()
