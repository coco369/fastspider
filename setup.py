# encoding=utf-8

import os

import setuptools

with open(os.path.join(os.path.join(os.path.dirname(__file__), "fastspider"), "VERSION"), "rb") as f:
	version = f.read().decode().strip()

with open("README.md", 'rb') as f:
	readme = f.read().decode().strip()

all_requires = []
with open(os.path.join(os.path.join(os.path.dirname(__file__), "fastspider"), "requirements.txt"), "rb") as f:
	requires = f.readlines()
	for package in requires:
		if package.decode().strip():
			all_requires.append(package.decode().strip())

setuptools.setup(
	name="fastspider",
	version=version,
	author="wanghaifei",
	author_email="wanghaifei36@126.com",
	python_requires=">=3.6",
	description="fastspider 爬虫框架",
	long_description=readme,
	entry_points={"console_scripts": ["fastspider=fastspider.start:main"]},
	url="https://github.com/coco369/fastspider.git",
	install_requires=all_requires,
	packages=setuptools.find_packages(),
	include_package_data=True,
	classifiers=["Programming Language :: Python :: 3"],
)
