import os
import DATA.globals as cg
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


path = cg.PATH
show_path = cg.PATH.split('\\')[-1]
show_path = f'\\{show_path}'


def keyboards(keyboard):

    if keyboard == 'ListDir':
        global path
        objects = [o for o in os.listdir(path) if not o.startswith('.')]
        folders = [d for d in objects if os.path.isdir(f'{path}\\{d}')]
        files = [f for f in objects if os.path.isfile(f'{path}\\{f}')]
        folder_btn = []
        file_btn = []
        buttons = []

        for folder in folders:
            btn = InlineKeyboardButton(f'🗂 {folder}', callback_data=f'folder.{folder}')
            folder_btn.append(btn)

        for file in files:
            btn = InlineKeyboardButton(f'💾 {file}', callback_data=f'file.{file}')
            file_btn.append(btn)

        for btn in folder_btn:
            buttons.append([btn])

        if path == cg.PATH:
            buttons.append([InlineKeyboardButton('🔙 BACK', callback_data='Menu.Main')])
        else:
            buttons.append([InlineKeyboardButton('↖️ FOLDER UP', callback_data='File.Back')])

        for btn in file_btn:
            buttons.append([btn])

        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='Menu.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')
        buttons.append([btn_b, btn_c])

        kb = InlineKeyboardMarkup(buttons)
        return kb


@Client.on_callback_query(filters.regex(r'^File') | filters.regex(r'^file') | filters.regex(r'^folder'))
async def callback_query(bot, call):
    global path, show_path
    cid = call.message.chat.id
    mid = call.message.id

    if call.data == 'File.Main':
        await bot.edit_message_text(cid, mid, f'Your filesystem\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data.startswith('folder'):
        folder = call.data.split('.')[1]
        path = f'{path}\\{folder}'
        show_path = f'{show_path}\\{folder}'

        await bot.edit_message_text(cid, mid, f'Your filesystem\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data == 'File.Back':
        path = path[0:path.rfind('\\')]
        show_path = show_path[0:show_path.rfind('\\')]

        await bot.edit_message_text(cid, mid, f'Your filesystem\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data.startswith('file'):
        file = call.data.split('.')[1]
        file_path = f'{path}\\{file}'
