# encoding=utf-8
import json
import re
import time

import fastspider
from fastspider.utils.tools import cookies2dict


class TestSpider(fastspider.LightSpider):
	start_urls = [
		"https://mdskip.taobao.com/core/initItemDetail.htm?itemId=618159324335"
	]

	def start_requests(self):
		cookies = cookies2dict("enc=He0FFUfznnffpjS6YSXQiTktURoDYk0on8ZMuumJrVPIKvBtMFgThw7BQ%2F97zg%2BQ7aFqB86eSU%2F5SNj8c%2FThpQ%3D%3D;x5sec=7b226d616c6c64657461696c736b69703b32223a226330303336333135643931663031363236386133656634396666623265323538434c696670496747454f794f6c72502b362b6d397577456f416a443874736d4e41673d3d227d")
		headers = {
			"referer": "https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
		}
		while True:
			for url in self.start_urls:
				yield fastspider.Request(url=url, callback=self.parse, cookies=cookies, headers=headers)

	def parse(self, request, response):
		text = response.content
		data = json.loads(str(text, encoding='gbk').replace('\n', ''))
		print(data["defaultModel"]["detailPageTipsDO"]["warmingUpHintText"])


if __name__ == "__main__":
	TestSpider().start()
