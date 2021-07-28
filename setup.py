# encoding=utf-8

import os

import setuptools

with open(os.path.join(os.path.join(os.path.dirname(__file__), "fastspider"), "VERSION"), "rb") as f:
	version = f.read().decode().strip()

with open("README.md", 'rb') as f:
	readme = f.read().decode().strip()

all_requires = []
with open(os.path.join(os.path.join(os.path.dirname(__file__), "fastspider"), "requirments.txt"), "rb") as f:
	requires = f.readlines()
	for package in requires:
		if package.decode().strip():
			all_requires.append(package.decode().strip())

setuptools.setup(
	name="fastspider",
	version=version,
	description="fastspider 爬虫框架",
	long_description=readme,
	author="wanghaifei",
	auth_email="wanghaifei36@126.com",
	url="https://github.com/coco369/fastspider.git",
	python_requires=">=3.6",
	license="",
	install_requires=all_requires,
	entry_points={"console_scripts": ["fastspider = fastspider.commands.cmdline:execute"]},
	classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License"],
)
