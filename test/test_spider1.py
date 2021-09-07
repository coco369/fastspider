# encoding=utf-8
import time

import fastspider


class TestSpider(fastspider.Spider):
	start_urls = ["https://movie.douban.com/top250", "https://movie.douban.com/top250?start=25&filter=",
	              "https://movie.douban.com/top250?start=50&filter=", "https://movie.douban.com/top250?start=75&filter=",
	              "https://movie.douban.com/top250?start=100&filter="]

	def start_requests(self):
		for url in self.start_urls:
			yield fastspider.Request(url=url)

	def parser(self, request, response):
		movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
		for movie in movies:
			href = movie.xpath('./div/div[2]/div[1]/a/@href')[0].get()
			title = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].get()

			print(href, title)


if __name__ == "__main__":
	TestSpider("test", 3).start()
