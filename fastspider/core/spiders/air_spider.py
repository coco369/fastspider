# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/29

Desc: fastspider核心代码, 轻量级爬虫air_spider
"""
from threading import Thread

from fastspider.core.base.air_base import AirBase
from fastspider.core.controller.spider_controller import AirSpiderController
from fastspider.db.memory_db import MemoryDB
from fastspider.http.request.request import Request
from fastspider.settings import common


class AirSpider(AirBase, Thread):
	# 定义私有变量
	__common_settings__ = {}

	def __init__(self, thread_count=None):
		"""
			初始化配置
			用户可自定义settings配置, 配置变量为__common_settings__, 类型为dict
		"""
		super(AirSpider, self).__init__()

		self._memory_db = MemoryDB()

		self._parser_controller = []

		for k, v in self.__class__.__common_settings__.items():
			setattr(common, k, v)
		self._thread_count = common.SPIDER_THREAD_COUNT if not thread_count else thread_count

	def add_task(self):
		"""
			将start_response中的任务Request对象存储到内存队列中
		:return: None
		"""
		for req in self.start_requests():
			if not isinstance(req, Request):
				raise Exception("返回参数错误, 当前只支持yield fastspider.Request对象")

			self._memory_db.put(req)

	def all_thread_task_done(self):
		"""
			判断内存队列中的任务是否执行完毕
		:return: True: 已执行完所有任务。 False: 还有处于待执行中的任务
		"""
		for i in range(3):
			for parser_controller in self._parser_controller:
				if parser_controller.has_task():
					return False

			# 检测任务队列是否为空
			if not self._memory_db.is_empty():
				return False

		return True

	def run(self):
		"""
			启动线程
		"""
		# 先将任务监听的控制方法启动, 再通过add_task将需要爬取的request对象写入, 通过while检测任务执行的情况, 任务执行完, 则暂定任务_thread_stop设置为True
		for i in range(self._thread_count):
			spider_controller = AirSpiderController(self._memory_db)
			spider_controller.add_parser(self)
			spider_controller.start()

			self._parser_controller.append(spider_controller)

		# 将任务放在内存中
		self.add_task()

		# 死循环, 一直执行任务, 判断任务task是否执行完成, 如果任务执行完毕, 则关闭各种链接，如mysql, 浏览器对象
		while True:
			if self.all_thread_task_done():

				for parser_controller in self._parser_controller:
					parser_controller.stop()

				print("无任务, 爬虫执行完毕")

				break
