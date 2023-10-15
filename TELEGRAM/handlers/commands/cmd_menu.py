from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_msg = ('🤖 BOT MENU\n'
            '\n'
            'Select')


def keyboards(keyboard):
    if keyboard == 'MenuMain':
        btn1 = InlineKeyboardButton('📋 SERVER USAGE STATS', callback_data='Usage.Main')
        btn2 = InlineKeyboardButton('📁 FILE SYSTEM', callback_data='File.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')
        buttons = [[btn1], [btn2], [btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb


@Client.on_message(filters.command('menu'))
async def cmd_menu(bot, msg):
    await bot.send_message(msg.chat.id, menu_msg,
                           reply_markup=keyboards('MenuMain'))


@Client.on_callback_query(filters.regex(r'^Menu'))
async def callback_query(bot, call):
    cid = call.message.chat.id
    mid = call.message.id

    if call.data == 'Menu.Main':
        await bot.edit_message_text(cid, mid, menu_msg,
                                    reply_markup=keyboards('MenuMain'))
