# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/27

Desc: 创建爬虫项目
"""
import re

from utils.tools import key_to_hump


class CreateFastSpider(object):

	def get_spider_tmpl(self, spider_type):
		"""
			获取爬虫模板
		:param spider_type: 爬虫类型
		:return: 返回爬虫类型对应的模板内容
		"""
		if spider_type == "air":
			tmp_name = "air_spider.tmpl"
		elif spider_type == "nomal":
			tmp_name = "nomal_spider.tmpl"

		return

	def create_spider(self, spider_class_name, spider_template):
		"""
			创建爬虫文件
		:param spider_class_name: 基于启动命令行中的爬虫名称来定义爬虫的类名，爬虫名称会转化为驼峰命名
		:param spider_template: 基于爬虫类型, 传入的对应的爬虫模板文件
		:return: 生成指定爬虫类型的爬虫文件内容
		"""
		return

	def create(self, spider_name, spider_type):
		name_regex = re.compile(r"^[a-zA-Z][a-zA-Z_]*$")
		if not name_regex.findall(spider_name):
			raise Exception("爬虫名称不符合要求, 请输入")

		spider_class_name = key_to_hump(spider_name)
		spider_template = self.get_spider_tmpl(spider_type)
		spider = self.create_spider(spider_class_name, spider_template)

		pass
