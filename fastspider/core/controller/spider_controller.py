# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/29

Desc: fastspider核心代码, 控制器
"""
from threading import Thread


class BaseController(Thread):
	# 统计任务执行成功的个数 和 任务执行失败的个数, 用于后期统计任务执行成功率, 成功率太低, 则发送报警信息
	# 成功率计算公司  失败任务总数 / 总任务数 > 0.5 则发送报警信息
	_success_task_num = 0
	_fail_task_num = 0

	has_task_flag = True

	def __init__(self):
		super(BaseController, self).__init__()

		self._thread_stop = False

	def has_task(self):
		return self.has_task_flag

	def stop(self):
		# 将线程启动的标识 设置为True
		self._thread_stop = True

	def add_parser(self):
		pass

	def run(self):
		while not self._thread_stop:
			pass


class AirSpiderController(BaseController):

	def __init__(self, memory_db):
		super(AirSpiderController, self).__init__()

		pass

	def run(self):
		pass
