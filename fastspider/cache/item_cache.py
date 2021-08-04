# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心代码, item实体缓存
"""
import importlib
from queue import Queue
from threading import Thread

from fastspider.item.item import Item
from fastspider.utils import tools
from fastspider.settings import common


class ItemCache(Thread):
	MAX_ITEM_COUNT = 5000
	DEAL_ITEM_MAX_SIZE = 500

	def __init__(self, redis_key):
		super(ItemCache, self).__init__()

		self._thread_stop = False

		self._item_queue = Queue(maxsize=self.__class__.MAX_ITEM_COUNT)

		self._redis_key = redis_key
		# 定义Item名在redis中的key值
		self._table_item = "{redis_key}:{table_name}"
		# 存储不同Item对redis中的key值的对应关系
		self._item_table = {}

		self._pipelines = self.load_pipelines()

	def flush(self):
		"""
			从队列中获取指定数量的item对象, 如果item对象获取满500个, 则开始处理item对象. 如果item对象不足500个, 则单独处理item对象
		:return:
		"""
		count, items = 0, []

		while not self._item_queue.empty():
			data = self._item_queue.get_nowait()
			count += 1

			if isinstance(data, Item):
				items.append(data)
			# TODO: 暂时不做item去重
			else:
				# TODO: 其他情况, 暂不处理
				print("其他情况, 暂不处理")

			if count >= self.__class__.DEAL_ITEM_MAX_SIZE:
				self.__add_item_to_db(items)

				count, items = 0, []

		if items:
			self.__add_item_to_db(items)

	def __pick_items(self, items):
		"""
			将不同Item对象区分开
		"""
		item_dict = {}
		while items:
			item = items.pop(0)
			item_name = item.item_name

			if self._item_table.get(item_name):
				table_item = self._item_table.get(item_name)
			else:
				# 组装redis中存储的key值
				table_item = self._table_item.format(
					redis_key=self._redis_key, table_name=item_name
				)
				self._item_table[item_name] = table_item

			if table_item not in item_dict:
				item_dict[table_item] = []
			# 将不同Item对象的数据保存到item_dict字典中.格式为{item对应的redis key值: [item字典, item字典].....}
			item_dict[table_item].append(items.to_dict)
		return item_dict

	def load_pipelines(self):
		"""
			加载settings中定义的piplines
		:return:
		"""
		pipelines = []
		for pipeline in common.ITEM_PIPELINES:
			module, class_name = pipeline.rsplit(".", 1)
			pipeline_cls = importlib.import_module(module).__getattribute__(class_name)

			if not isinstance(pipeline_cls(), "BasePipeline"):
				raise Exception(f"{class_name}必须继承 BasePipeline ")

			pipelines.append(pipeline_cls())
		return pipelines

	def __save_item_to_db(self, table_name, item_data):
		"""
			保存数据
		:param table_name: redis key名称
		:param item_data: 存储的数据
		:return:
		"""
		pass

	def __add_item_to_db(self, items):
		"""
			处理item对象
		"""
		# 处理item对象的信息, 返回redis队列和序列化item信息
		items_dict = self.__pick_items(items)
		if items_dict:
			table_name, item_data = items_dict.popitem()
			self.__save_item_to_db(table_name, item_data)

	def run(self):
		while not self._thread_stop:
			self.flush()
			tools.sleep_time(0.5)
