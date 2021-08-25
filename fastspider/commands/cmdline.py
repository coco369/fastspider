# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/27

Desc: 解析启动命令行参数, 并创建对应的爬虫
"""
import os
import sys

from fastspider.commands import create_builder


def _print_command_desc():
	version = ""
	with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "VERSION"), "rb") as f:
		version = f.read().decode().strip()
	print(f"fastspider Version: {version} \n")
	print(f"Usage:")
	print(f"  fastspider <command> [options] [args] \n")

	print(f"Available commands:")
	print(f"  startproject        create project")
	print(f"  startspider         create spider \n")

	print(f"Run spider commands")
	print(f"  crawl               run spider")

	print(f'Use "fastspider <command> -h to see more info about a command')


def execute():
	"""
		解析命令行参数
	"""
	argv = sys.argv
	if len(argv) < 4:
		_print_command_desc()
		return

	command = argv.pop(1)
	if command == "startproject":
		# TODO 创建project项目
		pass
	elif command == "startspider":
		create_builder.create()
	elif command == "crawl":
		create_builder.crawl()
	else:
		_print_command_desc()



