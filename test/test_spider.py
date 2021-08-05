# encoding=utf-8

import fastspider
from fastspider.item.item import Item


class DoubanItem(Item):

	def __init__(self, href, title):
		self.table_name = "douban"
		self.href = href
		self.title = title


class TestSpider(fastspider.LightSpider):
	# start_urls = ["https://movie.douban.com/top250", "https://movie.douban.com/top250?start=25&filter=",
	#               "https://movie.douban.com/top250?start=50&filter="]
	start_urls = ["https://movie.douban.com/top250"]

	# def start_requests(self):
	# 	yield fastspider.Request("https://movie.douban.com/top250", callback=self.parse)

	def parse(self, request, response):
		print(response)
		movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
		for movie in movies:
			href = movie.xpath('./div/div[2]/div[1]/a/@href')[0].get()
			title = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].get()

			print(href, title)
			douban_item = DoubanItem(href, title)
			yield douban_item


if __name__ == "__main__":
	TestSpider(3).start()
