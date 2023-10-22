import os
from pyrogram import Client, idle
import TELEGRAM.globals as tg


def start_telegram_bot():
    from TELEGRAM.globals import BOT
    print("BOT STARTING...")

    bot = Client("DATA\MULTIPLATFORM",
                 api_id=os.environ["API_ID"],
                 api_hash=os.environ["API_HASH"],
                 bot_token=os.environ["BOT_TOKEN"],
                 plugins=dict(root="TELEGRAM\handlers"),
                 max_concurrent_transmissions=4)

    tg.BOT = bot

    try:
        bot.stop()
    except ConnectionError:
        pass

    bot.start()
    print("BOT STARTED")
    idle()
    bot.stop()
