# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/26

Desc: fastspider核心代码, redis
"""
import time

import redis
from fastspider.utils.logger import log

from fastspider.settings import common


class RedisDB(object):

	def __init__(self, url=None, ip=None, port=None, password=None, db=1, max_connections=30, **kwargs):
		self._url = url or common.REDISDB_URL
		self._ip = ip or common.REDISDB_IP
		self._port = port or common.REDISDB_PORT
		self._password = port or common.REDISDB_USER_PASS
		self._db = port or common.REDISDB_DB
		self._max_connections = max_connections
		self._kwargs = kwargs

		self._client = None
		self._redis = None

		self.connect()

	@property
	def _client(self):
		try:
			if not self._redis.ping():
				raise ConnectionError("链接redis失败, 请检测redis配置")
		except Exception as e:
			self._reconnect()

		return self._redis

	@_client.setter
	def _client(self, val):
		self._redis = val

	def connect(self):
		"""
			链接redis
		"""
		if not self._url:
			if not self._ip or not self._port:
				raise Exception("请在配置 REDISDB_IP, REDISDB_PORT")
			if self._ip and self._port:
				self._client = redis.StrictRedis(host=self._ip, port=self._port, db=self._db, password=self._password,
				                                 decode_responses=True, max_connections=self._max_connections,
				                                 **self._kwargs)
		else:
			self._client = redis.StrictRedis.from_url(url=self._url, decode_responses=True)

		return self._client

	def _reconnect(self):
		"""
			重新链接redis
		"""
		retry_count = 0
		while True:
			try:
				retry_count += 1
				log.error(f"redis 连接断开, 重新连接 {retry_count}")
				if self.connect():
					log.info(f"redis 连接成功")
					return True
			except (ConnectionError, TimeoutError) as e:
				log.error(f"连接失败 e: {e}")

			time.sleep(2)

	def set(self, key, value, **kwargs):
		"""
			redis-string类型
		"""
		return self._client.set(key, value, **kwargs)

	def set_expire(self, key, seconds):
		"""
			设置过期时间
		"""
		return self._client.expire(key, seconds)
