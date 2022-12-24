
from tg_bot.start import ipad_bot, chat_id
from telethon import events


@ipad_bot.on(events.CallbackQuery(data=b'auth'))
async def handler(event):
    # Pop-up message with alert
    await ipad_bot.send_message(chat_id, 'https://t.me/Hss114060')


@ipad_bot.on(events.CallbackQuery(data=b'donate'))
async def handler(event):
    await ipad_bot.send_message(chat_id, "感谢大佬支持", file='/root/ipad_wechat/tg_bot/donate.jpg')


@ipad_bot.on(events.CallbackQuery(data=b'help'))
async def handler(event):
    binggo = '''使用方法如下：
/help 获取命令。
/change url 更换回调地址，例：/change http://127.11.11.11:9191
/check 检测微信状态。 
/restart 重启微信登录。'''
    await ipad_bot.send_message(chat_id, binggo)
