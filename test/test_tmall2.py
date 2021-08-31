import time
import hashlib
import requests

headers = {
	'Host': 'h5api.m.taobao.com',
	'cookie': 't=af7b753193ca2feb6387378709a363cc; _tb_token_=eb1ee3e1ee935; cookie2=1bbde7bef2d2eb9e2ea6c9104b2bbf8d; cna=PeiLFJrhqW4CAXkgmv3+E70E; _m_h5_tk=0f102b40794f5ce1cbf6189efee84f38_1543985837478; _m_h5_tk_enc=c6b00d0f38cdca735cc190e30f9eadf1; isg=BDQ0YzZQ1GD2NECvhLnjwVQ7BfJmpR7rLc7aM86VwL9COdSD9h0oh-r7vTdE2pBP',
	'Connection': 'keep-alive',
	'f-refer': 'wv_h5',
	'Accept': '*/*',
}

data = '{"shopId":"586728252","sellerId":"3459177618"}'  # 必须为这个格式
url = 'https://h5api.m.taobao.com/h5/mtop.taobao.shop.wireless.category.get/1.0/?jsv=2.4.5&appKey=12574478&t={time}&sign={sign}&api=mtop.taobao.shop.wireless.category.get&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data={data}'

# 第一次请求
# 获取
# _m_h5_tk
response = requests.get(url.format(sign='a2b39c32169159812ee93f0f4752e017', data=data, time=int(time.time() * 1000)))
res = response.cookies.get_dict()
print(res)
s = res['_m_h5_tk']
# _m_h5_tk
# 用于sign
# 的参数
s = s.split('_')[0]
print('_m_h5_tk:', res)
r = ';'.join(['{}={}'.format(k, v) for k, v in res.items()])  # 拼接ｃｏｏｏｋｉｅ
print(r)
headers['cookie'] = r

a = '{}&{}&12574478&{}'.format(s, int(time.time() * 1000), data)
print('params:', a)
print('t', int(time.time() * 1000))
ss = hashlib.md5(a.encode())
print('sign', ss.hexdigest())

# 发第二次请求
response = requests.get(url.format(sign=ss.hexdigest(), data=data, time=int(time.time() * 1000)), headers=headers)
print(response.content.decode())
print(response.url)
print(response.text)
