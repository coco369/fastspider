# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心爬虫AirSpider的基类代码
"""
from fastspider.http.request.request import Request


class LightBase(object):

	def start_requests(self):
		"""
			解析url地址
		:return: 返回可迭代的yield Request()
		"""
		if hasattr(self, "start_urls") and not self.start_urls:
			raise Exception("Spider 必须定义 start_urls")
		for url in self.start_urls:
			yield Request(url=url)

	def parser(self, request, response):
		"""
			默认的解析函数, 解析响应response的内容
		:param request: 请求对象
		:param response: 响应对象
		:return: 可不返回内容, 或者返回Item对象
		"""
		pass

	def start_callback(self):
		pass

	def end_callback(self):

		pass

	@property
	def name(self):
		# 示例方法, 获取类名
		return self.__class__.__name__
