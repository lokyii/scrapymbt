# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapymbtItem(scrapy.Item):
    # define the fields for your item here like:
    # 门户网站咨询和政府政策
    # 列表页
    website = scrapy.Field()  # 网站
    website_type = scrapy.Field()  # 网站类型
    keywords = scrapy.Field()  # 关键字
    title = scrapy.Field()  # 标题
    created_date = scrapy.Field()  # 创建日期

    # 根据关键字分类
    brand = scrapy.Field()  # 品牌，仅在新闻资讯类适用
    big_brand = scrapy.Field() # 大品牌
    small_brand = scrapy.Field() # 小品牌
    project = scrapy.Field()  # 项目
    product = scrapy.Field()  # 产品
    province = scrapy.Field()  # 省份

    # 详细页
    url = scrapy.Field()  # 详细页URL
    content = scrapy.Field()  # 内容

    # 仅用于政策法规类资讯
    # title_kw = scrapy.Field() # 标题含有的多个关键字
    # title_kw_num = scrapy.Field() # 标题含有的关键字个数
    # content_kw = scrapy.Field() # 内容含有的多个关键字
    # content_kw_num = scrapy.Field()  # 内容含有的关键字个数

    crawl_date = scrapy.Field() # 爬取日期


class StandardItem(scrapy.Item):
    # define the fields for your item here like:
    # 国标
    # 列表页
    title = scrapy.Field()  # 国标名
    url = scrapy.Field()  # URL
    status = scrapy.Field()  # 状态
    notice_date = scrapy.Field()  # 下达日期
    publish_date = scrapy.Field()  # 发布日期
    effect_date = scrapy.Field()  # 实施日期
    content = scrapy.Field()  # 内容
    keyword = scrapy.Field()  # 搜索关键词
    website_type = scrapy.Field()  # 网站类型




