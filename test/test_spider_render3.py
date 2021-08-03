# encoding=utf-8
import json
import re
import time

import fastspider
from fastspider.utils.tools import cookies2dict


class TestSpider(fastspider.LightSpider):
	start_urls = [
		"https://detail.tmall.com/item.htm?id=13060317764"
	]

	def start_requests(self):
		headers = {
			"referer": "https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
		}
		for url in self.start_urls:
			yield fastspider.Request(url=url, callback=self.parse, headers=headers)

	def parse(self, request, response):
		print(response)

		src = response.xpath('//*[@id="J_UlThumb"]/li[1]/a/img/@src').get()
		print(src)


if __name__ == "__main__":
	TestSpider().start()
