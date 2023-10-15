from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import RPCError
from COMMON.ConvertSize import convert_size
import ffmpeg


user_job = {}


def keyboards(keyboard):

    if keyboard == 'video_main':
        btn1 = InlineKeyboardButton('INVERT COLOURS', callback_data='video_invert')
        btn2 = InlineKeyboardButton('TRIM VIDEO', callback_data='video_trim')
        btn3 = InlineKeyboardButton('MERGE VIDEOS', callback_data='video_merge')
        btn4 = InlineKeyboardButton('CLOSE', callback_data='close')
        buttons = [[btn1], [btn2], [btn3], [btn4]]
        kb = InlineKeyboardMarkup(buttons)
        return kb


@Client.on_message(filters.video)
async def video_msg(bot, msg):
    cid = msg.chat.id
    user_job[cid] = msg
    await bot.send_message(cid, 'What do you want to do', reply_markup=keyboards('video_main'))


async def dl_progress(current, total, client, bm):
    percent = 100 * (current / total)
    bar = '▓' * int(percent / 5) + '░' * (20 - int(percent / 5))

    try:
        await client.edit_message_text(bm.chat.id, bm.id, f'|{bar}|\n'
                                                          f'{convert_size(current)} / {convert_size(total)}'
                                                          f'  :  {percent:.2f}%')
    except RPCError:
        pass

    if current == total:
        try:
            await client.edit_message_text(bm.chat.id, bm.id, f'Download complete')
        except RPCError:
            pass


@Client.on_callback_query(filters.regex('video_invert'))
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id
    video_message = user_job[cid]

    bm = await client.edit_message_text(cid, mid, 'Download starting')
    video_path = await video_message.download(progress=dl_progress, progress_args=(client, bm))
