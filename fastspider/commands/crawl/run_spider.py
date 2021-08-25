# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/25

Desc: 解析启动爬虫命令行参数, 并启动对应的爬虫
"""
import importlib


class RunFastSpider(object):

	@classmethod
	def run(cls, spider_path, thread_count):
		module, class_name = spider_path.rsplit(".", 1)
		spider_cls = importlib.import_module(module).__getattribute__(class_name)
		spider_cls(thread_count).start()
