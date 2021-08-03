import json
from urllib.parse import urlencode

import fastspider


class TestTmall(fastspider.LightSpider):
	"""
		令牌过期, 需要替换params中data的 pvuuid 值和 sign 以及 headers中的cookies
		获取聚划算分两个接口, params中的data也分两种情况
	"""
	start_urls = [
		"https://h5api.m.tmall.com/h5/mtop.tmall.kangaroo.core.service.route.pagerecommendservice/1.0/?",
	]

	def start_requests(self):
		params = {
			"jsv": "2.6.1",
			"appKey": "12574478",
			"t": "1627898871097",
			"sign": "3e2fd70745b86fa410010deea9c4f937",
			"api": "mtop.tmall.kangaroo.core.service.route.PageRecommendService",
			"v": "1.0",
			"param": """[object Object]""",
			"timeout": "3000",
			"jsonpIncPrefix": "kangaroo",
			"dataType": "jsonp",
			"preventFallback": "true",
			"type": "jsonp",
			"callback": "mtopjsonpkangaroo4",
			# "data": """{"url":"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w15914388-17459263184.11.12c25ce8Iio9Pf&wh_sid=84a0f5c4d1f663e6&sellerId=880734502&scene=taobao_shop","cookie":"hng=CN|zh-CN|CNY|156","pvuuid":"v1-eb25321b-092f-4959-b751-f67ffd7d9e98-1627898864165","fri":"{\\"moduleIdList\\":[\\"3986989690\\",\\"9707198930\\",\\"3305063800\\",\\"7752805340\\",\\"7284623640\\",\\"6491981960\\",\\"8153725620\\",\\"2871549900\\",\\"2094891590\\",\\"6591518700\\",\\"9530138980\\",\\"5254386120\\",\\"8098797430\\",\\"4866466790\\",\\"9494683320\\",\\"5019401070\\",\\"5335728530\\",\\"2432255390\\",\\"3689093040\\"]}","schemaVersion":"c519d06a-55a9-46dc-be04-877ff3f13409","sequence":3,"excludes":"2094891590;2871549900;3305063800;3986989690;5254386120;6491981960;6591518700;7284623640;7752805340;8153725620;9530138980;9707198930","device":"pc","backupParams":"excludes,device"}"""
			"data": """{"url":"https://pages.tmall.com/wow/ark-pub/common/db6e866b/tpl?spm=a1z10.3-b-s.w15914388-17459263184.11.12c25ce8Iio9Pf&wh_sid=84a0f5c4d1f663e6&sellerId=880734502&scene=taobao_shop","cookie":"hng=CN|zh-CN|CNY|156","pvuuid":"v1-eb25321b-092f-4959-b751-f67ffd7d9e98-1627898864165","fri":"{\\"moduleIdList\\":[\\"3986989690\\",\\"9707198930\\",\\"3305063800\\",\\"7752805340\\",\\"7284623640\\",\\"6491981960\\",\\"8153725620\\",\\"2871549900\\",\\"2094891590\\",\\"6591518700\\",\\"9530138980\\",\\"5254386120\\",\\"8098797430\\",\\"4866466790\\",\\"9494683320\\",\\"5019401070\\",\\"5335728530\\",\\"2432255390\\",\\"3689093040\\"]}","schemaVersion":"c519d06a-55a9-46dc-be04-877ff3f13409","sequence":2,"excludes":"3305063800;3986989690;6491981960;7284623640;7752805340;8153725620;9707198930","device":"pc","backupParams":"excludes,device"}"""
		}
		headers = {
			"Host": "h5api.m.tmall.com",
			"Cookie": "cna=z2dgGUY6wVsCAbaUcgOXTPOu; hng=CN%7Czh-CN%7CCNY%7C156; t=dbfb4fe94b6d684f7bc00c3d45fec865; _tb_token_=753851b8f5eee; cookie2=1aaf9e03a3365820865d17902f6f7ef6; xlly_s=1; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v1XFl6j7SvTEhgOFG8ZODABUcb7AOD%2BiuM61sNTeCFO6cjoyLtZBdyV8Ftg9DjKRTs2MSPx5aXDeVbjtNata3mduWbLVvQd%2FprBYEjxm3FU6MHFjJ1Ek71%2FCmhKMxCYRuRL6FAwVNhLXR8qmIKfWZhoFSzFuiS8a72ZgGcEeKt8SYKhsoI%2Bii3VPn7%2FkvBo6xJbOL8SwQkE5XxSZkoHY%2BViIRcenevY7i9qCdWxOUeAOvl7W6TgFv%2BRCs%3D; miid=248935710892448696; dnk=wang779598160; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=URm48syIYn73&cookie14=Uoe2yt28yU2tzA%3D%3D; uc3=vt3=F8dCujPwtebwX4BQ7ts%3D&nk2=FPjankxl8h7%2FtsBX2w%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D&id2=VAYrEn2psuPG; tracknick=wang779598160; uc4=id4=0%40Vh%2B56EJYlXZqQsRPzH4qvtG3gis%3D&nk4=0%40FnNat8zj29hCq6XUqDZSFGOK%2FHSEsgXh; lgc=wang779598160; login=true; cancelledSubSites=empty; csg=45796b34; enc=O3Hpc%2Ff36a8PeHONP%2B4YxDgIe0JMVWBfJNDzsbUIfu7jPzlQmUhezqS2wMxbBl6S5c5t6fRjeOlNeR6NvdR99Q%3D%3D; _m_h5_tk=173e91bf1a3e0e97b95b773266ec1b7c_1627903897321; _m_h5_tk_enc=616dc2cfbfd663cf39c45eef0f639447; tfstk=cnbVBQvZ0rUqfxY_vETalGRYkKoAZgCcs4RBmgC5iuCzxFKcibM9ZGukaC9Lrnf..; l=eBOOJLGRjVJholeUBOfZnurza77TIIRAguPzaNbMiOCPOgCM5tx1W6hkwP8HCnGVh6u6R3Rj4pR4BeYBqCmWXFQpwm4ty4Hmn; isg=BOXl1w4T6OOQcQ3lTHinmrcp9KEfIpm0XzHAuefKq5wq_gVwr3BQhVqQiGKIfrFs",
			"sec-ch-ua": 'Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
			"sec-ch-ua-mobile": "?0",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
			"accept": "*/*",
			"sec-fetch-site": "same-site",
			"sec-fetch-mode": "no-cors",
			"sec-fetch-dest": "script",
			"referer": "https://pages.tmall.com/",
			"accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
		}

		cookies = {
			'''
				cookie: t=23ba92232b7677dafdee2a748abbfc0f
				cookie: _tb_token_=3b137e1d71e5
				cookie: cookie2=1d6df488e8e33b5cc0894267b95caddc
				cookie: _m_h5_tk=eeb0bb31c0fcc77ee445367c0186231a_1627881573316
				cookie: _m_h5_tk_enc=9eebae74dab94fbd9d168446d10b335e
			'''
		}
		for url in self.start_urls:
			params = urlencode(params)
			new_url = url + params.replace("+", "%20")
			# yield fastspider.Request(url=new_url, headers=headers)

			# for i in ["http://pypi.douban.com", "http://pypi.douban.com"]:
			for i in ["https://www.baidu.com", "https://www.baidu.com"]:
				yield fastspider.Request(url=i, headers=headers)

	def parse(self, request, response):
		text = response.text
		print(text)
		result = json.loads(text[20:-1])

		data = result["data"]["resultValue"]["data"]
		for key, value in data.items():
			print(key)
			if value:
				for goods in value.get("item") or []:
					print(goods["itemTitle"], goods["itemActPrice"])


if __name__ == '__main__':
	t = TestTmall()
	t.start()
# url1 饼干鹏化、果干蜜饯、大口吃肉、坚果炒货、糕点点心 params需要data
# url2 方便速食、糖巧布丁、鱿鱼海味、豆干蔬菜、猜你喜欢 prams需要data
# url3 镇店爆款 params不需要data
