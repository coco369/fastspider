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

	def __init__(self, cycle_interval=1):
		super(Scheduler, self).__init__(self, cycle_interval=cycle_interval)

		self._mysql_db = MysqlDB()
		self._redis_db = RedisDB()

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

			tools.sleep_time(1)

	# 清理redis表中的数据

	def start_monitor_task(self):
		"""
			开启监控任务, 并记录任务的执行情况
		"""
		if not self._parsers:
			self._parsers.append(self)

		self.create_mission_record_table()


		log.debug("开始下发任务")


	def create_mission_record_table(self):
		sql = f"""select table_name from information_schema.tables where table_name='{common.MYSQL_RECORD_TABLE}';"""
		table = self._mysql_db.find(sql)
		if not table:
			sql = """
				CREATE TABLE {table_name} (
					`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
					`batch_date` {date} DEFAULT NULL COMMENT '批次时间',
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
			""".format(table_name=common.MYSQL_RECORD_TABLE, date=self._data_format)
			self._mysql_db.execute(sql)
