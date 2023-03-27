import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class SichuangfgwSpider(scrapy.Spider):
    name = 'sichuangfgw'
    allowed_domains = ['fgw.sc.gov.cn']

    def start_requests(self):
        start_date = self.settings.get('START_DATE') + ' 00:00:00'
        end_date = self.settings.get('END_DATE') + ' 00:00:00'
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        "searchWord": keyword,
                        "column": "%E6%94%BF%E7%AD%96",
                        "wordPlace": "0",
                        "orderBy": "1",
                        "startTime": start_date,
                        "endTime": end_date,
                        "pageSize": "10",
                        "pageNum": "0",
                        "timeStamp": "5",
                        "siteCode": "5100000018",
                        "siteCodes": "",
                        "checkHandle": "1",
                        "strFileType": "%E5%85%A8%E9%83%A8%E6%A0%BC%E5%BC%8F",
                        "sonSiteCode": "",
                        "areaSearchFlag": "1",
                        "secondSearchWords": "",
                        "countKey": " 0",
                        "left_right_index": "0"
            }
            url = 'http://fgw.sc.gov.cn/guestweb4/s?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)},
                                 headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        response.body.decode('utf8')
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="wordGuide Residence-permit"]')
        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('./div[2]/div/p[2]/span/text()').extract_first().strip()

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row.xpath('./div[1]/a/@title').extract_first().strip()
                    url = row.xpath('./div[1]/a/@href').extract_first().strip()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '四川'
                    item['website'] = '四川省发改委'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace(u'\u2002', '')
                                  for i in response.xpath('//*[@id="zoomcon"]/ucapcontent//p//text()').extract())

        yield item


