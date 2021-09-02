# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/30

Desc: fastspider核心代码, 封装requests包
"""
import requests
import urllib3
from requests.adapters import HTTPAdapter

from fastspider.http import user_agent
from fastspider.http.fastselenium.fastwebdriver import WebDriverPool
from fastspider.http.response.response import Response
from fastspider.settings import common
from fastspider.utils import tools

# 忽略警告信息
from fastspider.utils.logger import log

urllib3.disable_warnings()

urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'


class Request(object):
	user_agent_pool = user_agent
	proxies_pool = None
	webdriver_pool = None
	session = None

	# 组装非必须传入的参数
	__request_attrs__ = ["headers", "data", "params", "cookies", "json", "timeout", "proxies", "verify", "meta"]
	# 组装默认传递的参数
	__default_requests_attrs__ = {
		"url": "",
		"method": "",
		"retry_time": 0,
		"priority": 300,
		"parser_name": None,
		"callback": None,
		"filter_request": False,
		"use_session": False,
		"download_middleware": None,
		"web_render": False,
		"web_render_time": 0,
		"web_render_scroll": False,
		"request_sync": False
	}

	def __init__(self, url="", method="", retry_time=0, priority=300, parser_name=None, callback=None,
	             filter_request=False, use_session=False, download_middleware=None, web_render=False, web_render_time=0,
	             web_render_scroll=False, request_sync=False, **kwargs):
		self.url = url
		self.method = method
		self.retry_time = retry_time
		self.priority = priority
		self.parser_name = parser_name
		self.callback = callback
		self.filter_request = filter_request
		self.request_sync = request_sync
		self.use_session = use_session
		self.download_middleware = download_middleware
		self.web_render = web_render
		self.web_render_time = web_render_time
		self.web_render_scroll = web_render_scroll

		self.request_kwargs = {}
		for key, value in kwargs.items():
			if key in self.__class__.__request_attrs__:
				self.request_kwargs[key] = value

			self.__dict__[key] = value

	def __lt__(self, other):
		"""
			把Request对象插入到优先级对象中, 会判断每一个Reqeest对象的优先级。
			需要重定义__lt__方法, 使类能进行大小比较, 然后将具有优先级的Request对象插入到优先级队列中
		:param other:
		:return:
		"""
		return self.priority < other.priority

	@property
	def to_dict(self):
		request_dict = {}

		for key, value in self.__dict__.items():
			request_dict[key] = value

		return request_dict

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

	@property
	def _webdriver_pool(self):
		if not self.__class__.webdriver_pool:
			self.__class__.webdriver_pool = WebDriverPool(**common.WEBDRIVER)
		return self.__class__.webdriver_pool

	def get_response(self):
		# 获取meta参数
		meta = self.request_kwargs.pop("meta") if self.request_kwargs.get("meta") else ""

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
		if self.__dict__.get("method"):
			method = self.__dict__.get("method")
		elif "data" in self.request_kwargs:
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
		# if proxies and common.PROXY_ENABLE:
		# 	# 代理的获取方式, 依次获取隧道代理、IP地址代理.....
		# 	abuyun_proxies = tools.get_tunnel_proxy()
		# 	if abuyun_proxies:
		# 		self.request_kwargs.update(proxies=abuyun_proxies)
		self.request_kwargs.update(proxies=proxies)

		# TODO: 如果没有隧道代理, 则可以使用IP代理

		# 浏览器渲染
		use_session = self.use_session if self.use_session else common.USE_SESSION

		if self.web_render:
			try:
				driver = self._webdriver_pool.get()

				driver.get(self.url)

				if self.web_render_scroll:
					js = "return action=document.body.scrollHeight"
					height = driver.execute_script(js)
					for i in range(0, height, 150):
						if self.web_render_time:
							tools.sleep_time(self.web_render_time)
						driver.execute_script(f"window.scrollTo(0, {i})")

				if self.web_render_time:
					tools.sleep_time(self.web_render_time)

				html = driver.page_source
				response = Response.from_dict({
					"status_code": 200,
					"_content": html,
					"url": self.url,
					"cookies": driver.cookies,
					"meta": meta
				})
				response.driver = driver
			except Exception as e:
				print(e)
				raise e
			finally:
				self._webdriver_pool.remove(driver)

		# 设置session
		elif use_session:
			response = self._make_session.request(method=method, url=self.url, **self.request_kwargs)
			response.__dict__.setdefault("meta", meta)
			response = Response(response)
		else:
			response = requests.request(method=method, url=self.url, **self.request_kwargs)
			response.__dict__.setdefault("meta", meta)
			response = Response(response)

		log.debug(
			"""
			------------------%s.%s request for-----------------------------
				url = %s
				method = %s
				request_kwargs = %s
			""" % (
				self.parser_name,
				self.callback,
				self.url,
				method,
				self.request_kwargs,
			)
		)
		return response
