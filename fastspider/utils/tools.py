# encoding=utf-8


def key_to_hump(key):
	"""
		将变量转化为驼峰命名
	:return: 返回驼峰命名变量
	"""
	return key.lower().title().replace("_", "")
