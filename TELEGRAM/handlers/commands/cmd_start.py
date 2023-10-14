from pyrogram import Client, filters


@Client.on_message(filters.command("start"))
async def cmd_start(bot, msg):
    await msg.reply("Alive")
