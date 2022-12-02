import base64
import logging
import requests
import time
import ujson
import schedule


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Any
from ipad_wechat import getAuthorization
from ipad_wechat.config import *
from ipad_wechat.expand import Ping_Add_server, getsize, get_guid_id, sub_file_value
from ipad_wechat.IPad_qrcode.Auth import Auth
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


Get_Authorization = getAuthorization()
headers = {
    'accept': 'text/plain',
    'Authorization': Get_Authorization,
    'Content-Type': 'application/json-patch+json',
}


def TO_get_token() -> str:
    global Get_Authorization
    getAuthorization()
    return Get_Authorization


def WXSetProxy(_guid: str):
    data = '{\n  "Guid": "' + _guid + '",\n  "Enable": true,\n  "Address": "' + PROXY_IP_ADDRESS + '",\n  "Port": ' + str(
        PROXY_IP_PORT) + ',\n  "UserName": "",\n  "Password": ""\n}'

    response = requests.post(f'{NOLAN_URL}/Client/WXSetProxy', headers=headers,
                             data=data)
    right_code = ujson.loads(response.text)['code']
    if right_code == 0:
        logger.info(f"恭喜你成功设置了微信登录代理：\n代理IP为{PROXY_IP_ADDRESS}\n端口为：{PROXY_IP_PORT}")
    else:
        logger.error("您的代理ip和端口设置错误")


def Heartbeat(guid: str):
    data = '{\n  "Guid": "' + guid + '"\n}'

    response = requests.post(f'{NOLAN_URL}/Heartbeat/WXHeartBeat',
                             headers=headers, data=data)
    right_code = ujson.loads(response.text)['data']
    if right_code == "心跳成功":
        logger.info("恭喜你成功续命")
    else:
        logger.error("心跳错误："+right_code)


def get_guid() -> str:
    data = '{\n  "Terminal": 2,\n  "WxData": "",\n  "Brand": "",\n  "Name": "",\n  "Imei": "",\n  "Mac": ""\n}'
    guid = requests.post(f'{NOLAN_URL}/Client/WXCreate', headers=headers,
                         data=data)
    data = ujson.loads(guid.text)
    _guid = data['data']['Guid']
    logger.info("获得的guid：" + _guid)
    sub_file_value(Filename, "guid", _guid)
    WXSetProxy(_guid)
    return _guid


def WXSerialization(guid:str) -> str:

    data = '{\n  "Guid": "'+guid+'"\n}'

    response = requests.post(f'{NOLAN_URL}/Client/WXSerialization',
                             headers=headers, data=data)
    return response.json()['data']


def WXCheckLoginQrcode(guid: str, UUID: str):
    data = '{\n  "Guid": "' + guid + '",\n  "Uuid": "' + UUID + '"\n}'

    response = requests.post(f'{NOLAN_URL}/Login/WXCheckLoginQrcode',
                             headers=headers, data=data)
    data = ujson.loads(response.text)
    # logger.info(data)
    if data['data']['wxid']:
        wxid = data['data']['wxid']
        wxnewpass = data['data']['wxnewpass']
        return wxid, wxnewpass
    else:
        logger.info("赶紧扫码！TMD")
        return None,None

def WXSecLoginManual(guid: str, wxid: str, wxnewpass: str):
    data = '{\n  "Guid": "' + guid + '",\n  "Channel": 1,\n  "UserName": "' + wxid + '",\n  "Password": "' + wxnewpass + '",\n  "Slider": true,\n  "Init": true\n}'
    response = requests.post(f'{NOLAN_URL}/Login/WXSecLoginManual',
                             headers=headers, data=data)
    # logger.info(data)
    # logger.info(response.text)
    if response.status_code == 200:
        logger.info("微信登陆成功！")
    else:
        logger.error("微信登陆失败！")

def WXRecovery(Serialization:str):
    data = '{\n  "Serialization": "'+Serialization+'"\n}'

    res  = requests.post(f'{NOLAN_URL}/Client/WXRecovery', headers=headers,
                             data=data)
    return res.json()['data']['Guid']

def WXRelease(guid:str):
    data = '{\n  "Guid": "'+guid+'"\n}'

    res  = requests.post(f'{NOLAN_URL}/Client/WXRelease', headers=headers,
                             data=data)


def addserver(guid: str):

    Ping_Add_server(CALL_BACK_IP)
    data = '{\n  "Guid": "' + guid + '",\n  "Module": "WXSyncMsg",\n  "Url": "' + CALL_BACK_IP + '"\n}'


    #先关闭，才开启。防止多个托管服务同时推送同一端口！(后续改多微信)
    requests.post(f'{NOLAN_URL}/Server/Close', headers=headers,
                             data=data)

    response = requests.post(f'{NOLAN_URL}/Server/Add', headers=headers,
                             data=data)

    right_code = ujson.loads(response.text)['data']
    # logger.info(right_code)

def WXGetLoginQrcode(guid: str):
    data = '{\n  "Guid": "' + guid + '"\n}'
    response = requests.post(f'{NOLAN_URL}/Login/WXGetLoginQrcode',
                             headers=headers, data=data)
    data = ujson.loads(response.text)
    # print(data)
    qr_code_image = data['data']['qrcode']
    uuid = data['data']['uuid']
    return qr_code_image, uuid


def main():
    if getsize(Filename) == 0:
        guid = get_guid()
    else:
        guid = get_guid_id(Filename)
        # guid = WXRecovery(WXSerialization(guid))
        WXRelease(guid)
        guid = get_guid()
        # sub_file_value(Filename, "guid", guid)
        # WXSetProxy(guid)
    qr_code_image, uuid = WXGetLoginQrcode(guid)
    filename = 'wxlogin.jpg'
    imagedata = base64.b64decode(qr_code_image)
    file = open(filename, "wb")
    file.write(imagedata)
    file.close()
    Auth(port=QRCODE_PORT,email=(QRCODE_EMAIL[0],QRCODE_EMAIL[1]))
    while True:
        time.sleep(4)
        wxid, wxnewpass = WXCheckLoginQrcode(guid, uuid)
        if wxid :
            WXSecLoginManual(guid, wxid, wxnewpass)
            addserver(guid)
            Heartbeat(guid)
            scheduler = AsyncIOScheduler()
            scheduler.add_job(Heartbeat, trigger='interval', seconds=Heartbeat_cycle,
                              args=[guid])  # 每隔5s执行一次func
            scheduler.start()
            while True:
                schedule.run_pending()  # 运行所有可运行的任务
                time.sleep(Token_cycle)
                TO_get_token()

if __name__ == "__main__":
    main()
