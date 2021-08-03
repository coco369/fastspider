# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/08/03

Desc: fastspider核心代码, 封装webdriver
"""

from fastspider.http import user_agent

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class WebDriver(RemoteWebDriver):
	# TODO: 2021/08/03 目前暂时只支持Chrome
	CHROME = "Chrome"

	def __init__(self, driver_type=CHROME, load_images=True, user_agent=None, proxies=None, timeout=30,
	             windows_size=(1024, 800), custom_argument=None, executable_path=None, headless=None, **kwargs):
		self._driver_type = driver_type
		self._load_images = load_images
		self._user_agent = user_agent
		self._proxies = proxies
		self._timeout = timeout
		self._window_size = windows_size
		self._custom_argument = custom_argument
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
		if self._user_agent:
			random_user_agent = user_agent.get_ua()
			options.add_argument(f"user-agent={random_user_agent}")

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
