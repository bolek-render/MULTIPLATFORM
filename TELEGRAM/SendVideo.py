import time
from TELEGRAM.globals import BOT, videos_target
from pyrogram.errors import RPCError
from COMMON.ConvertSize import convert_size

bot = BOT
last_update = float()


async def up_progress(current, total, client, tm, fn):
    global last_update
    percent = 100 * (current / total)
    bar = '▓' * int(percent / 5) + '░' * (20 - int(percent / 5))

    try:
        if (time.time() - last_update) > 3:
            last_update = time.time()

            await client.edit_message_text(tm.chat.id, tm.id, f'Uploading {fn}\n'
                                                              f'|{bar}|\n'
                                                              f'{convert_size(current)} / {convert_size(total)}'
                                                              f'  :  {percent:.2f}%')
    except RPCError:
        pass

    if current == total:
        try:
            await client.edit_message_text(tm.chat.id, tm.id, f'Upload complete {fn}')
        except RPCError:
            pass


async def send_video(fn, video, data, msg, thumbnails=None, caption=None):
    global last_update
    duration = data['duration']
    width = data['width']
    height = data['height']
    if caption is None:
        caption = fn.split('.')[0]

    message = await bot.edit_message_text(msg.chat.id, msg.id, f'Upload staring {fn}')
    last_update = time.time()

    if thumbnails is not None:
        vm = await bot.send_video(videos_target, video,
                                  caption=caption,
                                  duration=duration,
                                  width=width,
                                  height=height,
                                  thumb=thumbnails,
                                  file_name=fn,
                                  progress=up_progress,
                                  progress_args=(bot, message, fn))

    else:
        vm = await bot.send_video(videos_target, video,
                                  caption=caption,
                                  duration=duration,
                                  width=width,
                                  height=height,
                                  file_name=fn,
                                  progress=up_progress,
                                  progress_args=(bot, message, fn))

    return vm.video.file_id, caption
