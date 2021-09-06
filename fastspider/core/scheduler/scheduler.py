# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 定时器scheduler
"""
import threading

from fastspider.http.request.request import Request

from fastspider.cache.request_cache import RequestCache
from fastspider.core.controller.collector import Collector
from fastspider.core.controller.spider_controller import CycleSpiderController
from fastspider.settings import common
from fastspider.utils.logger import log
from fastspider.utils import tools


class Scheduler(threading.Thread):
	__common_settings__ = {}

	def __init__(self, redis_key=None, thread_count=None, check_task_interval=None):
		"""
			定时执行爬虫任务的调度器
		"""
		self._thread_count = thread_count or common.SPIDER_THREAD_COUNT
		self._parsers = []
		self._parsers_controller = []

		super(Scheduler, self).__init__()

		# 解析自定义的字典__common_settings__ 变量中的参数
		for k, v in self.__class__.__common_settings__.items():
			setattr(common, k, v)

		self._redis_key = redis_key or common.REDIS_KEY
		self._request_cache = RequestCache(self._redis_key)
		self._collector = Collector(redis_key)

		self._base_controller = CycleSpiderController

	def _start(self):
		# 启动相关线程
		# 1. 总请求任务/请求失败任务/请求删除任务 与 Redis的同步 线程
		self._request_cache.start()
		# 2. 获取Redis中任务请求request的 线程
		self._collector.start()

		for i in range(self._thread_count):
			parser_controller = self._base_controller(
				collector=self._collector
			)
			for parser in self._parsers:
				parser_controller.add_parser(parser)
			# 启动线程
			parser_controller.start()

			self._parsers_controller.append(parser_controller)

		# 3. 下发任务
		# TODO: 可能多进程之间会添加重复的任务, 下发任务处将使用redis 锁进行处理。暂时先考虑启动单进程处理任务, 不考虑锁的问题。
		self._add_task()

	def _add_task(self):
		"""
			添加待执行任务
		"""
		todo_requests_count = self._collector.get_requests_count()
		if todo_requests_count:
			log.info(f"检测有待执行任务 {todo_requests_count} 条, 不重新下发新任务, 将接着上次异常终止处继续执行抓取任务")
		else:
			for parser in self._parsers:
				request = parser.start_requests()
				if request and not isinstance(request, Request):
					raise Exception("返回参数错误, 当前只支持yield fastspider.Request对象")
				request.parser_name = request.parser_name or parser.name

		# 刷新一波待执行任务
		self._request_cache.flush()

	def run(self):

		self._start()

		while True:
			pass

	def all_thread_is_done(self):
		"""
			检测所有的线程是否都执行完毕, 如果执行完毕,则返回True。 如果其中任何一个线程没有执行完毕, 则返回Fasle
		"""
		for i in range(5):
			# 检查 _collector 状态
			if self._collector.is_collector_task() or self._collector.get_requests_count() > 0:
				return False
			# 检查每个线程中任务的执行状态,
			for parser in self._parsers_controller:
				if parser.has_task():
					return False

			# 检查 _request_cache 状态
			if self._request_cache.get_request_count() > 0 or self._request_cache.is_adding_request_to_db():
				return False

			tools.sleep_time(1)
		return True

	def all_thread_stop(self):
		"""
			手动暂停所有的线程
		"""
		self._request_cache.stop()

		self._collector.stop()

		for parser in self._parsers_controller:
			parser.stop()

	def start_spider(self):
		"""
			启动爬虫
		"""

		pass
