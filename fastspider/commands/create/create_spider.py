# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/27

Desc: 创建爬虫项目
"""
import os
import re

from utils import tools


class CreateFastSpider(object):

	@staticmethod
	def get_spider_tmpl(spider_type):
		"""
			获取爬虫模板
		:param spider_type: 爬虫类型
		:return: 返回爬虫类型对应的模板内容
		"""
		if spider_type == "air":
			tmp_name = "air_spider.tmpl"
		elif spider_type == "nomal":
			tmp_name = "nomal_spider.tmpl"
		elif spider_type == "cycle":
			tmp_name = "cycle_spider.tmpl"
		else:
			raise Exception('spider_type error, must choice "air" "nomal" "cycle" ')

		with open(os.path.join(os.path.join(
				os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates"),
				             "spiders")), tmp_name)) as f:
			spider_template = f.read()

		return spider_template

	@staticmethod
	def create_spider(spider_class_name, spider_name, spider_template):
		"""
			创建爬虫文件
		:param spider_class_name: 基于启动命令行中的爬虫名称来定义爬虫的类名，爬虫名称会转化为驼峰命名
		:param spider_template: 基于爬虫类型, 传入的对应的爬虫模板文件的内容
		:return: 生成指定爬虫类型的爬虫文件内容
		"""
		spider_template = spider_template.replace("{{spider_class_name}}", spider_class_name)
		spider_file = f"{spider_name}.py"
		if os.path.exists(spider_file):
			input_params = input(f"文件{spider_file}已存在, 请选择覆盖y 还是 取消此操作n: ")
			if input_params not in ['y', 'Y']:
				print("取消创建爬虫的操作 退出")
				return
		with open(spider_file, "w+", encoding="utf-8") as f:
			f.write(spider_template)
			print(f"爬虫 {spider_file} 已成功生成")

	def create(self, spider_name, spider_type):
		name_regex = re.compile(r"^[a-zA-Z][a-zA-Z_]*$")
		if not name_regex.findall(spider_name):
			raise Exception("爬虫名称不符合要求, 请输入")

		spider_class_name = tools.key_to_hump(spider_name)
		spider_template = self.get_spider_tmpl(spider_type)
		self.create_spider(spider_class_name, spider_name, spider_template)
