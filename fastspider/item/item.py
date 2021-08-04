# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/30

Desc: fastspider核心代码, 实体Item
"""


class BaseItemMetaClass(type):

	def __new__(cls, name, bases, attrs):
		attrs.setdefault("__name__", None)
		attrs.setdefault("__table_name__", None)
		attrs.setdefault("__update_key__", None)
		attrs.setdefault("__unique_key__", None)
		return type.__new__(cls, name, bases, attrs)


class Item(metaclass=BaseItemMetaClass):
	"""
		定义继承的元类, 子类直接拥有元类中的属性。
	"""

	def __init__(self):
		pass

	def __setitem__(self, key, value):
		self.__class__.__dict__[key] = value

	def __getitem__(self, key):
		return self.__class__.__dict__[key]

	@property
	def item_name(self):
		return self.__class__.__name__

	@property
	def table_name(self):
		return self.__table_name__

	@table_name.setter
	def table_name(self, name):
		self.__table_name__ = name

	@property
	def to_dict(self):
		item_property = {}
		for key, values in self.__class__.__dict__.items():
			if key not in ("__name__", "__table_name__", "__update_key__", "__unique_key__"):
				item_property[key] = values
		return item_property
