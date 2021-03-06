# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/27

Desc: 解析启动命令行参数, 并创建对应的爬虫
"""
import argparse

from fastspider.commands.create.create_spider import CreateFastSpider
from fastspider.commands.crawl.run_spider import RunFastSpider


def create():
	parser = argparse.ArgumentParser(description="启动命令参数解析")
	parser.add_argument(
		"-s",
		"--spider",
		nargs="+",
		help="创建爬虫\n"
		     "如 fastspider startspider -s <spider_name> <spider_type> "
		     "spider_type=1     表示创建轻量爬虫LightSpider; "
		     "spider_type=2     分布式海量数据抓取爬虫Spider; ",
		metavar=""
	)

	args = parser.parse_args()

	if args.spider:
		spider_name, *spider_type = args.spider
		if not len(spider_type):
			spider_type = "1"
		elif len(spider_type) == 1:
			spider_type = spider_type[0]
		else:
			raise Exception('spider_type error, must choice "1" "2" ')

		CreateFastSpider().create(spider_name, spider_type)


def crawl():
	# 运行爬虫
	parser = argparse.ArgumentParser(description="启动命令参数解析")
	parser.add_argument(
		"-s",
		"--spider",
		nargs="+",
		help="运行爬虫\n"
		     "如 fastspider crawl -s <spider_path> -c <thread_count>"
		     "spider_path           表示启动的爬虫的路径"
		     "thread_count          表示启动的爬虫线程个数",
		metavar=""
	)
	parser.add_argument(
		"-c",
		"--thread_count",
		nargs="+",
		help="爬虫的线程个数\n"
		     "如 fastspider crawl -s <spider_path> -c <thread_count>"
		     "spider_path           表示启动的爬虫的路径"
		     "thread_count          表示启动的爬虫线程个数",
		metavar=""
	)

	args = parser.parse_args()
	if args.spider:
		spider_path, *spider_params = args.spider
		if len(spider_params):
			raise Exception(
				"spider crawl error, command example fastspider crawl -s <spider_name> -c <thread_count> / fastspider crawl -s <spider_name>")

		thread_count, *spider_params = args.thread_count

		if isinstance(thread_count, str):
			try:
				thread_count = int(thread_count)
			except Exception as e:
				raise Exception("spider thread_count must int type")
			if thread_count > 20:
				raise Exception("spider thread_count must lt 20")

		if len(spider_params):
			raise Exception(
				"spider crawl error, command example fastspider crawl -s <spider_name> -c <thread_count> / fastspider crawl -s <spider_name>")

		# 启动爬虫
		RunFastSpider().run(spider_path, thread_count)
