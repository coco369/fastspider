# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, 内存db
"""

from queue import PriorityQueue


class MemoryDB(object):
	"""
		PriorityQueue 优先级队列
		格式：q.put((数字,值))
		特点：数字越小，优先级越高。如果不传入数字, 那就按照值的asc值来判断优先级。asc值可以用过ord()方法来获取
	"""

	def __init__(self):
		self.priority_queue = PriorityQueue()

	def put(self, task):
		"""
			添加任务
		"""
		self.priority_queue.put(task)

	def get_nowait(self):
		"""
			获取队列中的任务
			get_nowait(): 强取任务, 获取不到任务, 则出现queue.empty异常
		:return: 返回任务或者None
		"""
		try:
			task = self.priority_queue.get_nowait()
			return task
		except Exception as e:
			return None

	def is_empty(self):
		"""
			判断当前队列是否为空
		:return: 队列为空, 返回True。队列不为空, 返回False
		"""
		return self.priority_queue.empty()
