# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 请求request缓存
"""

import collections
import threading

from fastspider.db.redis_db import RedisDB
from fastspider.utils import tools
from fastspider.settings import common
from fastspider.utils.logger import log


class RequestCache(threading.Thread):
	MAX_REQUESTS_COUNT = 1000

	def __init__(self, redis_key):
		super(RequestCache, self).__init__()

		self._thread_stop = False
		self._add_request_to_db_status = False

		self._requests_deque = collections.deque()
		self._del_requests_deque = collections.deque()

		self._redis_db = RedisDB()
		self._mission_request_name = common.REDIS_MISSION_REQUESTS.format(redis_key=redis_key)
		self._mission_fail_request_name = common.REDIS_MISSION_FAIL_REQUESTS.format(redis_key=redis_key)

	def run(self):
		while not self._thread_stop:
			try:
				self.__add_request_to_db()
			except Exception as e:
				log.error(f"向redis中添加待执行任务失败, 失败原因: {e}")
			tools.sleep_time(1)

	def flush(self):
		"""
			主动刷新任务
		"""
		try:
			self.__add_request_to_db()
		except Exception as e:
			log.error(f"向redis中添加待执行任务失败, 失败原因: {e}")

	def stop(self):
		self._thread_stop = True

	def add_request(self, request):
		"""
			向请求request队列中加入请求
		:param request: 请求
		"""
		self._requests_deque.append(request)

		if self.get_request_count() > self.MAX_REQUESTS_COUNT:
			self.flush()

	def get_request_count(self):
		"""
			获取待执行队列中的任务数
		"""
		return len(self._requests_deque)

	def add_del_request(self, request):
		"""
			向队列中添加需要移除的请求request
		:param request: 请求
		"""
		self._del_requests_deque.append(request)

	def add_fail_request(self, request):
		"""
			向队列中添加失败的请求
		:param request:
		:return:
		"""
		try:
			self._redis_db.zadd(self._mission_fail_request_name, request.to_dict, request.priority)
		except Exception as e:
			log.error(f"添加失败请求到redis表{self._mission_fail_request_name}中失败, 错误原因: {e}")

	def __add_request_to_db(self):
		request_list = []
		priority_list = []
		callbacks = []
		while self._requests_deque:
			request = self._requests_deque.popleft()
			self._add_request_to_db_status = True

			if callable(request):
				callbacks.append(request)

			# 请求优先等级
			priority = request.priority
			# TODO: 请求去重, 暂时不考虑
			filter_request = request.filter_request

			request_list.append(str(request.to_dict))
			priority_list.append(priority)

			if len(request_list) > self.__class__.MAX_REQUESTS_COUNT:
				self._redis_db.zadd(self._mission_request_name, request_list, priority_list)
				request_list = []
				priority_list = []

		# 数量达不到 MAX_REQUESTS_COUNT, 则单独处理
		if request_list:
			self._redis_db.zadd(self._mission_request_name, request_list, priority_list)

		# TODO: 不太明白
		# for callback in callbacks:
		# 	callback()

		# 将完成的任务从redis中移除
		if self._del_requests_deque:
			del_requests_list = []
			while self._del_requests_deque:
				del_requests_list.append(self._del_requests_deque.popleft())

			if del_requests_list:
				self._redis_db.zrem(self._mission_request_name, del_requests_list)

		self._add_request_to_db_status = False

	def is_adding_request_to_db(self):
		"""
			获取线程是否还在向db中添加数据
		"""
		return self._add_request_to_db_status
