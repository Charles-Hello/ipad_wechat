

from tg_bot.utils import *
from tg_bot.start import *
from utils import My_Redis
from config import Redis_ip,Redis_port


async def hello():
    info = '[项目地址](https://github.com/Charles-Hello/ipad_wechat.git)'
    btn = [[Button.inline('打赏奶茶', data="donate"), Button.inline(
        '联系作者', data="auth"), Button.inline('使用命令help', data="help")]]
    await ipad_bot.send_message(chat_id, "🥰欢迎您😚使用本项目地址❤--->"+info, buttons=btn, file='ipad_wechat.png')
    await ipad_bot.send_message(chat_id, "🥰麻烦您扫码登录微信💝", file='wxlogin.jpg')


if __name__ == "__main__":
    i = My_Redis(host=Redis_ip[0], port=Redis_port)
    i.Redis_pipe('login')
    with ipad_bot:
        ipad_bot.loop.create_task(hello())
        ipad_bot.loop.run_forever()
