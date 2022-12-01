import re
import json
import requests
from urllib.parse import unquote


class Qrcode_api():
    def upload(self, qr_file):
        """
        upload
        :param qr_file:
        :return:
        """
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
            "referer": "https://cli.im/tools"
        }
        upload_url = "https://upload.api.cli.im/upload.php?kid=cliim"
        files = {"Filedata": ('wxlogin.jpg', open(qr_file, 'rb'),)}

        r = requests.post(upload_url, files=files, headers=header)

        img_url = re.findall('back=#(.*?)\">', unquote(r.text))

        if img_url:
            img_url = img_url[0].replace('\\', '')
            img_url = json.loads(img_url).get('data', None)
            if img_url:
                img_url = img_url.get('path', None)
                return img_url
        return None

    def get_qrdata(self, img_url):
        payload = {
            "img": img_url,
        }
        query_url = "https://cli.im/apis/up/deqrimg"

        r = requests.post(query_url, data=payload)
        if r.json().get('status') == 1:
            info = r.json().get('info')
            if info:
                data = info.get('data')[0]
                return data
        return None

    def qrdecode(self, img):
        url = self.upload(img)
        if url:
            data = self.get_qrdata(img_url=url)
            if not data:
                err = "scan failed"
            else:
                return data
        else:
            err = "upload failed"

        return err
