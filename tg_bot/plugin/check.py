

from common import we_bot
from tg_bot.start import ipad_bot, chat_id
from telethon import events
from expand import get_guid_id


@ipad_bot.on(events.NewMessage(from_users=chat_id, pattern='/check'))
async def check(event):
    bot = we_bot()
    res = bot.Heartbeat(get_guid_id('token.txt'))
    await ipad_bot.send_message(chat_id, res)
