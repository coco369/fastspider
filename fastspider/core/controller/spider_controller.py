# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, 控制器
"""
import time
from collections import Iterable
import random
from threading import Thread

from fastspider.http.request.request import Request
from fastspider.item.item import Item
from fastspider.settings import common
from fastspider.utils.logger import log


class BaseController(Thread):
	# 统计任务执行成功的个数 和 任务执行失败的个数, 用于后期统计任务执行成功率, 成功率太低, 则发送报警信息
	# 成功率计算公司  失败任务总数 / 总任务数 > 0.5 则发送报警信息
	_success_task_num = 0
	_fail_task_num = 0

	has_task_flag = False

	def __init__(self, collector):
		super(BaseController, self).__init__()

		self._thread_stop = False
		self._parser = []

		self._collector = collector

	def has_task(self):
		return self.has_task_flag

	def stop(self):
		# 将线程启动的标识 设置为True
		self._thread_stop = True

	def add_parser(self, parser):
		self._parser.append(parser)


class LightSpiderController(BaseController):

	def __init__(self, memory_db, item_cache):
		super(LightSpiderController, self).__init__()

		self._memory_db = memory_db
		self._item_cache = item_cache

	def run(self):

		while not self._thread_stop:
			try:
				request = self._memory_db.get_nowait()
				if not request:
					self.has_task_flag = False
				else:
					self.has_task_flag = True
					self.deal_requests([request])
			except Exception as e:
				log.error(f"轻量级爬虫lightspider执行失败, 失败原因: {e}")

	def deal_requests(self, requests):
		"""
			处理请求
		:param request: 请求
		:return:
		"""
		response = None
		for request in requests:
			for parser in self._parser:
				# 判断当前请求是否是请求对应的爬虫触发的。避免同时多个爬虫一起执行时, 请求request和对应的爬虫匹配错误
				if request.parser_name == parser.name:
					try:
						# 解析request
						# if request.download_middleware:
						# 	pass
						# else:
						response = request.get_response()
						# 判断是否有回调函数
						if request.callback:
							# 检查回调函数是否可用
							# callback_parser = (
							# 	request.callback if callable(request.callback)
							# 	else tools.check_class_method(parser, request.callback)
							# )
							callback_parser = (request.callback)
							results = callback_parser(request, response)
						else:
							results = parser.parser(request, response)

						if results and not isinstance(results, Iterable):
							raise Exception(f"{parser.name}.{request.callback}必须可迭代的返回值")

						for result in results or []:
							if isinstance(result, Request):
								result.parser_name = result.parser_name or parser.name
								# 如果是同步的callback, 将解析request对象添加到requests中
								if result.request_sync:
									requests.append(result)
								else:
									# 异步, 将任务添加到 任务队列中
									self._memory_db.put(result)
							elif isinstance(result, Item):
								# 存入item缓存中
								self._item_cache.put(result)

					except Exception as e:
						# TODO: 记录任务失败的信息
						print(e)
						self._memory_db.put(request)
					# if request.retry_time:
					# 	request.retry_time -= 1
					# 	self._memory_db.put(request)
					# finally:
					# 	print("释放相关的链接, 如数据库、浏览器的链接")

					break
		# 休眠
		if common.SPIDER_SLEEP_TIME:
			if isinstance(common.SPIDER_SLEEP_TIME, (tuple, list)) and len(common.SPIDER_SLEEP_TIME) == 2:
				sleep_times = random.randint(common.SPIDER_SLEEP_TIME[0], common.SPIDER_SLEEP_TIME[1])
				time.sleep(sleep_times)
			else:
				time.sleep(common.SPIDER_SLEEP_TIME)


class CycleSpiderController(BaseController):

	def __init__(self, collector):
		super(CycleSpiderController, self).__init__()
		self._thread_stop = False
		self._parser = []

		self._collector = collector

	def run(self):
		while not self._thread_stop:
			requests = self._collector.get_requests(common.SPIDER_TASK_COUNT)
			if not requests:
				self.has_task_flag = False
			else:
				self.has_task_flag = True
				self.deal_requests(requests)

	def deal_requests(self, requests):
		for request in requests:
			response = None

			request = request["request_obj"]
			request_redis = request["request_redis"]

			for parser in self._parser:
				try:
					if parser.name == request.parser_name:

						# TODO: download_middleware处理
						response = request.get_response()
						# 判断是否有回调函数
						if request.callback:
							# 检查回调函数是否可用
							callback_parser = (request.callback)
							results = callback_parser(request, response)
						else:
							results = parser.parser(request, response)

						if results and not isinstance(results, Iterable):
							raise Exception(f"{parser.name}.{request.callback}必须可迭代的返回值")

						for result in results or []:
							if isinstance(result, Request):
								result.parser_name = result.parser_name or parser.name
								# 如果是同步的callback, 将解析request对象添加到requests中
								if result.request_sync:
									requests.append(result)
								else:
									# 异步, 将任务添加到 任务队列中
									self._memory_db.put(result)
							elif isinstance(result, Item):
								# 存入item缓存中
								self._item_cache.put(result)
				except Exception as e:
					log.exception(e)
