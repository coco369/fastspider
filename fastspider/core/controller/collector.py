# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, 合理调度redis中的requests队列中的任务
"""

import threading
import time

from fastspider.db.redis_db import RedisDB
from fastspider.settings import common
from fastspider.utils import tools


class Collector(threading.Thread):

	def __init__(self, redis_key=None):
		super(Collector, self).__init__()
		self._thread_stop = False

		self._redis_key = redis_key or common.REDIS_KEY
		self._interval = common.COLLECTOR_SLEEP_TIME
		self._get_task_count = common.COLLECTOR_TASK_COUNT

		self._redis_db = RedisDB()
		self._mission_request_name = common.REDIS_MISSION_REQUESTS.format(redis_key=redis_key)
		self._mission_spider_status = common.REDIS_SPIDER_STATUS.format(redis_key=redis_key)

	def _put_data(self):
		pass

	def run(self):
		while not self._thread_stop:
			self._put_data()

			tools.sleep_time(self._interval)
