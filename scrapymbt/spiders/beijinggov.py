from urllib.parse import urlencode
import scrapy
from scrapy import signals
from scrapy import Spider
from scrapymbt.items import *
import copy
from scrapymbt.process import Value
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class BeijinggovSpider(scrapy.Spider):
    name = 'beijinggov'
    allowed_domains = ['beijing.gov.cn']

    # 实例化一个浏览器对象
    def __init__(self, timeout=None, start_date=None, end_date=None, province_policy_kw=None):
        # 继承父类的init方法
        super(BeijinggovSpider, self).__init__()
        self.timeout = timeout
        self.start_date = start_date
        self.end_date = end_date
        self.province_policy_kw = province_policy_kw

        options = webdriver.FirefoxOptions()
        options.headless = True  # 设置火狐为headless无界面模式
        self.browser = webdriver.Firefox(options=options)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   start_date=crawler.settings.get('START_DATE'),
                   end_date=crawler.settings.get('END_DATE'),
                   province_policy_kw=crawler.settings.get('PROVINCE_POLICY_KW'))
        # spider = super(BeijinggovSpider, cls).from_crawler(crawler, *args, **kwargs)
        # crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        # return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
        #            start_date=crawler.settings.get('START_DATE'),
        #            end_date=crawler.settings.get('END_DATE'),
        #            province_policy_kw=crawler.settings.get('PROVINCE_POLICY_KW')), spider

    # 爬虫结束后关闭浏览器
    def spider_closed(self, spider):
        self.browser.quit()

    def start_requests(self):
        # tab_list[0]为市政府参数，tab_list[1]为市级部门参数
        tab_list = ["zcfg", "ssbm"]
        for keyword in self.province_policy_kw:
            for tab in tab_list:
                params = {
                                "tab": tab,
                                "siteCode": "1100000088",
                                "qt": keyword
                        }
                url = 'http://www.beijing.gov.cn/so/s?' + urlencode(params)
                yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)},
                                     headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.xpath('//*[@id="results"]/div')

        if rows is not None:
            for row in rows:
                # 前者为市政府路径，后者为市发改委
                if response.url[:39] == 'http://www.beijing.gov.cn/so/s?tab=zcfg':
                    created_date = row.xpath('.//div[@class="content"]/div//text()').extract_first().strip()[-10:]
                if response.url[:39] == 'http://www.beijing.gov.cn/so/s?tab=ssbm':
                    created_date = row.xpath('.//div[@class="content"]/div[2]//text()').extract_first().strip()[-10:]

                if self.start_date <= created_date <= self.end_date:
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    title = row.xpath('.//div[@class="title"]/a/@title').extract_first()
                    item['title'] = title
                    url = row.xpath('.//div[@class="title"]/a/@href').extract_first()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '北京'
                    item['website'] = '北京市政府'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="mainText"]/div//p//text()|//div[@class="xl_content"]/div//p//text()').extract())

        yield item

    # 疑问：虽然xpath一样，但有部分详情页的content为空，而且用requests获取并没有问题
    # 如：http://www.beijing.gov.cn/zhengce/zhengcefagui/202112/t20211207_2554935.html



