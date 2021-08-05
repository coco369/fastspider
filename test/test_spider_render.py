# encoding=utf-8
import json
import re

import fastspider
from fastspider.item.item import Item
from fastspider.utils.tools import cookies2dict


class TmallCheapItem(Item):

	def __init__(self, href="", title="", price="", msg="", src=""):
		self.table_name = "tmall_cheap"
		self.href = href
		self.title = title
		self.price = price
		self.msg = msg
		self.src = src


class TestSpider(fastspider.LightSpider):
	start_urls = [
		"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop"
	]

	detail_api = "https://mdskip.taobao.com/mobile/queryH5Detail.htm?itemId="

	detail_url = "https://detail.tmall.com/item.htm?id="

	def start_requests(self):
		for url in self.start_urls:
			yield fastspider.Request(url=url, callback=self.parse, web_render=True, web_render_scroll=True)

	def parse(self, request, response):
		text = response.content
		patterns = re.compile(r'href="//a.m.taobao.com/i(.*?).htm')
		result = patterns.findall(text)
		cookies = cookies2dict(
			"_tb_token_=e6b5a0e9e3a75;cookie2=199d289165818892c52422ad65a04320;t=d4fea93bd0a64ba2f26f6c098b82f5b6")
		headers = {
			"referer": "https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
		}
		for gid in result[:5]:
			tm_detail_api = self.detail_api + gid
			meta = {"gid": gid, "cookies": cookies, "headers": headers}
			yield fastspider.Request(url=tm_detail_api, cookies=cookies, headers=headers, callback=self.parse_detail,
			                         meta=meta, verify=False)

	def parse_detail(self, request, response):
		meta = response.meta
		text = response.content
		data = json.loads(str(text, encoding='gbk').replace('\n', ''))
		if data.get("item"):
			meta["title"] = data["item"]["title"]
			meta["price"] = data["price"]["price"]["priceText"]
			meta["msg"] = data['resource']['bigPromotion']['memo'][0]['text']
			# 获取图片
			tm_detail_url = self.detail_url + meta["gid"]
			meta["href"] = tm_detail_url
			yield fastspider.Request(url=tm_detail_url, cookies=meta["cookies"], headers=meta["headers"],
			                         callback=self.parse_detail_html, meta=meta, verify=False)
		else:
			print("过期")

	def parse_detail_html(self, request, response):
		meta = response.meta
		src = response.xpath('//*[@id="J_UlThumb"]/li[1]/a/img/@src').get()
		print(src, meta["title"], meta["price"], meta["msg"], meta["href"])
		item = TmallCheapItem(src=src, title=meta["title"], price=meta["price"], msg=meta["msg"], href=meta["href"])
		yield item


if __name__ == "__main__":
	TestSpider(5).start()
