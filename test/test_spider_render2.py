# encoding=utf-8
import json
import re
import time

import requests

import fastspider
from fastspider.utils.tools import cookies2dict


class TestSpider(fastspider.LightSpider):
	start_urls = [
		# "https://mdskip.taobao.com/core/initItemDetail.htm?itemId=13060317764"
		"https://mdskip.taobao.com/mobile/queryH5Detail.htm?itemId=13060317764"
	]

	def start_requests(self):
		# cookies = cookies2dict("enc=He0FFUfznnffpjS6YSXQiTktURoDYk0on8ZMuumJrVPIKvBtMFgThw7BQ%2F97zg%2BQ7aFqB86eSU%2F5SNj8c%2FThpQ%3D%3D;x5sec=7b226d616c6c64657461696c736b69703b32223a226330303336333135643931663031363236386133656634396666623265323538434c696670496747454f794f6c72502b362b6d397577456f416a443874736d4e41673d3d227d")
		cookies = cookies2dict("_tb_token_=e6b5a0e9e3a75; cookie2=199d289165818892c52422ad65a04320; t=d4fea93bd0a64ba2f26f6c098b82f5b6")
		headers = {
			"referer": "https://detail.tmall.com/",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "keep-alive"
		}
		for url in self.start_urls:
			# print('111111')
			# proxies = requests.get("http://139.196.28.232:8090/proxy?key=proxy").json()
			# print(proxies)
			meta = {
				"cookies": cookies,
				"headers": headers
			}
			yield fastspider.Request(url=url, callback=self.parse, headers=headers, meta=meta)
			# yield fastspider.Request(url=url, callback=self.parse, cookies=cookies, headers=headers, meta=meta)

	def parse(self, request, response):
		meta = response.meta
		print(meta)
		text = response.content
		data = json.loads(str(text, encoding='gbk').replace('\n', ''))
		print(data)
		if data.get("defaultModel"):
			print(data["defaultModel"]["detailPageTipsDO"]["warmingUpHintText"])
		else:
			print("过期")


if __name__ == "__main__":
	TestSpider().start()
