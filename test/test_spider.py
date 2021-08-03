# encoding=utf-8

import fastspider


class TestSpider(fastspider.LightSpider):
	start_urls = ["https://movie.douban.com/top250", "https://movie.douban.com/top250?start=25&filter=",
	              "https://movie.douban.com/top250?start=50&filter="]

	# def start_requests(self):
	# 	yield fastspider.Request("https://movie.douban.com/top250", callback=self.parse)

	def parse(self, request, response):
		print(response)
		movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
		for movie in movies:
			href = movie.xpath('./div/div[2]/div[1]/a/@href')[0].get()
			title = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].get()
			print(href, title)


if __name__ == "__main__":
	TestSpider().start()
