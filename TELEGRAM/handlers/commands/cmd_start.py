from pyrogram import Client, filters


@Client.on_message(filters.command('start'))
async def cmd_start(client, msg):
    await msg.reply('Alive')
