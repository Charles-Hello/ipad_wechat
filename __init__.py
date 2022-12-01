import requests

from ipad_wechat.config import NOLAN_URL, ToKen_Password, ToKen_Nolan_Password, ToKen_Expired, Filename
from ipad_wechat.expand import sub_file_value


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
