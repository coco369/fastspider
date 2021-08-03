# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/30

Desc: fastspider核心代码, 封装response包
"""
from bs4 import BeautifulSoup
from requests.models import Response as res

# from fastspider.http.selector import Selector
from parsel import Selector


class Response(res):
	"""
		封装requests中的响应Response
	"""

	def __init__(self, response):
		super(Response, self).__init__()
		# 将response的属性同步到封装的Response对象上
		self.__dict__.update(response.__dict__)

		# 编码的严格程度, strict \ replacce \ ignore
		self.encoding_errors = "strict"
		# 加载响应内容
		self._load_selector = None

	@property
	def selector(self):
		"""
			获取已经解析过的selector对象
		:return:
		"""
		if not self._load_selector:
			# TODO: 可以封装Selector的方法
			# self._load_selector = Selector(self.text)
			self._load_selector = Selector(self.text)
		return self._load_selector

	def bs4(self, parser="html.parser"):
		"""
			使用bs4进行响应内容的解析与提取
		:param parser: 解析器, 可以定义为html.parser、lxml、html5lib
		:return:
		"""
		return BeautifulSoup(self.text, parser)

	def xpath(self, query, **kwargs):
		return self.selector.xpath(query, **kwargs)
