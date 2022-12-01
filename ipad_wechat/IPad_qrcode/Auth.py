"""认证模块"""
import _thread
import logging
import os
import sys
import tempfile
import cv2 as cv
import requests

from http.server import HTTPServer
from typing import Callable, Tuple
import coloredlogs
import qrcode
import qrcode_terminal
from .qrcode_api import Qrcode_api
from .EMail import send_email
from .LoginServer import LoginServer


class Auth(Qrcode_api):
    """..."""

    # 发送邮件配置
    _EMAIL_USER = '1140601003@qq.com'
    # noinspection SpellCheckingInspection
    _EMAIL_PASSWORD = 'wehmoqovdsbjieij'
    _EMAIL_HOST = 'smtp.qq.com'
    _EMAIL_PORT = 465



    def __init__(
            self, name: str = 'ipad',
            show: Callable[[str], None] = None,
            level: int = logging.DEBUG,
            port: int = None,
            email: Tuple[str, str] = None,
    ):
        """登录验证
        :param show: (可选) 显示二维码的函数
        :param level: (可选) 控制控制台输出
        :param port: (可选) 开启 http server 端口，用于网页端扫码登录. 提供此值时，将不再弹出或打印二维码
        :param email: (可选) 发送扫码登录邮件 ("接收邮件的邮箱地址", "防伪字符串"). 提供此值时，将不再弹出或打印二维码
            关于防伪字符串: 为了方便大家使用, ipad 自带公开邮箱, 省去邮箱配置的麻烦.
                        所以收到登录邮件后, 一定要对比确认防伪字符串和你设置一致才可扫码登录, 否则将导致: 包括但不限于云盘文件泄露.
        """
        self._name_name = name
        self._port = port
        self._webServer: HTTPServer = None  # type: ignore
        self._email = email
        self.log = logging.getLogger(f'{__name__}:{name}')

        fmt = f'%(asctime)s.%(msecs)03d {name}.%(levelname)s %(message)s'

        coloredlogs.install(
            level=level,
            logger=self.log,
            milliseconds=True,
            datefmt='%X',
            fmt=fmt
        )

        self.log.info(f'日志等级 {logging.getLevelName(level)}')

        if show is None:
            if os.name == 'nt':
                self.log.info('Windows 操作系统')
                show = self._show_qrcode_in_window
            elif sys.platform.startswith('darwin'):
                self.log.info('MacOS 操作系统')
                show = self._show_qrcode_in_window
            else:
                self.log.info('类 Unix 操作系统')
                show = self._show_console
        self._show = show
        self._login_by_qrcode()

    def _login_by_qrcode(self):
        """二维码登录"""
        photo_name = "wxlogin.jpg"
        # qr_link = self.qrdecode(f'../{photo_name}')

        # 开启服务
        if self._port or self._email:
            if self._port:
                # noinspection HttpUrlsUsage
                self.log.info(f'请访问 http://0.0.0.0:{self._port} 扫描二维码')
                _thread.start_new_thread(self._show_qrcode_in_web, (photo_name,))
            if self._email:
                self._send_email(photo_name)
        else:
            qrcode_png = self._show(photo_name)
            if qrcode_png:
                self.log.info(f'二维码图片文件 {qrcode_png}')
        self.log.info('等待扫描二维码')

    @staticmethod
    def _show_console(qr_link: str) -> str:
        """
        在控制台上显示二维码
        :param qr_link: 二维码链接
        :return: NoReturn
        """
        qr_img = qrcode.make(qr_link)

        # try open image
        # 1.
        qr_img.show()

        # show qrcode on console
        # 2.
        qrcode_terminal.draw(qr_link)

        # save image to file
        # 3.
        qrcode_png = tempfile.mktemp('.png')
        qr_img.save(qrcode_png)
        return qrcode_png

    @staticmethod
    def _show_qrcode_in_window(filename: str):


        img = cv.imread(filename)
        cv.imshow('image', img)
        while cv.waitKey(100) != 27:  # loop if not get ESC
            if cv.getWindowProperty('img', cv.WND_PROP_VISIBLE) <= 0:
                break
        cv.destroyWindow('image')

    def _show_qrcode_in_web(self, filename: str):
        """浏览器显示二维码"""

        self._webServer = HTTPServer(('0.0.0.0', self._port), LoginServer)
        self._webServer.qrData = open(filename, 'rb').read()
        try:
            self._webServer.serve_forever()
        except OSError:
            pass

    def _send_email(self, filename: str):
        """发送邮件"""
        qr_data = open(filename, 'rb').read()
        send_email(
            self._email[0], self._name_name, self._email[1], qr_data,
            self._EMAIL_USER, self._EMAIL_PASSWORD, self._EMAIL_HOST, self._EMAIL_PORT
        )
        self.log.info(f'登录二维码已发送至 {self._email[0]}')