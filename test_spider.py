# encoding=utf-8

import fastspider


class TestSpider(fastspider.AirSpider):

	def start_requests(self):
		yield fastspider.Request("http://www.baidu.com", callback=self.parse1)

	def parse1(self, request, response):
		print(response)

		yield fastspider.Request("https://www.runoob.com/python/python-func-callable.html", callback=self.parse2)

	def parse2(self, request, response):

		print(response)


if __name__ == "__main__":
	TestSpider().start()
