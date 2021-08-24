import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import loguru

from fastspider.settings.common import LOG_NAME, LOG_PATH, LOG_LEVEL, LOG_IS_WRITE_TO_CONSOLE, LOG_MAX_BYTES, \
	LOG_ENCODING, LOG_FILE_MAX_NUMBER, LOG_IS_WRITE_TO_FILE

LOG_FORMAT = "%(threadName)s|%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s| %(message)s"


class LoggerHandler(logging.Handler):
	def emit(self, record):
		"""
			使用python3中的loguru日志模块
		"""
		# 一定会被执行的方法
		logger = loguru.logger.opt(depth=6, exception=record.exc_info)
		logger.log(record.levelname, record.getMessage())


def getlogger(name=None, path=None, log_level=None, write_to_file=None, write_to_console=None, file_number=None,
              max_bytes=None, encoding=None):
	"""
		获取定义的日志logger
	:param name: 日志名称
	:param path: 日志存储地址
	:param log_level: 日志级别 INFO DEBUG WARING ERROR
	:param write_to_console: 是否打印到控制台, True or False
	:param max_bytes: 日志文件存储的最大字节数
	:param encoding: 编码格式 utf-8
	:return:
	"""
	name = name or LOG_NAME
	path = path or LOG_PATH
	log_level = log_level or LOG_LEVEL
	write_to_file = write_to_file or LOG_IS_WRITE_TO_FILE
	write_to_console = write_to_console or LOG_IS_WRITE_TO_CONSOLE
	file_number = file_number or LOG_FILE_MAX_NUMBER
	max_bytes = max_bytes or LOG_MAX_BYTES
	encoding = encoding or LOG_ENCODING

	# 获取logger对象
	logger = logging.getLogger(name)
	logger.setLevel(log_level)
	# 获取格式化formatter
	formatter = logging.Formatter(LOG_FORMAT)

	if write_to_file:
		# 写入到文件
		if path and not os.path.exists(os.path.dirname(path)):
			os.mkdir(os.path.dirname(path))

		rotating_handler = RotatingFileHandler(
			path,
			mode='w',
			maxBytes=max_bytes,
			backupCount=file_number,
			encoding=encoding,
		)
		rotating_handler.setFormatter(formatter)
		logger.addHandler(rotating_handler)
	elif write_to_console:
		# 打印到控制台
		loguru_handler = LoggerHandler()
		loguru_handler.setFormatter(formatter)
		logger.addHandler(loguru_handler)
	else:
		stream_handler = logging.StreamHandler()
		stream_handler.stream = sys.stdout
		stream_handler.setFormatter(formatter)
		logger.addHandler(stream_handler)

	return logger


class FLog(object):
	log = None

	def __getattr__(self, item):
		if self.__class__.log is None:
			self.__class__.log = getlogger()
		return getattr(self.__class__.log, item)


log = FLog()
