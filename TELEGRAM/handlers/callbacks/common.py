from pyrogram import Client, filters


@Client.on_callback_query(filters.regex(r'^Close'))
async def callback_query(bot, call):
    cid = call.message.chat.id
    mid = call.message.id

    if call.data == 'Close':
        await bot.delete_messages(cid, mid)
