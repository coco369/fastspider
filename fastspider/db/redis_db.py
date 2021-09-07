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

	def __repr__(self):
		if self._url:
			return f"<RedisDB url:{self._url}>"

		return f"<RedisDB host: {self._ip} port: {self._ip} password: {self._password}>"

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

	def zadd(self, table_name, requests, priority=0):
		"""
			使用有序set集合进行数据的存储
		:param table_name: 集合名称
		:param requests:  请求支持list 或者单个值
		:param priority:  优先等级，支持list 或者 单个值, 可不传, 不传的情况下默认请求的优先级为0。或者也可以传入列表, 根据列表中的值来定义请求的执行优先级, 值越低, 越优先。
		:return:
		"""
		if isinstance(requests, list):
			if not isinstance(priority, list):
				priority = [priority] * len(requests)
			else:
				assert len(priority) == len(requests), "请求队列和优先级的值需要一一对应"

			# 批量操作
			pipeline = self._client.pipeline()
			pipeline.multi()
			for key, value in zip(requests, priority):
				pipeline.execute_command("ZADD", table_name, value, key)
				log.info(f"RedisDB 中插入任务成功, 数据格式为: {key}")
			return pipeline.execute()
		else:
			log.info(f"RedisDB 中插入任务成功, 数据格式为: {requests}")
			return self._client.execute_command("ZADD", table_name, priority, requests)

	def zrem(self, table_name, values):
		"""
			移除有序set集合中的元素, 如果元素不存在则忽略
		:param table_name: 集合名称
		:param values: 移除的元素, 支持列表 或者 单个值
		:return:
		"""
		if isinstance(values, list):
			self._client.zrem(table_name, *values)
		else:
			self._client.zrem(table_name, values)

	def zcount(self, table_name, priority_min=None, priority_max=None):
		"""
			计算有序set集合中的元素的个数
		:param table_name: 集合名称
		:param priority_min: 优先级范围的最小值
		:param priority_max: 优先级范围的最大值
		:return:
		"""
		if priority_min != None and priority_max != None:
			return self._client.zcount(table_name, priority_min, priority_max)
		else:
			return self._client.zcard(table_name)

	def zrangebyscore_set_score(
			self, table, priority_min, priority_max, score, count=None
	):
		"""
		@summary: 返回指定分数区间的数据 闭区间， 同时修改分数
		---------
		@param table: 集合名称
		@param priority_min: 最小分数
		@param priority_max: 最大分数
		@param score: 分数值
		@param count: 获取的数量，为空则表示分数区间内的全部数据
		---------
		@result:
		"""

		# 使用lua脚本， 保证操作的原子性
		lua = """
			-- local key = KEYS[1]
			local min_score = ARGV[1]
			local max_score = ARGV[2]
			local set_score = ARGV[3]
			local count = ARGV[4]
			
			-- 取值
			local datas = nil
			if count then
				datas = redis.call('zrangebyscore', KEYS[1], min_score, max_score, 'withscores','limit', 0, count)
			else
				datas = redis.call('zrangebyscore', KEYS[1], min_score, max_score, 'withscores')
			end
			
			local real_datas = {} -- 数据
			--修改优先级
			for i=1, #datas, 2 do
				local data = datas[i]
				local score = datas[i+1]
				
				table.insert(real_datas, data) -- 添加数据
				
				redis.call('zincrby', KEYS[1], set_score - score, datas[i])
			end
			
			return real_datas
		
		"""
		cmd = self._client.register_script(lua)
		if count:
			res = cmd(keys=[table], args=[priority_min, priority_max, score, count])
		else:
			res = cmd(keys=[table], args=[priority_min, priority_max, score])

		return res

	def zremrangebyscore(self, table_name, priority_min, priority_max):
		"""
			用于移除有序set集中，指定分数（score）区间内的所有成员
		:param table_name: 集合名称
		:param priority_min: 优先级最小值
		:param priority_max: 优先级最大值
		"""
		return self._client.zremrangebyscore(table_name, priority_min, priority_max)
