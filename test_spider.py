# encoding=utf-8

import fastspider


class TestSpider(fastspider.AirSpider):

	def start_requests(self):
		yield fastspider.Request("http://www.baidu.com")

	def parse(self, response):
		print(response.text)


if __name__ == "__main__":
	TestSpider().start()
