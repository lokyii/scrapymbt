# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapymbt.items import *
import time
from scrapymbt.process import Value
from scrapymbt.settings import *


class TimePipeline:
    def process_item(self, item, spider):
        if isinstance(item, ScrapymbtItem) or isinstance(item, StandardItem):
            crawl_date = time.strftime('%Y-%m-%d', time.localtime())
            item['crawl_date'] = crawl_date
            return item


# 给在门户网站爬取到的信息添加属性：brand, project, product, province, big_brand, small_brand
# 给政策类资讯添加属性：title_kw, title_kw_num, content_kw, content_kw_num
class TypePipeline:
    def process_item(self, item, spider):
        if spider.name == 'hvacrhome' or spider.name == 'vkhvacr' or spider.name == 'chinaiol' \
                or spider.name == 'hvacjournal' or spider.name == 'idcquan' or spider.name == 'aircon'\
                or spider.name == 'gdct_winxin_pa':
            brand = Value(item['keywords'], BRAND).return_value()
            project = Value(item['keywords'], PROJECT).return_value()
            product = Value(item['keywords'], PRODUCT).return_value()
            province = Value(item['keywords'], PROVINCE).return_value()

            # 若brand/project/product/province为空的话，就继续用title匹配出结果
            if brand is None:
                brand = Value(item['title'], BRAND).return_value()
            if project is None:
                project = Value(item['title'], PROJECT).return_value()
            if product is None:
                product = Value(item['title'], PRODUCT).return_value()
            if province is None:
                province = Value(item['title'], PROVINCE).return_value()

            # 若brand/product/province仍为空的话，就继续用content匹配出结果
            if brand is None:
                brand = Value(item['content'], BRAND).return_value()
            if product is None:
                product = Value(item['content'], PRODUCT).return_value()
            if province is None:
                province = Value(item['content'], PROVINCE).return_value()

            # 先区分出品牌，再区分大品牌和小品牌
            if brand is not None:
                big_brand = Value(brand, BIG_BRAND).return_value()
                small_brand = Value(brand, SMALL_BRAND).return_value()
            else:
                big_brand = None
                small_brand = None

            item['brand'] = brand
            item['big_brand'] = big_brand
            item['small_brand'] = small_brand
            item['project'] = project
            item['product'] = product
            item['province'] = province

        # if spider.name != 'hvacrhome' and spider.name != 'vkhvacr' and spider.name != 'chinaiol' \
        #         and spider.name != 'std' and spider.name != 'hvacjournal' and spider.name != 'idcquan'\
        #         and spider.name != 'aircon' and spider.name != 'gdct_winxin_pa':
        #     title_kw = Value(item['title'], PROVINCE_POLICY_KW).return_multi_kw()
        #     title_kw_num = Value(item['title'], PROVINCE_POLICY_KW).keyword_count()
        #     content_kw = Value(item['content'], PROVINCE_POLICY_KW).return_multi_kw()
        #     content_kw_num = Value(item['content'], PROVINCE_POLICY_KW).keyword_count()
        #
        #     item['title_kw'] = title_kw
        #     item['title_kw_num'] = title_kw_num
        #     item['content_kw'] = content_kw
        #     item['content_kw_num'] = content_kw_num

        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        # 数据库登录
        admin_db = self.client['admin']
        user = 'admin'
        pwd = 'admin888'
        admin_db.authenticate(user, pwd)

        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['info_hub'].update_one({'url': item.get('url')}, {'$set': item}, upsert=True)
        return item

