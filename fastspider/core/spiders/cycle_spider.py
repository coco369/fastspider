# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/09/02

Desc: fastspider核心代码, 周期循环爬虫cycle_spider
"""
from fastspider.core.base.cycle_base import CycleBase
from fastspider.core.scheduler.scheduler import Scheduler
from fastspider.db.mysql_db import MysqlDB
from fastspider.db.redis_db import RedisDB
from fastspider.utils import tools
from fastspider.utils.logger import log
from fastspider.settings import common


class CycleSpider(CycleBase, Scheduler):

	def __init__(self, task_table, record_table, cycle_interval=1, check_task_interval=5):
		"""
			初始化
		:param cycle_interval: 周期循环执行的时间, 以 1 day天单位, 小时表达为1/24
		:param check_task_interval: 检查爬虫任务的周期时间, 以 1s 秒为单位
		:param _record_table: 爬虫任务执行的批次表
		"""
		super(Scheduler, self).__init__(self, cycle_interval=cycle_interval)

		self._mysql_db = MysqlDB()
		self._redis_db = RedisDB()

		self._task_table = task_table
		self._record_table = record_table
		self._cycle_interval = cycle_interval

		# 间隔周期按 day 计算
		if self._cycle_interval > 1:
			self._data_format = "%Y-%m-%d"
		elif self._cycle_interval < 1 and self._cycle_interval > 1 / 24:
			self._data_format = "%Y-%m-%d %H"
		else:
			self._data_format = "%Y-%m-%d %H:%M"

	def run(self):
		"""
			启动爬虫
		"""
		try:
			if not self._parsers:
				self._parsers.append(self)

			# 创建任务表
			self.create_mission_record_table()

			# 开始启动
			self._start()
			# 判断是否结束
			while True:
				if self.all_thread_is_done():
					self.all_thread_stop()
					break

				# 休息5秒后再次检查爬虫是否还在运行
				tools.sleep_time(5)
		except Exception as e:
			log.error(f"爬虫执行异常, 异常原因: {e}")

	# TODO: 可以触发报警

	def start_monitor_task(self):
		"""
			开启监控任务, 并记录任务的执行情况
		"""
		if not self._parsers:
			self._parsers.append(self)

		self.create_mission_record_table()

		log.debug("开始添加待执行的任务")
		# for parser in self._parsers:
		# 	parser.add_task()

		while True:
			# 先检查mysql中记录表内的任务是否执行完毕

			# 检查redis中是否还有任务
			pass

	def check_task_is_done(self):
		"""
			检查爬虫任务是否执行完毕
		:return True表示执行完毕  False表示还在执行中
		"""
		sql = """select total_count, done_count, date_format(cycle_date, {date_format}) from {table_name} order by id desc limit 1;""".format(
			table_name=self._record_table,
			date_format=self._data_format.replace("%M", "%i")
		)
		result = self._mysql_db.execute(sql)
		if result:
			pass
		else:
			self.init_task_record()

			pass

		return True

	def create_mission_record_table(self):
		sql = f"""select table_name from information_schema.tables where table_name='{self._record_table}';"""
		table = self._mysql_db.find(sql)
		if not table:
			sql = """
				CREATE TABLE {table_name} (
					`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
					`cycle_date` {date} DEFAULT NULL COMMENT '周期执行开始时间',
					`total_count` int(11) DEFAULT NULL COMMENT '任务总数',
					`done_count` int(11) DEFAULT NULL COMMENT '完成数',
					`fail_count` int(11) DEFAULT NULL COMMENT '失败任务数',
					`interval` float(11) DEFAULT NULL COMMENT '批次间隔',
					`interval_unit` varchar(20) DEFAULT NULL COMMENT '批次间隔单位 day, hour',
					`create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '批次开始时间',
					`update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '本条记录更新时间',
					`is_done` int(11) DEFAULT '0' COMMENT '批次是否完成 0 未完成  1 完成',
					PRIMARY KEY (`id`)
					) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
				);
			""".format(table_name=self._record_table, date=self._data_format)
			self._mysql_db.execute(sql)

	def init_task_record(self):
		"""
			插入初始化的任务信息
		"""
		sql = """
			select count(*) from {table_name};
		""".format(table_name=self._task_table)
		task_count = self._mysql_db.find(sql)
		total_task_count = task_count[0][0]

		cycle_date = tools.format_date(self._data_format)

		sql = """
			insert into %s cycle_date, total_count, done_count, fail_count, `interval`, interval_unit, create_time 
			values (%s, %s, %s, %s, %s, %s, CURRENT_TIME);
		""" % (
			self._record_table, cycle_date, total_task_count, 0, 0, self._cycle_interval,
			'day' if self._cycle_interval >= 1 else 'hours'
		)
		affect_row = self._mysql_db.insert(sql)
		if affect_row:

			self.start_spider()

		else:
			log.error("插入任务记录失败")

