# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, 合理调度redis中的requests队列中的任务
"""
import collections
import threading

from fastspider.http.request.request import Request

from fastspider.db.redis_db import RedisDB
from fastspider.settings import common
from fastspider.utils import tools
from fastspider.utils.logger import log


class Collector(threading.Thread):

	def __init__(self, redis_key=None):
		super(Collector, self).__init__()
		self._thread_stop = False

		self._redis_key = redis_key or common.REDIS_KEY
		self._interval = common.COLLECTOR_SLEEP_TIME
		self._get_task_count = common.COLLECTOR_TASK_COUNT
		# TODO: 后期修改为分布式后, _spider_mark可修改成不同主机的 ”IP-当前时间“
		self._spider_mark = f"spiders-{tools.get_current_timestamp()}"
		# 第一次获取任务
		self._first_get_task = True

		self._is_collector_task = False

		# 待执行请求队列
		self._todo_requests = collections.deque()

		self._redis_db = RedisDB()
		self._mission_request_name = common.REDIS_MISSION_REQUESTS.format(redis_key=redis_key)
		self._mission_spider_status = common.REDIS_SPIDER_STATUS.format(redis_key=redis_key)

	def _put_data(self):
		"""
			向待执行任务队列_todo_requests中插入任务
			# TODO
		:return:
		"""
		current_timestamp = tools.get_current_timestamp()

		spider_count = self._redis_db.zcount(self._mission_spider_status,
		                                     priority_min=current_timestamp - (self._interval + 10),
		                                     priority_max=current_timestamp)

		request_count = self._get_task_count
		if spider_count:
			all_spider_count = self._redis_db.zcount(self._mission_spider_status)
			if all_spider_count % spider_count == 0:
				request_count = all_spider_count // spider_count
			else:
				request_count = all_spider_count // spider_count + 1

		request_count = (
			request_count
			if request_count <= self._get_task_count
			else self._get_task_count
		)

		# 第一次执行
		if self._first_get_task and spider_count <= 1:
			datas = self._redis_db.zrangebyscore_set_score(
				self._mission_request_name,
				priority_min=current_timestamp,
				priority_max=current_timestamp + common.REQUEST_LOST_TIMEOUT,
				score=300,
				count=None,
			)
			self._first_get_task = False
			lose_count = len(datas)
			if lose_count:
				log.info("重置丢失任务完毕，共{}条".format(len(datas)))

		# 取任务，只取当前时间戳以内的任务，同时将任务分数修改为 current_timestamp + setting.REQUEST_LOST_TIMEOUT
		requests_list = self._redis_db.zrangebyscore_set_score(
			self._mission_request_name,
			priority_min="-inf",
			priority_max=current_timestamp,
			score=current_timestamp + common.REQUEST_LOST_TIMEOUT,
			count=request_count,
		)

		if requests_list:
			self._is_collector_task = True
			# 存request
			self._put_requests(requests_list)

	def _put_requests(self, requests_list):
		for request in requests_list:
			try:
				request_dict = {
					"request_obj": Request.from_dict(eval(request)),
					"request_redis": request
				}
				self._todo_requests.append(request_dict)
			except Exception as e:
				log.error(f"数据格式转换失败, 失败原因: {e}, 失败请求request: {request}")

	def _add_node_heartbeat(self):
		"""
			添加节点的心跳
		"""
		self._redis_db.zadd(self._mission_spider_status, self._spider_mark, tools.get_current_timestamp())

	def _delete_node_heartbeat(self):
		"""
			删除节点的心跳
		"""
		self._redis_db.zremrangebyscore(self._mission_spider_status, "-inf",
		                                tools.get_current_timestamp() - (self._interval + 10))

	def run(self):
		while not self._thread_stop:
			try:
				self._add_node_heartbeat()
				self._put_data()
			except Exception as e:
				log.error(f"{e}")

			self._is_collector_task = False
			tools.sleep_time(self._interval)

	def get_requests(self, count):
		"""
			获取指定个数的请求
		:param count: 请求个数
		:return: 获取到指定个数的请求
		"""
		requests = []
		count = count if count <= len(self._todo_requests) else len(self._todo_requests)
		while count:
			requests.append(self._todo_requests.popleft())
			count -= 1

		return requests

	def stop(self):
		self._thread_stop = True

	def get_requests_count(self):
		"""
			获取待处理任务数量
		"""
		return len(self._todo_requests) or self._redis_db.zcount(self._mission_request_name) or 0

	def is_collector_task(self):
		"""
			获取任务处理状态
		"""
		return self._is_collector_task
