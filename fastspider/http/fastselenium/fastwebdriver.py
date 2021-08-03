# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/03

Desc: fastspider核心代码, 封装webdriver
"""
import threading
from queue import Queue

from selenium.webdriver.chrome.webdriver import WebDriver

from fastspider.http import user_agent
from fastspider.settings import common

from selenium import webdriver

from fastspider.utils.tools import Singleton


class WebDriver(WebDriver):
	# TODO: 2021/08/03 目前暂时只支持Chrome
	CHROME = "Chrome"

	def __init__(self, driver_type=CHROME, load_images=True, user_agent=None, proxies=None, timeout=30,
	             windows_size=(1024, 800), executable_path=None, headless=None, **kwargs):
		
		super(WebDriver, self).__init__()

		self._driver_type = driver_type
		self._load_images = load_images
		self._user_agent = user_agent
		self._proxies = proxies
		self._timeout = timeout
		self._window_size = windows_size
		self._executable_path = executable_path
		self._headless = headless

		if self._driver_type == WebDriver.CHROME:
			self.driver = self.chrome_driver()

	def chrome_driver(self):
		"""
			获取chrome浏览器对象
		:return: 浏览器对象
		"""
		options = webdriver.ChromeOptions()
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option("useAutomationExtension", False)

		# 加载图片设置
		if self._load_images:
			prefs = {"profile.default_content_settings.images": 2}
			options.add_experimental_option("prefs", prefs)

		# user-agent设置
		if not self._user_agent:
			random_user_agent = user_agent.get_ua(common.USER_AGENT_TYPE)
			options.add_argument(f"user-agent={random_user_agent}")
		else:
			options.add_argument(f"user-agent={self._user_agent}")

		# 代理proxies设置
		if self._proxies:
			options.add_argument(f"--proxy-server={self._proxies}")

		# 无头模式设置
		if self._headless:
			options.add_argument("--headless")

		# 浏览器窗口大小设置
		if self._window_size:
			options.add_argument(f"--window-size={self._window_size[0]},{self._window_size[1]}")

		# 是否指定webdriver.exe的路径设置
		if self._executable_path:
			driver = webdriver.Chrome(chrome_options=options, executable_path=self._executable_path)
		else:
			driver = webdriver.Chrome(chrome_options=options)
		# execute_cdp_cmd 通过调用DevTools来调试
		# 模拟浏览器访问被识别, 应对方案如下
		driver.execute_cdp_cmd(
			"Page.addScriptToEvaluateOnNewDocument",
			{
				"source": """
	                Object.defineProperty(navigator, 'webdriver', {
	                    get: () => undefined
	                })
                """
			},
		)
		return driver


@Singleton
class WebDriverPool(object):
	"""
		webdriver池
	"""

	def __init__(self, pool_count=1, **kwargs):
		self.pool_count = pool_count
		self.queue = Queue(maxsize=self.pool_count)
		self.kwargs = kwargs
		# 多重锁, RLock允许在同一线程中被多次acquire, acquire和release必须成对出现
		self.thread_lock = threading.RLock()
		self.queue_count = 1

	def get(self):
		"""
		:return: 获取浏览器deiver对象
		"""
		# TODO: queue中为什么需要5个driver对象
		while self.queue_count <= self.queue.maxsize:
			with self.thread_lock:
				driver = WebDriver(**self.kwargs)
				self.queue.put(driver)
				self.queue_count += 1

		driver = self.queue.get()
		return driver

	def put(self, driver):
		self.queue.put(driver)

	def remove(self, driver):
		driver.close()
		self.queue_count -= 1
