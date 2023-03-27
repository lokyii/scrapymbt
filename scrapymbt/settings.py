# Scrapy settings for scrapymbt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import time

BOT_NAME = 'scrapymbt'

SPIDER_MODULES = ['scrapymbt.spiders']
NEWSPIDER_MODULE = 'scrapymbt.spiders'

COMMANDS_MODULE = 'scrapymbt.commands'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapymbt (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# log日志输出保存到log文件中
# LOG_ENCODING = 'UTF-8'
# LOG_LEVEL = 'DEBUG'
# log_file_path = 'log/scrapymbt_log_{time}.log'.format(time=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
# LOG_FILE = log_file_path


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapymbt.middlewares.ScrapymbtSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'scrapymbt.middlewares.SeleniumDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapymbt.pipelines.TimePipeline': 300,
    'scrapymbt.pipelines.TypePipeline': 301,
    'scrapymbt.pipelines.MongoPipeline': 302
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# START_DATE = '2022-01-01'
# END_DATE = '2022-01-31'

import datetime
def get_last_month_start_end():
    """
    获取上月第一天和最后一天并返回(元组)
    example:
        now date:2020-03-06
        return:2020-02-01,2020-02-29
    :return: 字符串
    """
    today = datetime.date.today()
    last_day_of_last_month = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
    first_day_of_last_month = datetime.date(last_day_of_last_month.year, last_day_of_last_month.month, 1)
    last_day_of_last_month = datetime.datetime.strftime(last_day_of_last_month, '%Y-%m-%d')
    first_day_of_last_month = datetime.datetime.strftime(first_day_of_last_month, '%Y-%m-%d')
    return first_day_of_last_month, last_day_of_last_month

START_DATE = get_last_month_start_end()[0]
END_DATE = get_last_month_start_end()[1]


MONGO_URI = 'localhost'
MONGO_DB = 'eurovent'
MONGO_COLLECTION = 'info_hub'

SELENIUM_TIMEOUT = 20

# 新闻资讯类网站分类
BRAND = ["海信日立", "三菱", "美的", "东芝", "大金", "松下", "格力", "海信", "海尔", "日立", "江森自控", "麦克维尔", "艾默生",
         "开利", "顿汉布什", "约克", "丹佛斯", "天加", "美控",
         "盾安", "堃霖", "荣事达", "国祥", "英维克", "积微", "雅士", "远大",
         "汉中精机", "EK", "GCHV", "TCL", "欧博", "申菱", "科龙", "长虹", "热立方", "舒瑞普",
         "A.O.史密斯", "中科福德", "中广欧特斯", '中广电器', "威乐", "海林", "海林自控", "瑞福来", "四季沐歌", "派沃", "曼茨", "瑞福莱",
         "纽恩泰", "荏原", '比泽尔', '富士通', '台佳', '思科', 'EBC', '克莱门特', '碧涞', '埃瓦', '西屋康达', '同方', '欧文托普',
         '光芒新能源', '海悟', '依必安派特', '芬尼克兹', '芬尼', '松井', '天池花雨', '新科', 'Welling', '威灵', '依必安派特',
         '世创电能', '特灵', '正理生能', '万和', '力诺瑞特', '荣事达', '奥斯康', '中际·自然能', '扬子', '依必安派特',
         '太阳雨', '特斯联', '格瑞德', '三星', 'Ecoer', '格兰富', '格瑞', '捷丰', '依米康', '奥利凯', '固舍', '博世', '飞利浦', '湿腾',
         '费诺克斯', '海诺帝', '依玛', '邦登', '利雅路', 'Airwin艾尔文', '森德', '朴勒', 'DRP-JOINT', '奥克斯',
         '万顺买', '雅凯', '贝特', '奈兰', '菲斯曼', '奥利凯', '霍尼韦尔', '阳帆', '美博', '泰恩特', '菲索', '卡乐', '博浪', '三花', '优能',
         '奈固', '曼瑞德', '科希家', '九洲空调', '网筑集团', '迪莫', '小松鼠', '海顿', '羽顺', '昊森', '瑞马', '诺科', '阿诗丹顿',
         '乐卡', "双良", "LG", "喜德瑞", "平欧", '迪艾智控', "生能", '搏力谋', '春田', '绿科', '西派克', '维谛', '华信', '绿泉', '元亨',
         '莱恩', '东元', '博乐', 'LEASY', '澳克莱', '九恒', '源盟', '爱客多', '智博士', '英特', '天普', '威能', '维塔', '哈唯',
         '天舒', '舒适易佰', '豪瓦特', '沃逸', '普瑞思顿', '皇家空调', '欧思丹', '亿利达', '妥思', '沃茨', '日出东方', '正旭', '斯密',
         "必信", '森乐', '百朗', '三尼舒适家', '美意', '阔盛', '斯凯孚', '新沪', '航研', '源牌', '和益节能', '瑞美', '爱赛为', 'JOKA',
         '科斯曼', '苏米德', '博容', '哈思', '为山之', '林内', '施耐德', '柯耐弗', '英华特', '宏宇', '福加', '蒂森', '青鱼', '华天成',
         '埃瑞德', '美埃', '中际热能', '冰轮环境', '布朗', '欧井', '科希曼']

BIG_BRAND = ["海信日立", "三菱", "美的", "东芝", "大金", "松下", "格力", "海信", "海尔", "日立", "江森自控", "麦克维尔", "艾默生",
             "开利", "顿汉布什", "约克", "丹佛斯", "天加", "美控"]

SMALL_BRAND = ["盾安", "堃霖", "荣事达", "国祥", "英维克", "积微", "雅士", "远大",
               "汉中精机", "EK", "GCHV", "TCL", "欧博", "申菱", "科龙", "长虹", "热立方", "舒瑞普",
               "A.O.史密斯", "中科福德", "中广欧特斯", '中广电器', "威乐", "海林", "海林自控", "瑞福来", "四季沐歌", "派沃", "曼茨", "瑞福莱",
               "纽恩泰", "荏原", '比泽尔', '富士通', '台佳', '思科', 'EBC', '克莱门特', '碧涞', '埃瓦', '西屋康达', '同方', '欧文托普',
               '光芒新能源', '海悟', '依必安派特', '芬尼克兹', '芬尼', '松井', '天池花雨', '新科', 'Welling', '威灵', '依必安派特',
               '世创电能', '特灵', '正理生能', '万和', '力诺瑞特', '荣事达', '奥斯康', '中际·自然能', '扬子', '依必安派特',
               '太阳雨', '特斯联', '格瑞德', '三星', 'Ecoer', '格兰富', '格瑞', '捷丰', '依米康', '奥利凯', '固舍', '博世', '飞利浦', '湿腾',
               '费诺克斯', '海诺帝', '依玛', '邦登', '利雅路', 'Airwin艾尔文', '森德', '朴勒', 'DRP-JOINT', '奥克斯',
               '万顺买', '雅凯', '贝特', '奈兰', '菲斯曼', '奥利凯', '霍尼韦尔', '阳帆', '美博', '泰恩特', '菲索', '卡乐', '博浪', '三花', '优能',
               '奈固', '曼瑞德', '科希家', '九洲空调', '网筑集团', '迪莫', '小松鼠', '海顿', '羽顺', '昊森', '瑞马', '诺科', '阿诗丹顿',
               '乐卡', "双良", "LG", "喜德瑞", "平欧", '迪艾智控', '生能', '搏力谋', '春田', '绿科', '西派克', '维谛', '华信', '绿泉', '元亨',
               '莱恩', '东元', '博乐', 'LEASY', '澳克莱', '九恒', '源盟', '爱客多', '智博士', '英特', '天普', '威能', '维塔', '哈唯',
               '天舒', '舒适易佰', '豪瓦特', '沃逸', '普瑞思顿', '皇家空调', '欧思丹', '亿利达', '妥思', '沃茨', '日出东方', '正旭', '斯密',
               '必信', '森乐', '百朗', '三尼舒适家', '美意', '阔盛', '斯凯孚', '新沪', '航研', '源牌', '和益节能', '瑞美', '爱赛为', 'JOKA',
               '科斯曼', '苏米德', '博容', '哈思', '为山之', '林内', '施耐德', '柯耐弗', '英华特', '宏宇', '福加', '蒂森', '青鱼', '华天成',
               '埃瑞德', '美埃', '中际热能', '冰轮环境', '布朗', '欧井', '科希曼']

PROJECT = ["新品", "项目案例", "战略合作", "市场活动", "专卖店", "线下门店", "中标", "招标", "采购", "展会", "房地产"]

PRODUCT = ["压缩机", "离心热泵", "空气源热泵", "地源热泵", "热泵", "两联供", "多联机", "中央空调", "粮食烘干机", "风管机", "地暖机",
           "模块机", "风盘", "天花机", "控制器", "计费系统", "末端", "离心机", "两联供", "制冷剂"]

PROVINCE = ["河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南",
            "广东", "海南", "四川", "贵州", "云南", "陕西 ", "甘肃", "青海", "北京", "天津", "上海", "重庆", "内蒙古", "广西",
            "西藏", "宁夏", "新疆"]

HEBEI = ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水']
SHANXI = ['太原', '大同', '朔州', '忻州', '阳泉', '吕梁', '晋中', '长治', '晋城', '临汾', '运城']
LIAONING = ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛']
JILIN = ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边']
HEILONGJIANG = ['哈尔滨', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆', '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化', '大兴安岭']
JIANGSU = ['南京', '无锡', '徐州', '常州', '苏州', '南通', '连云港', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁']
ZHEJIANG = ['杭州', '宁波', '温州', '绍兴', '湖州', '嘉兴', '金华', '衢州', '台州', '丽水', '舟山']
ANHUI = ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '阜阳', '宿州', '滁州', '六安', '宣城', '池州', '亳州']
FUJIAN = ['福州', '厦门', '漳州', '泉州', '三明', '莆田', '南平', '龙岩', '宁德', '平潭']
JIANGXI = ['南昌', '九江', '上饶', '抚州', '宜春', '吉安', '赣州', '景德镇', '萍乡', '新余', '鹰潭']
SHANDONG = ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照市', '临沂', '德州', '聊城', '滨州', '菏泽']
HENAN = ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '商丘', '周口', '驻马店', '南阳', '信阳', '济源']
HUBEI = ['武汉', '黄石', '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈', '咸宁', '随州', '恩施']
HUNAN = ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西']
GUANGDONG = ['广州', '深圳', '佛山', '东莞', '中山', '珠海', '江门', '肇庆', '惠州', '汕头', '潮州', '揭阳', '汕尾', '湛江', '茂名', '阳江', '云浮', '韶关',
             '清远', '梅州', '河源']
HAINAN = ['海口', '三亚', '三沙', '儋州']
SICHUAN = ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中市',
           '资阳市', '阿坝', '甘孜', '凉山']
