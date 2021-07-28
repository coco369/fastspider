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

packages = setuptools.find_packages()
packages.extend(
	[
		"fastspider",
		"fastspider.templates",
		"fastspider.templates.project",
		"fastspider.templates.spiders",
	]
)


setuptools.setup(
	name="fastspider",
	packages=packages,
	version=version,
	description="fastspider 爬虫框架",
	long_description=readme,
	author="wanghaifei",
	author_email="wanghaifei36@126.com",
	url="https://github.com/coco369/fastspider.git",
	python_requires=">=3.6",
	install_requires=all_requires,
	entry_points={"console_scripts": ["fastspider=fastspider.start:main"]},
	classifiers=["Programming Language :: Python :: 3"],
)
