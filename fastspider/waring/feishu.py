# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/15

Desc: fastspider的预警功能, 对接飞书的机器人进行信息推送
"""
import base64
import json
import time
import hmac
from hashlib import sha256

import requests

from fastspider.settings.common import FEISHU_WEB_HOOK, FEISHU_SECRET


class FeiShuRobot(object):

	def __init__(self, webhook=None, secret=None):
		self._webhook = webhook or FEISHU_WEB_HOOK
		self._secret = secret or FEISHU_SECRET
		self._now_time = str(round(time.time()))
		self._key = f"{self._now_time}\n{self._secret}".encode("utf-8")

	def sign(self):
		code = hmac.new(self._key, "".encode("utf-8"), digestmod=sha256).digest()
		sign = base64.b64encode(code).decode("utf-8")
		return sign

	def send_msg(self, msg):
		sign = self.sign()

		data = {
			"timestamp": self._now_time,
			"sign": sign,
			"msg_type": "text",
			"content": {
				"text": msg
			}
		}
		headers = {
			"Content-Type": "application/json"
		}
		req = requests.post(self._webhook, headers=headers, data=json.dumps(data))

		return req
