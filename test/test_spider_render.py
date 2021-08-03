# encoding=utf-8

import fastspider


class TestSpider(fastspider.LightSpider):
	start_urls = ["https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop"]

	def start_requests(self):
		for url in self.start_urls:
			yield fastspider.Request(url=url, callback=self.parse, web_render=True)

	def parse(self, request, response):
		print(response)
		print(response.content)


if __name__ == "__main__":
	TestSpider().start()
