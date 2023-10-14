import os
from pyrogram import Client, idle


def start_telegram_bot():

    print('BOT STARTING...')

    bot = Client("DATA\MULTIPLATFORM",
                 api_id=os.environ['API_ID'],
                 api_hash=os.environ['API_HASH'],
                 bot_token=os.environ['BOT_TOKEN'],
                 plugins=dict(root='TELEGRAM\handlers'),
                 max_concurrent_transmissions=4)

    try:
        bot.stop()
    except ConnectionError:
        pass

    bot.start()
    print('BOT STARTED')
    idle()
    bot.stop()
