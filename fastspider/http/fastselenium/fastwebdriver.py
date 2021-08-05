# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/03

Desc: fastspider核心代码, 封装webdriver
"""
import threading
from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from fastspider.http import user_agent
from fastspider.settings import common

from fastspider.utils.tools import Singleton


class FastWebDriver(WebDriver):
	# TODO: 2021/08/03 目前暂时只支持Chrome
	CHROME = "Chrome"

	def __init__(self, driver_type=CHROME, not_load_images=True, user_agent=None, proxies=None, timeout=30,
	             windows_size=(1024, 800), executable_path=None, headless=None, **kwargs):

		self._driver_type = driver_type
		self.not_load_images = not_load_images
		self._user_agent = user_agent
		self._proxies = proxies
		self._timeout = timeout
		self._window_size = windows_size
		self._executable_path = executable_path
		self._headless = headless

		if self._driver_type == FastWebDriver.CHROME:
			self.driver = self.chrome_driver()

		# 当网络差get(url)不返回,但也不报错, 设置超时选项来解决程序卡住的问题。
		self.driver.set_page_load_timeout(self._timeout)
		# 设置10秒脚本超时时间
		self.driver.set_script_timeout(self._timeout)

	def chrome_driver(self):
		"""
			获取chrome浏览器对象
		:return: 浏览器对象
		"""
		options = webdriver.ChromeOptions()
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option("useAutomationExtension", False)

		# 加载图片设置
		if self.not_load_images:
			prefs = {"profile.managed_default_content_settings.images": 2}
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
			driver = webdriver.Chrome(options=options, executable_path=self._executable_path)
		else:
			driver = webdriver.Chrome(options=options)
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

	@property
	def cookies(self):
		new_cookies = {}
		for cookie in self.get_cookies():
			new_cookies[cookie["name"]] = cookie["value"]
		return new_cookies

	def __getattr__(self, name):
		"""
			WebDriver启动后, 会生成相应的控制浏览器会话的session_id等参数。
			其父类WebDriver需要使用到session_id等属性, 因此通过当前浏览器对象this.driver将相关session_id等属性获取到, 并作为属性的value值返回
		:param name: 参数
		:return: 返回当前浏览器对象driver的相关属性
		"""
		if self.driver:
			return getattr(self.driver, name)
		else:
			raise AttributeError


@Singleton
class WebDriverPool:
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
				driver = FastWebDriver(**self.kwargs)
				self.queue.put(driver)
				self.queue_count += 1

		driver = self.queue.get()
		return driver

	def put(self, driver):
		self.queue.put(driver)

	def remove(self, driver):
		driver.close()
		self.queue_count -= 1

	def close(self):
		while not self.queue.empty():
			driver = self.queue.get()
			driver.close()
			self.queue_count -= 1
