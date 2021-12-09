# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapymbtItem(scrapy.Item):
    # define the fields for your item here like:
    # 列表页
    website = scrapy.Field()  # 网站
    website_type = scrapy.Field()  # 网站类型
    keywords = scrapy.Field()  # 关键字
    title = scrapy.Field()  # 标题
    created_date = scrapy.Field()  # 创建日期

    # 根据关键字分类
    brand = scrapy.Field()  # 品牌，仅在新闻资讯类适用
    project = scrapy.Field()  # 项目
    product = scrapy.Field()  # 产品
    province = scrapy.Field()  # 省份
    content_type = scrapy.Field()  # 内容分类

    # 详细页
    url = scrapy.Field()  # 详细页URL
    content = scrapy.Field()  # 内容

    crawl_date = scrapy.Field() # 爬取日期