GUIZHOU = ['贵阳', '遵义', '六盘水', '安顺', '毕节', '铜仁']
YUNNAN = ['昆明', '曲靖', '玉溪', '昭通', '保山', '丽江', '普洱', '临沧', '德宏', '怒江', '迪庆', '大理', '楚雄', '红河', '文山', '西双版纳']
SHAANXI = ['西安', '宝鸡', '咸阳', '铜川', '渭南', '延安', '榆林', '汉中', '安康', '商洛']
GANSU = ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南']
QINGHAI = ['西宁', '海东']
NEIMENGGU = ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安盟', '锡林郭勒', '阿拉善']
GUANGXI = ['南宁', '柳州', '桂林', '梧州', '北海', '崇左', '来宾', '贺州', '玉林', '百色', '河池', '钦州', '防城港', '贵港']
XIZANG = ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲']
NINGXIA = ['银川', '石嘴山', '吴忠', '固原', '中卫']
XINJIANG = ['乌鲁木齐', '克拉玛依', '吐鲁番', '哈密']

KEYWORD_TAB = ["生态环境部", "住建部", "政府采购", "发改委", "统计局", "国务院", "住房和城乡建设局", "财政部",
               "取暖改造", "制冷剂",
               "绿色建筑", "地热供暖", "建筑碳排放",
               "老旧小区"]

