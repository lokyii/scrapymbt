import scrapy


class MiitSpider(scrapy.Spider):
    name = 'miit'
    allowed_domains = ['miit.gov.cn']
    start_urls = ['http://miit.gov.cn/']

    def parse(self, response):
        pass
