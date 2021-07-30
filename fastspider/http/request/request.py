# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/30

Desc: fastspider核心代码, 封装requests包
"""
import requests
import urllib3

from fastspider.http import user_agent
from fastspider.settings import common

# 忽略警告信息
urllib3.disable_warnings()


class Request(object):
	user_agent_pool = user_agent
	proxies_pool = None

	# 组装非必须传入的参数
	__request_attrs__ = ["headers", "data", "params", "cookies", "json", "timeout", "proxies", "verify"]
	# 组装默认传递的参数
	__default_requests_attrs__ = {
		"url": "",
		"retry_time": 0,
		"parser_name": None,
		"callback": None,
		"use_session": None,
		"download_middleware": None,
		"web_render": False,
		"web_render_time": 0,
		"request_sync": False
	}

	def __init__(self, url="", retry_time=0, parser_name=None, callback=None, use_session=None,
	             download_middleware=None, web_render=False, web_render_time=0, request_sync=False, **kwargs):
		self.url = url
		self.retry_time = retry_time
		self.parser_name = parser_name
		self.callback = callback
		self.request_sync = request_sync
		self.use_session = use_session
		self.download_middleware = download_middleware
		self.web_render = web_render
		self.web_render_time = web_render_time

		self.request_kwargs = {}
		for key, value in kwargs.items():
			if key in self.__class__.__request_attrs__:
				self.request_kwargs[key] = value

			self.__dict__[key] = value

	def get_response(self):

		# 设置请求超时时间
		self.request_kwargs.setdefault(
			"timeout", common.REQUEST_TIMEOUT
		)

		# 设置ssl验证
		self.request_kwargs.setdefault(
			"verify", False
		)

		# 获取请求方式method
		method = "GET"
		if not self.__dict__.get("method"):
			if "data" in self.request_kwargs:
				method = "POST"

		# 设置ua
		headers = self.request_kwargs.get("headers", {})
		if "user-agent" not in headers and "User-Agent" not in headers:
			headers["User-Agent"] = self.__class__.user_agent_pool.get_ua(common.USER_AGENT_TYPE)
			self.request_kwargs.update(headers=headers)

		# 设置session
		use_session = self.use_session if self.use_session else common.USE_SESSION

		if use_session:
			pass
		else:
			response = requests.request(method=method, url=self.url, **self.request_kwargs)
			# TODO: 封装response

		return response
