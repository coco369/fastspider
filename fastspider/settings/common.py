# encoding=utf-8
"""
Auth: coco369
Email: 779598160@qq.com

CreateTime: 2021/07/29

Desc: 配置文件
"""

# 爬虫配置

SPIDER_THREAD_COUNT = 1  # 爬虫并发数

# request网络请求超时时间
REQUEST_TIMEOUT = 22  # 等待服务器响应的超时时间，浮点数，或(connect timeout, read timeout)元组

# UserAgent类型 支持 'chrome', 'opera', 'firefox', 'internetexplorer', 'safari'，若不指定则随机类型
USER_AGENT_TYPE = "chrome"

# requests 使用session
USE_SESSION = False

# 下载时间间隔 单位秒。
# 支持格式, 如 SPIDER_SLEEP_TIME = 3
# 如 SPIDER_SLEEP_TIME = [2, 5] 或者 (2, 5) 则间隔为 2~5秒之间的随机数，包含2和5
SPIDER_SLEEP_TIME = (
	0
)

# 是否开启代理
PROXY_ENABLE = True
# 是否使用隧道代理
PROXY_TUNNEL_HOST = None
PROXY_TUNNEL_PORT = None
PROXY_TUNNEL_USER = None
PROXY_TUNNEL_PASSWORD = None

# 浏览器渲染
WEBDRIVER = dict(
	not_load_images=True,  # 是否加载图片
	user_agent=None,  # 字符串 或 无参函数，返回值为user_agent
	proxies=None,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
	headless=False,  # 是否为无头浏览器
	driver_type="Chrome",  # CHROME、PHANTOMJS、FIREFOX
	timeout=30,  # 请求超时时间
	window_size=(1024, 800),  # 窗口大小
)

# 数据入库的pipeline，可自定义，默认RedisPipeline
ITEM_PIPELINES = [
	# "fastspider.pipeline.test.TmallCheapPipeline"
	# "fastspider.pipeline.redis_pipeline.RedisPipeline",
	# "fastspider.pipeline.mysql_pipeline.MysqlPipeline",
	# "fastspider.pipeline.mongo_pipeline.MongoPipeline",
]

# 日志配置
LOGGER = dict(
	# LOG_IS_WRITE_TO_CONSOLE=True,  # 是否打印到控制台
	# LOG_NAME=os.path.basename(os.getcwd()),
	# LOG_PATH="log/%s.log",  # log存储路径
	# LOG_LEVEL="DEBUG",
	# LOG_IS_WRITE_TO_FILE=True,  # 是否保存到文件中
	# LOG_MAX_BYTES=10 * 1024 * 1024,  # 每个日志文件的最大字节数
	# LOG_FILE_MAX_NUMBER=10,  # 最大备份文件个数
	# LOG_ENCODING="utf8",  # 日志文件编码
)

# 【必填项】 REDIS
REDISDB_URL = ""
REDISDB_IP = "127.0.0.1"
REDISDB_PORT = 6379
REDISDB_USER_PASS = ""
# 默认 0 到 15 共16个数据库
REDISDB_DB = 1
# 心跳检测的数据缓存的时间，以秒为单位
REDISDB_TIME = 5

# 导入自定义settings的配置文件
try:
	from settings import *
except Exception as e:
	pass
