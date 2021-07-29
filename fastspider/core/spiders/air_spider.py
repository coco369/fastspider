# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/29

Desc: fastspider核心代码, 轻量级爬虫air_spider
"""
from threading import Thread

from fastspider.core.base.air_base import AirBase
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
		self._memory_db = MemoryDB()

		for k, v in self.__class__.__common_settings__.items():
			setattr(common, k, v)
		self._thread_count = common.SPIDER_THREAD_COUNT if not thread_count else thread_count

	def add_task(self):
		"""
			将start_response中的任务Request对象存储到内存队列中
		:return: None
		"""
		for req in self.start_request():
			if not isinstance(req, Request):
				raise Exception("返回参数错误, 当前只支持yield fastspider.Request对象")

			self._memory_db.put(req)

	def run(self):
		"""
			启动线程
		"""
		for i in range(self._thread_count):

			pass

		# 将任务放在内存中
		self.add_task()
