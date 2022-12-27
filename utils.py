import requests
import sys
import redis
import re


if "tg_bot" not in str(sys.argv[0]):
    from ipad_wechat.config import NOLAN_URL, ToKen_Password, ToKen_Nolan_Password, ToKen_Expired, Filename
    from ipad_wechat.expand import sub_file_value
else:
    from config import NOLAN_URL, ToKen_Password, ToKen_Nolan_Password, ToKen_Expired, Filename
    from expand import sub_file_value


def getAuthorization() -> str:
    headers = {
        'accept': '*/*',
        'Authorization': f'{ToKen_Password}',
    }

    params = {
        'password': f'{ToKen_Nolan_Password}',
        'minutes': f'{ToKen_Expired}',
    }
    _getAuthorization = requests.get(f'{NOLAN_URL}/Token/Create', params=params,
                                     headers=headers).text

    # logger.logger.info("获得的Authorization是:" + _getAuthorization)
    sub_file_value(Filename, "", _getAuthorization)
    return _getAuthorization


class My_Redis:
    def __init__(self, host: str, port: int, password=None):
        if password is None:
            self.r = redis.StrictRedis(
                host=host, port=port, decode_responses=True)
        else:
            self.r = redis.StrictRedis(
                host=host, port=port, password=password, decode_responses=True)

    def Redis_pipe(self, key: str) -> str:
        try:
            with self.r.monitor() as m:
                for command in m.listen():
                    a = command['command']
                    b = a.split(" ")
                    method = b[0].lower()
                    _key = b[1]
                    if re.findall(r'get|set', method) != [] and _key == key:
                        return self.r.get(key)
        except Exception as e:
            print(e)

    def Redis_set(self, key: str, value: str):
        self.r.set(key, value)
