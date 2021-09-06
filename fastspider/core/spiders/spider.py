# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 周期循环爬虫cycle_spider
"""
from fastspider.item.item import Item

from fastspider.core.base.cycle_base import CycleBase
from fastspider.core.scheduler.scheduler import Scheduler
from fastspider.db.mysql_db import MysqlDB
from fastspider.db.redis_db import RedisDB
from fastspider.utils import tools
from fastspider.utils.logger import log
from fastspider.settings import common
from fastspider.http.request.request import Request


class Spider(CycleBase, Scheduler):

	def __init__(self, redis_key=None, thread_count=None, check_task_interval=5):
		"""
			初始化
		:param cycle_interval: 周期循环执行的时间, 以 1 day天单位, 小时表达为1/24
		:param check_task_interval: 检查爬虫任务的周期时间, 以 1s 秒为单位
		:param _record_table: 爬虫任务执行的批次表
		"""
		super(Spider, self).__init__(
			self, redis_key=redis_key,
			thread_count=thread_count,
			check_task_interval=check_task_interval
		)

		self._mysql_db = MysqlDB()
		self._redis_db = RedisDB()

		self._redis_key = redis_key
		self._thread_count = thread_count
		self._check_task_interval = check_task_interval

		self._is_distributed_task = False

		self._mission_requests = common.REDIS_MISSION_REQUESTS.format(redis_key=redis_key)
		self._mission_spider_status = common.REDIS_SPIDER_STATUS.format(redis_key=redis_key)

	def run(self):
		"""
			启动爬虫
		"""
		try:
			if not self._parsers:
				self._parsers.append(self)

			# 开始启动
			self._start()
			# 判断是否结束
			while True:
				if self.all_thread_is_done():
					self.all_thread_stop()
					break

				# 休息5秒后再次检查爬虫是否还在运行
				tools.sleep_time(5)
		except Exception as e:
			log.error(f"爬虫执行异常, 异常原因: {e}")

	def start_monitor_task(self):
		"""
			开启监控任务, 并记录任务的执行情况
		"""
		if not self._parsers:
			self._parsers.append(self)

		while True:
			# 检查redis中是否还有任务
			todo_requests = self._redis_db.zcount(self._mission_requests)
			if todo_requests:
				log.info("redis 中尚有%s条积压任务，暂时不派发新任务" % todo_requests)
			else:
				# 添加待执行任务
				self.add_task()

			tools.sleep_time(self._check_task_interval)

	def add_task(self):
		"""
			向redis中添加待执行任务
		"""

		for parser in self._parsers:
			requests = parser.start_requests()
			for request in requests:
				if isinstance(request, Request):
					self._request_cache.add_request(request)
					self._is_distributed_task = True

				elif isinstance(request, Item):
					# TODO: 待处理, 可返回Item对象

					pass
				else:
					raise Exception("返回参数错误, 当前只支持yield fastspider.Request对象 和 fastpisder.Item对象")

		self._request_cache.flush()

		if self._is_distributed_task:
			# 开始启动
			self.start_spider()
