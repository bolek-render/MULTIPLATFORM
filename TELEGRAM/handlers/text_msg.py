import re
import DATA.globals as cg
from pyrogram import Client, filters
from VIDEO_REC.RecordHandler import record_handler


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

            await record_handler(url, path, fn_ffmpeg, msg)

        # RECORD LINK STREAMLINK
        if fn_streamlink is not None:

            pass
