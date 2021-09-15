# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 分布式爬虫spider
"""
from fastspider.core.base.cycle_base import CycleBase
from fastspider.core.scheduler.scheduler import Scheduler
from fastspider.utils import tools
from fastspider.utils.logger import log


class Spider(CycleBase, Scheduler):

	def __init__(self, redis_key=None, thread_count=None, check_task_interval=5):
		"""
			初始化
		"""
		super(Spider, self).__init__(
			redis_key=redis_key,
			thread_count=thread_count,
			check_task_interval=check_task_interval
		)

	def run(self):
		"""
			启动爬虫
		"""
		try:
			self.start_callback()

			if not self._parsers:
				self._parsers.append(self)

			# 开始启动
			self._start()
			# 判断是否结束
			while True:
				if self.all_thread_is_done():
					self.all_thread_stop()

					self.end_callback()
					
					log.info("无任务, 爬虫执行完毕")
					break

				# 休息1秒后再次检查爬虫是否还在运行
				tools.sleep_time(1)
		except Exception as e:
			log.error(f"爬虫执行异常, 异常原因: {e}")
