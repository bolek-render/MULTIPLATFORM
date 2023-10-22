import re
import DATA.globals as cg
from pyrogram import Client, filters
from VIDEO_REC.RecordHandler import record_handler


@Client.on_message(filters.text)
async def text_msg(bot, msg):
    cid = msg.chat.id
    text = str(msg.text)
    http_urls = re.findall(r'(https?://\S+)', text)

    fn = None
    path = None

    for url in http_urls:

        # FUSI LINKS
        if 'ourpow' and ('m3u8' or 'flv') in url:
            fn = url.split('/')[-2]
            fn = f'{fn}.mp4'
            path = f'{cg.PATH}{cg.SS}VIDS{cg.SS}FUSI'

        # RECORD LINK
        if fn is not None:

            await record_handler(url, path, fn, msg)
