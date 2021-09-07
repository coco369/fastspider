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
			redis_key=redis_key,
			thread_count=thread_count,
			check_task_interval=check_task_interval
		)

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
				tools.sleep_time(1)
		except Exception as e:
			log.error(f"爬虫执行异常, 异常原因: {e}")
