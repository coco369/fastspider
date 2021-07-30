# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/30

Desc: fastspider核心代码, 封装requests包
"""
import requests
import urllib3
from requests.adapters import HTTPAdapter

from fastspider.http import user_agent
from fastspider.http.response.response import Response
from fastspider.settings import common
from fastspider.utils import tools

# 忽略警告信息
urllib3.disable_warnings()


class Request(object):
	user_agent_pool = user_agent
	proxies_pool = None
	session = None

	# 组装非必须传入的参数
	__request_attrs__ = ["headers", "data", "params", "cookies", "json", "timeout", "proxies", "verify"]
	# 组装默认传递的参数
	__default_requests_attrs__ = {
		"url": "",
		"retry_time": 0,
		"parser_name": None,
		"callback": None,
		"use_session": False,
		"download_middleware": None,
		"web_render": False,
		"web_render_time": 0,
		"request_sync": False
	}

	def __init__(self, url="", retry_time=0, parser_name=None, callback=None, use_session=False,
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

	@property
	def _make_session(self):
		"""
		:return: 生成request.Session对象
		"""
		self.__class__.session = requests.Session()
		# pool_connections – 缓存的 urllib3 连接池个数  pool_maxsize – 连接池中保存的最大连接数
		adapter = HTTPAdapter(pool_connections=500, pool_maxsize=500)
		# mount 挂载前缀, 只要URL是以http前缀开头的会话, 都会被传入到适配器adapter中
		self.__class__.session.mount("http", adapter)
		return self.__class__.session

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
		else:
			if "user-agent" in headers:
				headers.pop("user-agent")
			headers.setdefault(
				"User-Agent", self.__class__.user_agent_pool.get_ua(common.USER_AGENT_TYPE)
			)
			self.request_kwargs.update(headers=headers)

		# 代理proxies
		proxies = self.request_kwargs.get("proxies", False)
		if proxies and common.PROXY_ENABLE:
			# 代理的获取方式, 依次获取隧道代理、IP地址代理.....
			abuyun_proxies = tools.get_tunnel_proxy()
			if abuyun_proxies:
				self.request_kwargs.update(proxies=abuyun_proxies)

		# TODO: 如果没有隧道代理, 则可以使用IP代理

		# 浏览器渲染
		# TODO: 暂不支持浏览器渲染

		# 设置session
		use_session = self.use_session if self.use_session else common.USE_SESSION
		if use_session:
			response = self._make_session.request(method=method, url=self.url, **self.request_kwargs)
		else:
			response = requests.request(method=method, url=self.url, **self.request_kwargs)

		# TODO: 封装response
		response = Response(response)
		return response