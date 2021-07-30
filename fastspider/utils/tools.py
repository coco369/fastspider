# encoding=utf-8


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
