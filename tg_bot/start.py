import json
import logging
from telethon import TelegramClient, connection, Button, events


logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO,
    filemode='w')
logger = logging.getLogger(__name__)
_botjson = 'tg_bot/bot.json'

with open(_botjson, 'r', encoding='utf-8') as f:
    bot = json.load(f)
api_id = bot['api_id']
chat_id = int(bot['user_id'])
api_hash = bot['api_hash']
proxystart = bot['proxy']
StartCMD = bot['StartCMD']
TOKEN = bot['bot_token']
proxyType = bot['proxy_type']
proxy_secret = bot['proxy_password']

connectionType = connection.ConnectionTcpMTProxyRandomizedIntermediate if proxyType == "MTProxy" else connection.ConnectionTcpFull
if 'proxy_user' in bot.keys() and bot['proxy_user'] != "代理的username,有则填写，无则不用动":
    proxy = {
        'proxy_type': bot['proxy_type'],
        'addr':  bot['proxy_add'],
        'port': bot['proxy_port'],
        'username': bot['proxy_user'],
        'password': bot['proxy_password']}
elif proxyType == "MTProxy":
    proxy = (bot['proxy_add'], bot['proxy_port'], bot['proxy_password'])
else:
    proxy = (bot['proxy_type'], bot['proxy_add'], bot['proxy_port'])

# 开启tg对话
if proxystart and 'noretry' in bot.keys() and bot['noretry']:
    ipad_bot = TelegramClient('bot', api_id, api_hash, connection=connectionType,
                           proxy=proxy).start(bot_token=TOKEN)
elif proxystart:
    ipad_bot = TelegramClient('bot', api_id, api_hash, connection=connectionType,
                           proxy=proxy, connection_retries=None).start(bot_token=TOKEN)
elif 'noretry' in bot.keys() and bot['noretry']:
    ipad_bot = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)
else:
    ipad_bot = TelegramClient('bot', api_id, api_hash,
                           connection_retries=None).start(bot_token=TOKEN)
