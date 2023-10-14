import shutil
import psutil
import DATA.globals as cg
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from COMMON.ConvertSize import convert_size


def keyboards(keyboard):
    if keyboard == 'UsageMain':
        btn1 = InlineKeyboardButton('📀 DISK USAGE', callback_data='Usage.Disk')
        btn2 = InlineKeyboardButton('📊 MEMORY USAGE', callback_data='Usage.Memory')
        btn3 = InlineKeyboardButton('📈 CPU USAGE', callback_data='Usage.CPU.Main')
        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='Menu.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')

        buttons = [[btn1], [btn2], [btn3], [btn_b], [btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'UsageBack':
        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='Usage.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')

        buttons = [[btn_b], [btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'TestTimes':
        btn1 = InlineKeyboardButton('⏲ 1', callback_data='Usage.CPU.1')
        btn2 = InlineKeyboardButton('⏲ 3', callback_data='Usage.CPU.3')
        btn3 = InlineKeyboardButton('⏲ 5', callback_data='Usage.CPU.5')
        btn4 = InlineKeyboardButton('⏲ 7', callback_data='Usage.CPU.7')
        btn5 = InlineKeyboardButton('⏲ 10', callback_data='Usage.CPU.10')

        btn_b = InlineKeyboardButton('🔙 BACK', callback_data='Usage.Main')
        btn_c = InlineKeyboardButton('❌ CLOSE', callback_data='Close')

        buttons = [[btn1, btn2, btn3, btn4, btn5], [btn_b, btn_c]]
        kb = InlineKeyboardMarkup(buttons)
        return kb


@Client.on_callback_query(filters.regex(r'^Usage'))
async def callback_query(bot, call):
    cid = call.message.chat.id
    mid = call.message.id

    if call.data == 'Usage.Main':
        await bot.edit_message_text(cid, mid, '📋 SERVER USAGE STATS\n'
                                              '\n'
                                              'Select',
                                    reply_markup=keyboards('UsageMain'))

    if call.data == 'Usage.Disk':
        disk = shutil.disk_usage(cg.PATH)

        await bot.edit_message_text(cid, mid, f'📀 DISK USAGE\n'
                                              f'\n'
                                              f'Total : {convert_size(disk.total)}\n'
                                              f'Free : {convert_size(disk.free)}\n'
                                              f'Used : {convert_size(disk.used)}',
                                    reply_markup=keyboards('UsageBack'))

    if call.data == 'Usage.Memory':
        memory = psutil.virtual_memory()

        await bot.edit_message_text(cid, mid, f'📊 MEMORY\n'
                                              f'\n'
                                              f'Total : {convert_size(memory[0])}\n'
                                              f'Used : {convert_size(memory[3])}\n'
                                              f'Free : {convert_size(memory[4])}\n'
                                              f'Usage : {memory[2]} %',
                                    reply_markup=keyboards('UsageBack'))

    if call.data.startswith('Usage.CPU'):
        param = call.data.split('.')[-1]

        if param == 'Main':
            await bot.edit_message_text(cid, mid, '📈 CPU USAGE\n'
                                                  '\n'
                                                  'Select test time (in seconds)',
                                        reply_markup=keyboards('TestTimes'))

        else:
            test_time = float(param)

            await bot.edit_message_text(cid, mid, '📈 CPU USAGE\n'
                                                  '\n'
                                                  '⏳ Testing, wait ...')

            cpu = psutil.cpu_percent(test_time)

            await bot.edit_message_text(cid, mid, f'📈 CPU USAGE\n'
                                                  f'\n'
                                                  f'Usage : {cpu} %',
                                        reply_markup=keyboards('UsageBack'))
