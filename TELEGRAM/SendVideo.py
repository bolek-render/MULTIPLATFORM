from TELEGRAM.globals import BOT
from pyrogram.errors import RPCError
from COMMON.ConvertSize import convert_size

bot = BOT


def up_progress(current, total, client, tm, fn):
    percent = 100 * (current / total)
    bar = '▓' * int(percent / 5) + '░' * (20 - int(percent / 5))

    try:
        client.edit_message_text(tm.chat.id, tm.id, f'Uploading {fn}\n'
                                                    f'|{bar}|\n'
                                                    f'{convert_size(current)} / {convert_size(total)}'
                                                    f'  :  {percent:.2f}%')
    except RPCError:
        pass

    if current == total:
        try:
            client.edit_message_text(tm.chat.id, tm.id, f'Upload complete {fn}')
        except RPCError:
            pass


def send_video(fn, video, data, thumbnails=None):
    print('sv')
    duration = data['duration']
    width = data['width']
    height = data['height']
    caption = fn.split('.')[0]

    # thumbnails created
    tm = bot.send_message(1794541520, f'Upload staring {fn}')

    if thumbnails is not None:
        vm = bot.send_video(1794541520, video,
                            caption=caption,
                            duration=duration,
                            width=width,
                            height=height,
                            thumb=thumbnails,
                            file_name=fn,
                            progress=up_progress,
                            progress_args=(bot, tm, fn))

    # thumbnails generation failed
    else:
        vm = bot.send_video(1794541520, video,
                            caption=caption,
                            duration=duration,
                            width=width,
                            height=height,
                            file_name=fn,
                            progress=up_progress,
                            progress_args=(bot, tm, fn))
