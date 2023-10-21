import re
import DATA.globals as cg
from pyrogram import Client, filters
from FUSI.ConnectionTest import connection_test
from TELEGRAM.globals import errors
from VIDEO_REC.Record_M3U8 import RecordM3U8


@Client.on_message(filters.text)
async def text_msg(bot, msg):
    cid = msg.chat.id
    text = str(msg.text)
    http_urls = re.findall(r'(https?://\S+)', text)

    fn = None
    v_path = None
    rec_name = None

    for url in http_urls:

        # FUSI LINKS
        if 'ourpow' and ('m3u8' or 'flv') in url:
            fn = url.split('/')[-2]
            rec_name = fn
            fn = f'{fn}.mp4'
            v_path = f'{cg.PATH}{cg.SS}VIDS{cg.SS}FUSI'

        # RECORD LINK
        if fn is not None:
            record = RecordM3U8(url, v_path, fn)
            record.run()

            bm = await msg.reply(f'Trying to record : {rec_name}', disable_notification=True)

            code, err = connection_test(url)

            if code == 0:
                await bot.edit_message_text(bm.chat.id, bm.id, f'Offline / pause / lag : {rec_name}')

            if code == 1:
                await bot.edit_message_text(bm.chat.id, bm.id, f'Recording : {rec_name}')

            if code == -1:
                await bot.edit_message_text(bm.chat.id, bm.id, f'{err} : {url}')

            if code == -1000:
                bot.send_message(errors, err)
