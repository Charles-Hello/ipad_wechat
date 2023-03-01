import base64
import time
import subprocess
import time
import threading


from ipad_wechat.config import *
from ipad_wechat.expand import getsize, get_guid_id
from ipad_wechat.IPad_qrcode.Auth import Auth
from ipad_wechat.common import we_bot
from ipad_wechat.utils import getAuthorization,My_Redis





def main():
    if TGBOT == 'true':
        subprocess.Popen('python3 -m tg_bot', shell=True)
    bot = we_bot()
    if getsize(Filename) == 0:
        guid = bot.get_guid()
    else:
        guid = get_guid_id(Filename)
        # guid = WXRecovery(WXSerialization(guid))
        bot.WXRelease(guid)
        guid = bot.get_guid()
    if OPEN_PROXY == 'true':
        bot.WXSetProxy(guid)
    qr_code_image, uuid = bot.WXGetLoginQrcode(guid)
    filename = 'wxlogin.jpg'
    imagedata = base64.b64decode(qr_code_image)
    file = open(filename, "wb")
    file.write(imagedata)
    file.close()
    Auth(port=QRCODE_PORT, email=(QRCODE_EMAIL[0], QRCODE_EMAIL[1]))
    while True:
        time.sleep(4)
        i = My_Redis(host=Redis_ip,port=Redis_port,password=Redis_pass)
        i.Redis_set('login','true')
        wxid, wxnewpass = bot.WXCheckLoginQrcode(guid, uuid)
        if wxid:
            bot.WXSecLoginManual(guid, wxid, wxnewpass)
            bot.addserver(guid, CALL_BACK_IP)
            bot.Heartbeat(guid)
            
            def createTimer():
                t = threading.Timer(Heartbeat_cycle, repeat)
                t.start()

            def repeat():
                bot.TO_get_token(getAuthorization())
                bot.Heartbeat(guid)
                createTimer()
            createTimer()
if __name__ == "__main__":
    main()
