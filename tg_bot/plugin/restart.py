
import os
from tg_bot.start import ipad_bot, chat_id
from telethon import events



@ipad_bot.on(events.NewMessage(from_users=chat_id, pattern='/restart'))
async def my_start(event):
    await ipad_bot.send_message(chat_id, "正在为你重启微信登陆程序😘\n稍后会在bot发送登录二维码🥰\n请不要忘了我哟🤩")
    wx_chat = "ps -ef | grep 'python3 -m ipad_wechat' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null;"
    bot = "ps -ef | grep 'python3 -m tg_bot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; " \
    "cd /root;python3 -m ipad_wechat"
    os.system(wx_chat)
    os.system(bot)