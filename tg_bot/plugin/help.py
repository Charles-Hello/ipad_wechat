

from tg_bot.start import ipad_bot, chat_id
from telethon import events


@ipad_bot.on(events.NewMessage(from_users=chat_id, pattern='/help'))
async def my_start(event):
    '''接收/help命令后执行程序'''
    binggo = '''使用方法如下：
/help 获取命令。
/change url 更换回调地址，例：/change http://127.11.11.11:9191
/check 检测微信状态。 
/restart 重启微信登录。'''
    await ipad_bot.send_message(chat_id, binggo)
