# encoding=utf-8
import json
import re
import time

import requests

import fastspider
from fastspider.utils.tools import cookies2dict


class TestSpider(fastspider.LightSpider):
	start_urls = [
		# "https://mdskip.taobao.com/mobile/queryH5Detail.htm?itemId=646958187838"
		"https://detail.tmall.com/item.htm?id=646958187838"
	]

	def start_requests(self):
		cookies = cookies2dict("_tb_token_=e6b5a0e9e3a75; cookie2=199d289165818892c52422ad65a04320; t=d4fea93bd0a64ba2f26f6c098b82f5b6")
		headers = {
			"referer": "https://detail.tmall.com/",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "keep-alive"
		}
		for url in self.start_urls:
			meta = {
				"cookies": cookies,
				"headers": headers
			}
			yield fastspider.Request(url=url, callback=self.parse, headers=headers, meta=meta)

	def parse(self, request, response):
		meta = response.meta
		print(meta)
		text = response.content
		data = json.loads(str(text, encoding='gbk').replace('\n', ''))
		print(data)



if __name__ == "__main__":
	TestSpider().start()
