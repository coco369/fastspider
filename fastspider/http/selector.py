# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/30

Desc: fastspider核心代码, 选择器的封装
"""

from parsel import Selector as ParselSelector


class Selector(ParselSelector):

	def __init__(self, text=None):
		self.text = text
		
		super(Selector, self).__init__(text)

