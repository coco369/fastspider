# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, redis缓存
"""
from threading import Thread

from fastspider.utils.logger import log

from fastspider.db.redis_db import RedisDB
from fastspider.utils import tools


class RedisCache(Thread):

	def __init__(self, parser_name):
		super(RedisCache, self).__init__()

		self._thread_stop = False
		self._redis = RedisDB()
		self._parser_name = parser_name

	def heartbeat(self, parser_name):
		"""
			心跳检测
		"""
		log.debug("---%s 心跳检测---" % parser_name)
		self._redis.set(parser_name, 1)
		self._redis.set_expire(parser_name, 1)

	def run(self):
		while not self._thread_stop:
			for parser_name in self._parser_name:
				self.heartbeat(parser_name)
			tools.sleep_time(1)

	def stop(self):
		self._thread_stop = True
