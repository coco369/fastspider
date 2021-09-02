# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 定时器scheduler
"""
import threading

from fastspider.settings import common


class Scheduler(threading.Thread):
	__common_settings__ = {}

	def __init__(self):
		"""
			定时执行爬虫任务的调度器
		"""
		self.cycle_interval = 0

		super(Scheduler, self).__init__()

		# 解析自定义的字典__common_settings__ 变量中的参数
		for k, v in self.__class__.__common_settings__.items():
			setattr(common, k, v)

	def _start(self):
		# 启动相关线程

		pass

	def run(self):

		while True:
			pass
