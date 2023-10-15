import os
import DATA.globals as cg
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

path = cg.PATH
show_path = cg.PATH.split('\\')[-1]
show_path = f'\\{show_path}'


def keyboards(keyboard, param=None):
    if keyboard == 'ListDir':
        objects = [o for o in os.listdir(path) if not o.startswith('.')]  # don't show hidden files
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

    if keyboard == 'FileOptions':
        file = param
        btn1 = InlineKeyboardButton('🗳 UPLOAD', callback_data=f'fileup.{file}')
        btn2 = InlineKeyboardButton('🗑 DELETE', callback_data=f'filedel.{file}')
        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='File.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')
        buttons = [[btn1], [btn2], [btn_b, btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'DelConfirm':
        file = param
        btn1 = InlineKeyboardButton('⏹ NO', callback_data='File.Main')
        btn2 = InlineKeyboardButton('‼️ YES', callback_data=f'filedelyes.{file}')
        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='File.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')
        buttons = [[btn1], [btn2], [btn_b, btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb


@Client.on_callback_query(filters.regex(r'^File') | filters.regex(r'^file') | filters.regex(r'^folder'))
async def callback_query(bot, call):
    global path, show_path
    cid = call.message.chat.id
    mid = call.message.id

    if call.data == 'File.Main':
        await bot.edit_message_text(cid, mid, f'Current path\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data.startswith('folder'):
        folder = call.data.split('.')[1]
        path = f'{path}\\{folder}'
        show_path = f'{show_path}\\{folder}'

        await bot.edit_message_text(cid, mid, f'Current path\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data == 'File.Back':
        path = path[0:path.rfind('\\')]
        show_path = show_path[0:show_path.rfind('\\')]

        await bot.edit_message_text(cid, mid, f'Current path\n'
                                              f'\n'
                                              f'{show_path}',
                                    reply_markup=keyboards('ListDir'))

    if call.data.startswith('file'):
        data = call.data.split('.')[0]
        name = call.data.split('.')[1]
        ext = call.data.split('.')[2]
        file = f'{name}.{ext}'
        file_path = f'{path}\\{file}'

        if data == 'file':
            await bot.edit_message_text(cid, mid, f'Current path\n'
                                                  f'\n'
                                                  f'{show_path}\n'
                                                  f'Select what to do\n'
                                                  f'\n'
                                                  f'{file}',
                                        reply_markup=keyboards('FileOptions', file))

        if data == 'fileup':
            await bot.edit_message_text(cid, mid, f'Uploading {file}')
            await bot.send_document(cid, file_path, file_name=file)
            await bot.answer_callback_query(call.id, f'✅🗳 {file} Uploaded', show_alert=True)
            await bot.edit_message_text(cid, mid, f'Current path\n'
                                                  f'\n'
                                                  f'{show_path}',
                                        reply_markup=keyboards('ListDir'))

        if data == 'filedel':
            await bot.edit_message_text(cid, mid, f'Current path\n'
                                                  f'\n'
                                                  f'{show_path}\n'
                                                  f'\n'
                                                  f'Are you sure to delete {file}',
                                        reply_markup=keyboards('DelConfirm', file))

        if data == 'filedelyes':
            os.remove(file_path)
            await bot.answer_callback_query(call.id, f'✅🗑 {file} Deleted', show_alert=True)
            await bot.edit_message_text(cid, mid, f'Current path\n'
                                                  f'\n'
                                                  f'{show_path}',
                                        reply_markup=keyboards('ListDir'))
