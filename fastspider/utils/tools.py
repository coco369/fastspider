# encoding=utf-8
import pickle
import time

from fastspider.settings import common


def key_to_hump(key):
	"""
		将变量转化为驼峰命名
	:return: 返回驼峰命名变量
	"""
	return key.lower().title().replace("_", "")


def check_class_method(obj, name):
	"""
		检查对象是否有某个属性
	:return:
	"""
	try:
		return getattr(obj, str(name))
	except Exception as e:
		print(f"对象{obj} 没有方法{str(name)}")
		return None


def get_tunnel_proxy():
	"""
		隧道代理
	"""
	try:
		if common.PROXY_ENABLE:
			proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
				"host": common.PROXY_TUNNEL_HOST,
				"port": common.PROXY_TUNNEL_PORT,
				"user": common.PROXY_TUNNEL_USER,
				"pass": common.PROXY_TUNNEL_PASSWORD,
			}
			proxies = {
				"http": proxy_meta,
				"https": proxy_meta,
			}
			return proxies
		return None
	except Exception as e:
		return None


def sleep_time(times):
	"""
		休眠指定时间
	:param times: 秒
	"""
	time.sleep(times)


class Singleton(object):
	def __init__(self, cls):
		self._cls = cls
		self._instance = {}

	def __call__(self, *args, **kwargs):
		if self._cls not in self._instance:
			self._instance[self._cls] = self._cls(*args, **kwargs)
		return self._instance[self._cls]


def cookies2dict(cookies):
	"""
		将request中的cookies解析为字典
	"""
	cookie_dict = {}
	for i in cookies.split(";"):
		cookie = i.split("=")
		cookie_dict[cookie[0]] = cookie[1]
	return cookie_dict


def pascal_case_to_snake_case(name):
	"""
		将驼峰命名改为单词下划线命名
	:param name: 驼峰命名变量
	:return: 单词下划线命名变量
	"""
	snake_name = []
	for index, char in enumerate(name):
		if index != 0 and char.isupper():
			snake_name.append("_")
		snake_name.append(char)
	return "".join(snake_name).lower()


def time_to_timestamp(strtime):
	"""
		将字符串时间转换为时间戳
	"""
	timeArray = time.strptime(strtime, "%Y-%m-%d %H:%M")
	return int(time.mktime(timeArray))


def get_current_timestamp():
	"""
		获取当前时间的时间戳
	"""
	return int(time.time())


def dumps_obj(obj):
	return pickle.dumps(obj)


def loads_obj(obj_str):
	return pickle.loads(obj_str)
