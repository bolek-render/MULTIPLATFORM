import asyncio
from TELEGRAM.SendVideo import send_video
from TELEGRAM.globals import BOT, logs
from FUSI.ConnectionTest import connection_test
from VIDEO_REC.GetVideoData import get_video_data
from VIDEO_REC.Record_ffmpeg import record_m3u8
from VIDEO_REC.Thumbnails import gen_thumbnails
from VIDEO_REC.globals import rec_current

bot = BOT


async def record_handler(url, path, fn, msg):
    sys_message = None

    rec_coro = asyncio.to_thread(record_m3u8, url, path, fn)
    rec_task = asyncio.create_task(rec_coro)

    await asyncio.sleep(0.1)

    rec_name = fn.split('.')[0]

    message = await msg.reply(f'Trying to record : {rec_name}', disable_notification=True)

    code, text = connection_test(url)

    if code == 0:
        await bot.edit_message_text(message.chat.id, message.id, f'{text} : {rec_name}')

    if code == 1:
        await bot.edit_message_text(message.chat.id, message.id, f'{text} : {rec_name}')
        sys_message = await bot.send_message(logs, f'Trying to record : {rec_name}')

    if code == -1:
        await bot.edit_message_text(message.chat.id, message.id, f'{text} : {url}')

    if code == -1000:
        bot.send_message(logs, text)

    status, err = await rec_task

    sent_to = rec_current[fn][1]
    del rec_current[fn]

    if status:
        await bot.edit_message_text(sys_message.chat.id, sys_message.id, f'Record finished : {rec_name}')

        video = err
        data = get_video_data(video)

        if data['size'] > 10485760:  # 10 MB MINIMUM TO SET THUMBNAILS ON TELEGRAM

            await bot.edit_message_text(sys_message.chat.id, sys_message.id, f'Generating thumbnails : {rec_name}')

            thumbs_coro = asyncio.to_thread(gen_thumbnails, video, data)
            thumbs = await thumbs_coro

            await bot.edit_message_text(sys_message.chat.id, sys_message.id, f'Thumbnails finished : {rec_name}')

            if thumbs is not None:
                vid_msg = await send_video(fn, video, data, sys_message, thumbnails=thumbs)
            else:
                vid_msg = await send_video(fn, video, data, sys_message, thumbnails=None)

        else:
            vid_msg = await send_video(fn, video, data, sys_message, thumbnails=None)
