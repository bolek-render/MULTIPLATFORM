import os
import DATA.globals as cg
from TELEGRAM.BotMain import start_telegram_bot
from VIDEO_REC.UnVideos import move_videos


if __name__ == '__main__':

    cg.PATH = os.getcwd()
    cg.set_slash()

    # move_videos()

    start_telegram_bot()
