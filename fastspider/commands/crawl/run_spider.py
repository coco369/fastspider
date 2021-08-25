# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/25

Desc: 解析启动爬虫命令行参数, 并启动对应的爬虫
"""
import sys
import importlib

from fastspider.settings import common

sys.path.append(common.BASE_PATH)


class RunFastSpider(object):

	@classmethod
	def run(cls, spider_path, thread_count):
		module, class_name = spider_path.rsplit(".", 1)
		mod = importlib.import_module(module)
		try:
			obj = getattr(mod, class_name)
		except AttributeError:
			raise NameError(f"Module '{module}' doesn't define any object named '{class_name}'")

		obj(thread_count).start()
