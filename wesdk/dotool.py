#coding:utf-8
from vncdotool import api
class DoTool:
    QR=1
    LOGIN=1
    CHAT=1
    def __init__(self, ip="127.0.0.1", port=5900):
        self.client = api.connect(f'{ip}::{port}')
    def state(self):
        pass
    def click_login(self):
        self.client.mouseMove(640, 425)
        self.client.mouseDown(1)
        self.client.mouseUp(1)
        self.client.mouseDown(1)
        self.client.mouseUp(1)
    def switch_account(self):
        self.client.mouseMove(640, 425)
        self.client.mouseDown(1)
        self.client.mouseUp(1)
        self.client.mouseDown(1)
        self.client.mouseUp(1)
    def qrcode(self, filename='./.qr.png'):
        self.client.captureRegion(filename, 541, 224, 200, 200)