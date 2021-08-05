# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/05

Desc: pipeline基类

多态性是指具有不同功能的函数可以使用相同的函数名，这样就可以用一个函数名调用不同内容的函数.
"""
import abc
from typing import List, Dict


class BasePipeline(metaclass=abc.ABCMeta):
	"""
		使用ABCMeta作为元类来定义抽象基类
	"""

	@abc.abstractmethod
	def save_items(self, table, items: List[Dict]):
		"""
			保存数据
		:param table: 表名
		:param items: 数据 格式为 [{},{},{}....]
		:return: 保存成功返回True   保存失败返回False
		"""

		return True

	def update_items(self, table, items: List[Dict]):
		# TODO: 暂时不实现更新方法
		return True
