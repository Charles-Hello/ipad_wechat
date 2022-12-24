from common import we_bot
from config import *
from expand import get_guid_id
from tg_bot.start import ipad_bot, chat_id
from telethon import events


@ipad_bot.on(events.NewMessage(from_users=chat_id, pattern='/change'))
async def change(event):
    '''接收/call命令后执行程序'''
    msg_text = event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = ''.join(msg_text[1:])
    else:
        text = None
    if not text:
        res = '''请正确使用/change命令，如
        /change url 运行改变回调地址
        '''
        await ipad_bot.send_message(chat_id, res)
    else:
        bot = we_bot()
        bot.addserver(get_guid_id, text)
