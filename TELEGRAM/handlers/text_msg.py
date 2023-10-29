import re
import time
import DATA.globals as cg
from pyrogram import Client, filters
from COMMON.ConvertTime import convert_time
from VIDEO_REC.RecordHandler import record_handler
from VIDEO_REC.globals import rec_current


@Client.on_message(filters.text)
async def text_msg(bot, msg):
    cid = msg.chat.id
    text = str(msg.text)
    http_urls = re.findall(r'(https?://\S+)', text)

    fn_ffmpeg = None
    fn_streamlink = None
    path = None

    for url in http_urls:

        # FUSI LINKS
        if 'ourpow' and ('m3u8' or 'flv') in url:
            fn_ffmpeg = url.split('/')[-2]
            fn_ffmpeg = f'{fn_ffmpeg}.mp4'
            path = f'{cg.PATH}{cg.SS}VIDS{cg.SS}FUSI'

        # INSTA LINKS
        if 'instagram' and 'mpd' in url:
            fn_streamlink = f'insta.mp4'
            path = f'{cg.PATH}{cg.SS}VIDS{cg.SS}INSTA'

        # RECORD LINK FFMPEG
        if fn_ffmpeg is not None:
            if fn_ffmpeg not in rec_current.keys():
                rec_current[fn_ffmpeg] = (time.time(), [cid])
                await record_handler(url, path, fn_ffmpeg, msg)
            else:
                start_time = rec_current[fn_ffmpeg][0]
                cids = rec_current[fn_ffmpeg][1]
                rec_name = fn_ffmpeg.split('.')[0]
                rec_time = time.time() - start_time

                await msg.reply(f'{rec_name} - Recording since : {convert_time(rec_time)}',
                                disable_notification=True)

                if cid not in cids:
                    cids.append(cid)
                    rec_current[fn_ffmpeg] = (start_time, cids)

        # RECORD LINK STREAMLINK
        if fn_streamlink is not None:

            pass
