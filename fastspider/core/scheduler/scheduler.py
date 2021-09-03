# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 定时器scheduler
"""
import threading

from fastspider.cache.request_cache import RequestCache
from fastspider.core.controller.collector import Collector
from fastspider.core.controller.spider_controller import BaseController
from fastspider.settings import common


class Scheduler(threading.Thread):
	__common_settings__ = {}

	def __init__(self, redis_key=None, thread_count=None):
		"""
			定时执行爬虫任务的调度器
		"""
		self.cycle_interval = 0
		self._thread_count = thread_count or common.SPIDER_THREAD_COUNT
		self._parsers = []
		self._parsers_controller = []

		super(Scheduler, self).__init__()

		# 解析自定义的字典__common_settings__ 变量中的参数
		for k, v in self.__class__.__common_settings__.items():
			setattr(common, k, v)

		self._redis_key = redis_key or common.REDIS_KEY
		self._request_cache = RequestCache(self._redis_key)

		self._base_controller = BaseController

	def _start(self):
		# 启动相关线程
		# 1. 总请求任务/请求失败任务/请求删除任务 与 Redis的同步 线程
		self._request_cache.start()
		# 2. 获取Redis中任务请求request的 线程
		self._collector = Collector(self._redis_key)

		for i in range(self._thread_count):
			parser_controller = self._base_controller(

			)
			for parser in self._parsers:
				parser_controller.add_parser(parser)
			# 启动线程
			parser_controller.start()

			self._parsers_controller.append(parser_controller)

		# 3. 下发任务

	def run(self):

		self._start()

		while True:
			pass
