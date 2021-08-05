# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/05

Desc: mysql的pipeline管道
"""
from fastspider.pipeline.base_pipeline import BasePipeline


class MysqlPipeline(BasePipeline):

	def __init__(self):
		pass

	def save_items(self, table, items):
		"""
			管道pipeline中必须被实现的方法
		"""
		pass
