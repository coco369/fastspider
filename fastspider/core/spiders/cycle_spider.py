# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 周期循环爬虫cycle_spider
"""
from fastspider.core.base.cycle_base import CycleBase
from fastspider.core.scheduler.scheduler import Scheduler
from fastspider.db.mysql_db import MysqlDB
from fastspider.db.redis_db import RedisDB


class CycleSpider(CycleBase, Scheduler):

	def __init__(self):
		super(CycleSpider, self).__init__()

		self._mysql_db = MysqlDB()
		self._redis_db = RedisDB()

	def run(self):
		# 启动
		self._start()
