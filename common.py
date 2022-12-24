import sys
if "tg_bot" not in str(sys.argv[0]):
    from ipad_wechat.utils import getAuthorization
    from ipad_wechat.config import *
    from ipad_wechat.expand import Ping_Add_server, sub_file_value
else:
    from utils import getAuthorization
    from config import *
    from expand import Ping_Add_server, sub_file_value
import logging
import ujson
import requests

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class we_bot:
    def __init__(self) -> None:
        self.headers = {
            'accept': 'text/plain',
            'Authorization': getAuthorization(),
            'Content-Type': 'application/json-patch+json',
        }

    def TO_get_token(self, demo) -> str:
        self.headers = {
            'accept': 'text/plain',
            'Authorization': demo,
            'Content-Type': 'application/json-patch+json',
        }

    def WXSetProxy(self, _guid: str):
        data = '{\n  "Guid": "' + _guid + '",\n  "Enable": true,\n  "Address": "' + PROXY_IP_ADDRESS + '",\n  "Port": ' + str(
            PROXY_IP_PORT) + ',\n  "UserName": "",\n  "Password": ""\n}'

        response = requests.post(f'{NOLAN_URL}/Client/WXSetProxy', headers=self.headers,
                                 data=data)
        right_code = ujson.loads(response.text)['code']
        if right_code == 0:
            logger.info(
                f"恭喜你成功设置了微信登录代理：\n代理IP为{PROXY_IP_ADDRESS}\n端口为：{PROXY_IP_PORT}")
        else:
            logger.error("您的代理ip和端口设置错误")

    def Heartbeat(self, guid: str):
        data = '{\n  "Guid": "' + guid + '"\n}'

        response = requests.post(f'{NOLAN_URL}/Heartbeat/WXHeartBeat',
                                 headers=self.headers, data=data)
        right_code = ujson.loads(response.text)['data']
        if right_code == "心跳成功":
            text = "微信状态❣"
            logger.info("恭喜你成功续命")

        else:
            text = "微信状态💔"
            logger.error("心跳错误：")
            logger.error(right_code)
        return text

    def get_guid(self) -> str:
        data = '{\n  "Terminal": 2,\n  "WxData": "",\n  "Brand": "",\n  "Name": "",\n  "Imei": "",\n  "Mac": ""\n}'
        guid = requests.post(f'{NOLAN_URL}/Client/WXCreate', headers=self.headers,
                             data=data)
        print(guid.text)
        data = ujson.loads(guid.text)
        _guid = data['data']['Guid']
        logger.info("获得的guid：" + _guid)
        sub_file_value(Filename, "guid", _guid)
        # WXSetProxy(_guid)
        return _guid

    def WXSerialization(self, guid: str) -> str:

        data = '{\n  "Guid": "'+guid+'"\n}'

        response = requests.post(f'{NOLAN_URL}/Client/WXSerialization',
                                 headers=self.headers, data=data)
        return response.json()['data']

    def WXCheckLoginQrcode(self, guid: str, UUID: str):
        data = '{\n  "Guid": "' + guid + '",\n  "Uuid": "' + UUID + '"\n}'

        response = requests.post(f'{NOLAN_URL}/Login/WXCheckLoginQrcode',
                                 headers=self.headers, data=data)
        data = ujson.loads(response.text)
        # logger.info(data)
        if data['data']['wxid']:
            wxid = data['data']['wxid']
            wxnewpass = data['data']['wxnewpass']
            return wxid, wxnewpass
        else:
            logger.info("赶紧扫码！TMD")
            return None, None

    def WXSecLoginManual(self, guid: str, wxid: str, wxnewpass: str):
        data = '{\n  "Guid": "' + guid + '",\n  "Channel": 1,\n  "UserName": "' + wxid + \
            '",\n  "Password": "' + wxnewpass + '",\n  "Slider": true,\n  "Init": true\n}'
        response = requests.post(f'{NOLAN_URL}/Login/WXSecLoginManual',
                                 headers=self.headers, data=data)
        # logger.info(data)
        # logger.info(response.text)
        if response.status_code == 200:
            logger.info("微信登陆成功！")
        else:
            logger.error("微信登陆失败！")

    def WXRecovery(self, Serialization: str):
        data = '{\n  "Serialization": "'+Serialization+'"\n}'

        res = requests.post(f'{NOLAN_URL}/Client/WXRecovery', headers=self.headers,
                            data=data)
        return res.json()['data']['Guid']

    def WXRelease(self, guid: str):
        data = '{\n  "Guid": "'+guid+'"\n}'

        res = requests.post(f'{NOLAN_URL}/Client/WXRelease', headers=self.headers,
                            data=data)

    def addserver(self, guid, CALL_BACK_IP: str):

        Ping_Add_server(CALL_BACK_IP)
        data = '{\n  "Guid": "' + guid + \
            '",\n  "Module": "WXSyncMsg",\n  "Url": "' + CALL_BACK_IP + '"\n}'

        # 先关闭，才开启。防止多个托管服务同时推送同一端口！(后续改多微信)
        requests.post(f'{NOLAN_URL}/Server/Close', headers=self.headers,
                      data=data)

        response = requests.post(f'{NOLAN_URL}/Server/Add', headers=self.headers,
                                 data=data)

        right_code = ujson.loads(response.text)['data']
        # logger.info(right_code)

    def WXGetLoginQrcode(self, guid: str) -> str:
        try:
            data = '{\n  "Guid": "' + guid + '"\n}'
            response = requests.post(f'{NOLAN_URL}/Login/WXGetLoginQrcode',
                                     headers=self.headers, data=data)
            data = ujson.loads(response.text)
            # print(data)
            qr_code_image = data['data']['qrcode']
            uuid = data['data']['uuid']
            return qr_code_image, uuid
        except Exception as e:
            logging.error("代理函数报错：")
            logging.error(e)
            os._exit(0)