HEATING = ["供热", "采暖", "取暖"]
REPLACE_COAL = ["煤改气", "煤改电"]
SUBSIDY = ["政策补贴", "地方补贴", "补贴", "补助"]
ECO_DATA = ["宏观经济", "最新数据", "经济"]
POLICY = ["政策", "政策支持", "首个", "新增", "方案", "通知", "意见", "十四五", "碳达峰", "法规"]

# 招投标关键字
BID_KW = ["精密空调", "中央空调", "空调", "天花机", "热泵", "末端", "末端空调", "空调维保", "通风系统", "新风系统", "采暖", "煤改电"]

# 政策法规分类
PROVINCE_POLICY_DELETED_KW = ['绿色农业', '农业绿色', '林业绿色', '绿色林业', '商品住宅销售价格', '冰雪运动用品国家标准']

# Helen's version
# PROVINCE_POLICY_KW = ['绿色', '低碳', '零碳', '减碳', '降碳', '碳中和', '碳达峰', '碳减排', '节能', '数据中心',
#                       '煤改', '煤炭清洁', '清洁能源', '采暖', '供暖', '空调', '热水', '新风', '热泵', '补贴',
#                       '商品住宅', '高品质住宅', '高品质商品住宅', '住房',
#                       '国家标准', '国标', '能效']

# Yuqing's version
PROVINCE_POLICY_KW = ['绿色低碳', '减碳', '降碳', '碳中和', '碳减排', '双控', '双碳', '零碳',
                      '煤改', '清洁能源', '能效', '能耗',
                      '节能', '建筑节能', '绿色建筑', '绿色工业', '旧改',
                      '数据中心', '空调', '采暖', '供暖', '制冷', '新风机', '热泵', 'PUE', '精密空调', '机房空调', '热负荷管理',
                      '地热', '制冷剂',
                      '国家标准', '标准', '国标',
                    ]

# 国标关键字
STD_KW = ['空调', '热泵', '新风', '数据中心', '机房', '节能改造', '建筑节能', '能效', '节能', '精密空调', '机房空调', '热负荷管理',
          '多联机', '组合式空调箱']

# 品牌筛选出“生能”难题，假如标题出现“可再生能源”，则品牌辨识为“生能”