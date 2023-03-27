import copy
import time
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from scrapymbt.items import ScrapymbtItem


class ShanxigovSpider(scrapy.Spider):
    name = 'shanxigov'
    allowed_domains = ['shanxi.gov.cn']

    # 实例化一个浏览器对象
    def __init__(self, timeout=None, start_date=None, end_date=None, province_policy_kw=None):
        # 继承父类的init方法
        super(ShanxigovSpider, self).__init__()
        self.timeout = timeout
        self.start_date = start_date
        self.end_date = end_date
        self.province_policy_kw = province_policy_kw

        options = webdriver.FirefoxOptions()
        # options.headless = True  # 设置火狐为headless无界面模式
        self.browser = webdriver.Firefox(options=options)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   start_date=crawler.settings.get('START_DATE'),
                   end_date=crawler.settings.get('END_DATE'),
                   province_policy_kw=crawler.settings.get('PROVINCE_POLICY_KW'))

    # 爬虫结束后关闭浏览器
    def spider_closed(self, spider):
        self.browser.quit()

    def start_requests(self):

        # param_list[0]为市政府参数，param_list[1]为市发改委参数
        param_list = [{"configTenantId": "7", "areaCode": ""},
                      {"configTenantId": "85", "areaCode": "500000112"}]
        for keyword in self.province_policy_kw:
            for param in param_list:
                params = {
                    "searchWord": keyword,
                    "tenantId": "7",
                    "configTenantId": param["configTenantId"],
                    "dataTypeId": "10",
                    "pageSize": "10",
                    "orderBy": "time",
                    "searchBy": "all",
                    "beginDateTime": beginDateTime,
                    "endDateTime": endDateTime,
                    "areaCode": param["areaCode"]
                }
                url = 'http://www.cq.gov.cn/cqgovsearch/search.html?' + urlencode(params)
                yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)},
                                     headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.xpath('//*[@id="news_list"]/div[@class="item is-policy"]')

        if rows is not None:
            for row in rows:
                created_date = row.xpath(
                    './div[@class="description"]/div/ul/li[3]/span[3]/text()').extract_first().strip()

                if self.start_date <= created_date <= self.end_date:
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    title = row.xpath('./div[@class="title"]/a/@title').extract_first()
                    item['title'] = title
                    url = row.xpath('./div[@class="title"]/a/@href').extract_first()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '重庆'
                    item['website'] = '重庆市政府'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(
            i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace(u'\u2002', '')
            for i in
            response.xpath('//div[starts-with(@class,"view TRS_UEDITOR trs_paper_default")]//p//text()').extract())

        yield item