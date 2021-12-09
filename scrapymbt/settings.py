# Scrapy settings for scrapymbt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapymbt'

SPIDER_MODULES = ['scrapymbt.spiders']
NEWSPIDER_MODULE = 'scrapymbt.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapymbt (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapymbt.middlewares.ScrapymbtSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapymbt.middlewares.ScrapymbtDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapymbt.pipelines.TimePipeline': 300,
    'scrapymbt.pipelines.MongoPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

START_DATE = '2021-11-01'
END_DATE = '2021-11-30'

MONGO_URI = 'localhost'
MONGO_DB = 'eurovent'
MONGO_COLLECTION = 'info_hub'

gov_kw = ['数据中心', '节能审查', 'PUE', '能源消费', '煤改电', '补贴', '清洁能源', '空调', '热水', '采暖']

# 为新闻资讯类网站分类
BRAND = ["海信日立", "海信", "海尔", "盾安", "天加", "三菱重工海尔", "三菱重工", "荏原", "江森自控日立万宝", "松下", "江森自控", "麦克维尔",
         "美的", "堃霖", "荣事达", "东芝", "国祥", "艾默生", "开利", "大金", "日立", "英维克", "积微", "雅士", "格力", "远大",
         "顿汉布什", "汉中精机", "EK", "GCHV", "TCL", "欧博", "松下", "申菱", "约克", "科龙", "长虹", "热立方", "舒瑞普",
         "A.O.史密斯", "丹佛斯", "中科福德", "中广欧特斯", "威乐", "海林", "海林自控", "瑞福来", "四季沐歌", "派沃", "曼茨", "瑞福莱",
         "纽恩泰"]
PROJECT = ["新品", "项目案例", "战略合作", "市场活动", "专卖店", "线下门店", "中标", "招标", "展会", "房地产"]

PRODUCT = ["压缩机", "离心热泵", "空气源热泵", "地源热泵", "热泵", "两联供", "多联机", "中央空调", "粮食烘干机", "风管机", "地暖机",
           "模块机", "风盘", "天花机", "控制器", "计费系统", "末端", "离心机", "两联供", "制冷剂"]

PROVINCE = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南",
            "广东", "海南", "四川", "贵州", "云南", "陕西 ", "甘肃", "青海", "北京", "天津", "上海", "重庆", "内蒙古", "广西",
            "西藏", "宁夏", "新疆"]

SHANDONG_CITY = ["济南", "青岛", "烟台", "威海", "东营", "淄博", "潍坊", "日照", "莱芜", "菏泽", "枣庄", "德州", "滨州", "临沂",
                 "济宁", "聊城", "泰安"]

KEYWORD_TAB = ["生态环境部", "住建部", "政府采购", "发改委", "统计局", "国务院", "住房和城乡建设局", "财政部",
               "取暖改造", "制冷剂",
               "绿色建筑",  "地热供暖", "建筑碳排放",
               "老旧小区"]

HEATING = ["供热", "采暖", "取暖"]
REPLACE_COAL = ["煤改气", "煤改电"]
SUBSIDY = ["政策补贴", "地方补贴", "补贴", "补助"]
ECO_DATA = ["宏观经济", "最新数据", "经济"]
POLICY = ["政策", "政策支持", "首个", "新增", "方案", "通知", "意见", "十四五", "碳达峰", "法规"]

BID_KW = ["精密空调", "中央空调", "空调", "天花机", "热泵", "末端", "末端空调", "空调维保", "通风系统", "新风系统", "采暖", "煤改电"]



