# encoding=utf-8
import json
import re
from datetime import date

import fastspider
from fastspider.utils import tools
from fastspider.utils.tools import cookies2dict


# from dev import TOKEN, DOMAIN
# from settings import APIKEY


class TestSpider(fastspider.LightSpider):
	sz_start_urls = [
		["https://sanzhisongshu.tmall.com/shop/view_shop.htm?spm=a230r.1.14.4.7cac3422aI4hF5&user_number_id=880734502",
		 "jhs_1"],
		[
			"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w15914388-17459263184.11.12c25ce8Iio9Pf&wh_sid=84a0f5c4d1f663e6&sellerId=880734502&scene=taobao_shop",
			"jhs_2"],
	]

	lyf_start_urls = [
		[
			"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.1-b-s.w5003-23915965559.1.4d0252e8CQ9ayx&wh_sid=8dc6f5b94c42a26f&sellerId=732501769&scene=taobao_shop",
			"jhs_2"],
	]

	bcw_start_urls = [
		[
			"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop",
			"jhs_2"],
		[
			"https://baicaowei.tmall.com/?ali_refid=a3_430582_1006:1103173608:N:yXJrW6DMoWk3LhCIzaFIbg%3D%3D:ec44b6d0b36892558bde14256a4834c6&ali_trackid=1_ec44b6d0b36892558bde14256a4834c6&spm=a230r.1.14.4",
			"jhs_1"],
	]

	lppz_start_urls = [
		["https://liangpinpuzi.tmall.com/shop/view_shop.htm?spm=a230r.1.14.15.4f7c3274zasarX&user_number_id=619123122",
		 "jhs_3"]
	]

	detail_api = "https://mdskip.taobao.com/mobile/queryH5Detail.htm?itemId="

	detail_url = "https://detail.tmall.com/item.htm?id="
	# 使用订单侠查询商品详情接口
	ddx_detail_url = "http://api.tbk.dingdanxia.com/tbk/item_info"

	# save_bp_data = f"{DOMAIN}/xserver/admin/lab/bp/save"

	def start_requests(self):
		# 三只松鼠
		# start_urls = self.sz_start_urls + self.lyf_start_urls + self.bcw_start_urls + self.lppz_start_urls
		start_urls = self.sz_start_urls
		for item in start_urls:
			yield fastspider.Request(url=item[0], callback=self.parser, web_render=True, web_render_scroll=True,
			                         web_render_time=0, meta={"type": item[1]})

	def parser(self, request, response):
		type = response.meta["type"]
		text = response.content
		if type == "jhs_1":
			patterns = re.compile(r'detail.tmall.com.*?id=(.*?)[&%]')
		elif type == "jhs_2":
			patterns = re.compile(r'href="//a.m.taobao.com/i(.*?).htm')
		elif type == "jhs_3":
			patterns = re.compile(r'item.taobao.com.*?id=(.*?)&')

		result = patterns.findall(text)
		cookies = cookies2dict(
			"_tb_token_=e6b5a0e9e3a75;cookie2=199d289165818892c52422ad65a04320;t=d4fea93bd0a64ba2f26f6c098b82f5b6")
		headers = {
			"referer": "https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w20163031-22649597774.17.564348b739A6q4&wh_sid=a9e13bad3df9ada9&sellerId=628189716&scene=taobao_shop",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
		}
		print(list(set(result)))
		for gid in list(set(result)):
			tm_detail_api = self.detail_api + gid
			meta = {"gid": gid, "cookies": cookies, "headers": headers}
			yield fastspider.Request(url=tm_detail_api, cookies=cookies, callback=self.parser_detail, meta=meta,
			                         verify=False)

	def parser_detail(self, request, response):
		try:
			meta = response.meta
			text = response.content
			data = json.loads(str(text, encoding='gbk').replace('\n', ''))
			if data.get("item"):
				priceTip = data["price"].get("priceTip")
				# 判断活动是否待预售
				if priceTip and "已秒完" not in priceTip:
					meta["title"] = "【" + priceTip.split('，')[0] + "】 " + data["item"]["title"]
					# meta["price"]  (\d*.\d*?)元  (\d)月(\d)日( \d*:\d*)
					price_title = re.compile("前(\d+)件.*?([.\d]+)元").findall(priceTip)
					meta["blockedBy"] = "admin"
					if price_title:
						# blockedBy=admin 冻结   blockedBy=N 不冻结
						meta["blockedBy"] = "N"

					price = re.compile("([.\d]+)元").findall(priceTip)
					meta["price"] = price[0] if price else ""

					startAt = re.compile("(\d*)月(\d*)日( \d*:\d*)[开始,有效]").findall(priceTip)
					# startAt = re.compile("(\d)月(\d)日( \d*:\d*)有效").findall(priceTip)
					month, day, hour = startAt[0][0], startAt[0][1], startAt[0][2]

					new_startAt = f"{date.today().year}-{month}-{day}{hour}"
					timeArray = tools.time_to_timestamp(new_startAt)
					meta["startAt"] = int(str(int(timeArray)).ljust(13, '0'))
					# 获取图片
					meta["href"] = self.detail_url + meta['gid']
				# data = {
				# 	"apikey": APIKEY,
				# 	"num_iids": meta['gid']
				# }
				# yield fastspider.Request(url=self.ddx_detail_url, headers=meta["headers"], meta=meta, verify=False,
				#                          callback=self.parser_detail_html, data=data)
			else:
				print(f"商品:{meta['gid']} 已过期")
		except Exception as e:
			print(e)

# def parser_detail_html(self, request, response):
# 	meta = response.meta
# 	src = json.loads(response.text)["data"][0]["pict_url"]
# 	# 保存数据
# 	data = {
# 		"id": meta["gid"],
# 		"name": meta["title"],
# 		"linkUrl": meta["href"],
# 		"imgUrl": src,
# 		"type": "淘宝",
# 		"price": meta["price"],
# 		"startAt": meta["startAt"],
# 		"platType": "food",
# 		"blockedBy": meta["blockedBy"]
# 	}
# 	headers = {
# 		'token': TOKEN,
# 		'Content-Type': 'application/json'
# 	}
# 	print(data)
# 	yield fastspider.Request(url=self.save_bp_data, method="POST", json=data, headers=headers,
# 	                         callback=self.save_parser)
#
# def save_parser(self, request, response):
#
# 	print(response)
# 	print(response.text)


if __name__ == '__main__':
	TestSpider().start()

