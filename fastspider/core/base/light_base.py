# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: fastspider核心爬虫LightSpider的基类代码
"""
from datetime import datetime

from fastspider.http.request.request import Request
from fastspider.waring.feishu import FeiShuRobot
from fastspider.settings import common


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
		"""
			向飞书\企业微信\钉钉 推送任务开始信息
		"""
		# TODO: 先实现向飞书机器人推送信息
		if common.FEISHU_SECRET and common.FEISHU_WEB_HOOK:
			msg = f"爬虫{self.name}开始启动, 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
			FeiShuRobot().send_msg(msg)

	def end_callback(self):
		"""
			向飞书\企业微信\钉钉 推送任务结束信息
		"""
		# TODO: 先实现向飞书机器人推送信息
		if common.FEISHU_SECRET and common.FEISHU_WEB_HOOK:
			msg = f"爬虫{self.name}执行完毕, 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
			FeiShuRobot().send_msg(msg)

	@property
	def name(self):
		# 示例方法, 获取类名
		return self.__class__.__name__

