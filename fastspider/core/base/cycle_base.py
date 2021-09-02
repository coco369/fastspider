# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心爬虫CycleSpider的基类代码
"""
from fastspider.core.base.light_base import LightBase


class CycleBase(LightBase):

	def add_task(self):
		"""
			添加任务
		"""
		pass

	def start_requests(self, task):
		"""
			启动任务, task为任务信息
		"""
		pass
