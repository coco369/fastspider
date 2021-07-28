# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2020/07/27

Desc: 解析启动命令行参数, 并创建对应的爬虫
"""
import argparse

from fastspider.commands.create.create_spider import CreateFastSpider


def create():
	parser = argparse.ArgumentParser(description="启动命令参数解析")
	parser.add_argument(
		"-s",
		"--spider",
		nargs="+",
		help="创建爬虫\n"
		     "如 fastspider startspider -s <spider_name> <spider_type> "
		     "spider_type=air       表示创建轻量爬虫AirSpider; "
		     "spider_type=nomal     分布式海量数据抓取爬虫NomalSpider; "
		     "spider_type=cycle     分布式周期性抓取爬虫CycleSpiser; ",
		metavar=""
	)

	args = parser.parse_args()

	if args.spider:
		spider_name, *spider_type = args.spider
		if not len(spider_type):
			spider_type = "air"
		elif len(spider_type) == 1:
			spider_type = spider_type[0]
		else:
			raise Exception('spider_type error, must choice "air" "nomal" "cycle" ')

		CreateFastSpider().create(spider_name, spider_type)
