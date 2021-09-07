# encoding=utf-8
import time

import fastspider


class TestSpider(fastspider.Spider):
	douban_url = "https://movie.douban.com/top250"

	def start_requests(self):
		yield fastspider.Request(url=self.douban_url)

	def parser(self, request, response):
		movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
		for movie in movies:
			href = movie.xpath('./div/div[2]/div[1]/a/@href')[0].get()
			title = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].get()

			print(href, title)


if __name__ == "__main__":
	TestSpider("test", 3).start()
