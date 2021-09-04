# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 数据库mysqldb
"""
import functools
from typing import List, Dict

import pymysql
from pymysql import cursors

from fastspider.settings.common import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT
from fastspider.utils.logger import log

from dbutils.pooled_db import PooledDB


def retry(func):
	# 重试机制
	@functools.wraps
	def inner(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			log.error(f"查询数据异常, sql: {kwargs.get('sql')}, error: {e}")
		return func(*args, **kwargs)

	return inner


class MysqlDB(object):

	def __init__(self, host=None, port=3306, username=None, password=None, database=None, **kwargs):
		self.host = host if host else MYSQL_HOST
		self.port = port if port else MYSQL_PORT
		self.username = username if username else MYSQL_USERNAME
		self.password = password if password else MYSQL_PASSWORD
		self.database = database if database else MYSQL_DATABASE

		# DBUtils 是一套允许线程化 Python 程序可以安全和有效的访问数据库的模块。使用该模块实现数据库mysql的链接
		try:
			self.connect_pooled_db = PooledDB(
				creator=pymysql,
				host=self.host,
				port=self.port,
				user=self.username,
				password=self.password,
				db=self.database,
				charset="utf8mb4",
				cursorclass=cursors.SSCursor,
				mincached=1,
				maxcached=100,
				maxconnections=100,
				blocking=True,
				ping=7
			)
		except Exception as e:
			log.error(
				f"数据库链接【失败】, 账号信息: username: {self.username}, host: {self.host}, port: {self.port}, database: {self.database}, 详细失败原因: {e}")
		else:
			log.debug(
				f"数据库链接【成功】, 账号信息: username: {self.username}, host: {self.host}, port: {self.port}, database: {self.database}")

	def get_connect(self):
		"""
			获取数据库链接
		:return: 数据库链接对象, 游标
		"""
		conn = self.connect_pooled_db.connection(shareable=False)
		cursor = conn.cursor()
		return conn, cursor

	def close(self, conn, cursor):
		"""
			关闭数据库链接
		:param conn: 数据库链接对象
		:param cursor: 游标
		"""
		conn.close()
		cursor.close()

	# 封装方法
	@retry
	def find(self, sql, limit=0):
		"""
			查询数据
		:param sql:  查询sql语句
		:param limit:  限制查询的结果, 0表示查询所有数据 1表示查询1条数据 其他值表示查询指定条数数据
		:return:
		"""
		conn, cursor = self.get_connect()
		cursor.execute(sql)
		if limit == 0:
			result = cursor.fetchall()
		elif limit == 1:
			result = cursor.fetchone()
		else:
			result = cursor.fetchmany(limit)

		self.close(conn, cursor)
		return result

	def insert(self, sql):
		"""
			插入数据
		:param sql: 插入sql语句
		:return: 插入数据成功后, 受影响的条数
		"""
		affect_rows = None
		try:
			conn, cursor = self.get_connect()
			affect_rows = cursor.execute(sql)
			conn.commit()
		except Exception as e:
			log.error(f"插入数据失败, sql: {sql}， error: {e}")
		finally:
			self.close(conn, cursor)

		return affect_rows

	def insert_many(self, sql, data: List[Dict]):
		"""
			批量插入数据, 性能比insert强
		:param sql: sql语句模板。如 insert into table (files1, fields2, files3....) values (value1, value2, value3....)
		:param data: 插入的数据。如[{1,2,3}, {4,5,6} .... ]
		:return: 插入数据成功后, 受影响的条数
		"""
		affect_rows = None
		try:
			conn, cursor = self.get_connect()
			affect_rows = cursor.executemany(sql, data)
			conn.commit()
		except Exception as e:
			log.error(f"批量插入数据失败, sql: {sql}， error: {e}")
		finally:
			self.close(conn, cursor)

		return affect_rows

	def update(self, sql):
		"""
			更新数据
		:param sql: 更新sql语句
		:return: True表示更新成功  False表示更新失败
		"""
		try:
			conn, cursor = self.get_connect()
			cursor.execute(sql)
			conn.commit()
		except Exception as e:
			log.error(f"更新数据失败, sql: {sql}， error: {e}")
			return False
		else:
			return True
		finally:
			self.close(conn, cursor)

	def delete(self, sql):
		"""
			删除数据
		:param sql: 删除sql语句
		:return: True表示更新成功  False表示更新失败
		"""
		try:
			conn, cursor = self.get_connect()
			cursor.execute(sql)
			conn.commit()
		except Exception as e:
			log.error(f"更新数据失败, sql: {sql}, error: {e}")
			return False
		else:
			return True
		finally:
			self.close(conn, cursor)

	def execute(self, sql):
		"""
			执行sql
		:param sql: sql语句
		:return: True表示更新成功  False表示更新失败
		"""
		try:
			conn, cursor = self.get_connect()
			cursor.execute(sql)
			conn.commit()
		except Exception as e:
			log.error(f"执行sql语句失败, sql: {sql}， error: {e}")
			return False
		else:
			return True
		finally:
			self.close(conn, cursor)