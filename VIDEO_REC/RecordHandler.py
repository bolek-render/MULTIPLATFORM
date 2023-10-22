import asyncio
from TELEGRAM.globals import BOT
from FUSI.ConnectionTest import connection_test
from TELEGRAM.globals import errors
from VIDEO_REC.Record_M3U8 import record_m3u8


bot = BOT


async def record_handler(url, path, fn, msg):
    coro = asyncio.to_thread(record_m3u8, url, path, fn)
    task = asyncio.create_task(coro)
    await asyncio.sleep(0.1)

    rec_name = fn.split('.')[0]
    bm = await msg.reply(f'Trying to record : {rec_name}', disable_notification=True)

    code, text = connection_test(url)

    if code == 0:
        await bot.edit_message_text(bm.chat.id, bm.id, f'{text} : {rec_name}')

    if code == 1:
        await bot.edit_message_text(bm.chat.id, bm.id, f'{text} : {rec_name}')

    if code == -1:
        await bot.edit_message_text(bm.chat.id, bm.id, f'{text} : {url}')

    if code == -1000:
        bot.send_message(errors, text)

    status, error = await task

    if status:
        # send video
        pass
