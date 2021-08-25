# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/25

Desc: 解析启动爬虫命令行参数, 并启动对应的爬虫
"""


class RunFastSpider(object):

	@classmethod
	def run(cls, spider_class_name, thread_count):

		spider_class_name(thread_count).start()
