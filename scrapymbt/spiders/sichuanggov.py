import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class SichuanggovSpider(scrapy.Spider):
    name = 'sichuanggov'
    allowed_domains = ['sc.gov.cn']

    def start_requests(self):
        # 该网站根据发文年份筛选不能返回结果
        # year = self.settings.get('START_DATE')[:4]

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            # column为政府文件
            params = {
                        "allSearchWord": keyword,
                        "orSearchType": "1",
                        "pageSize": "10",
                        "pageNum": "0",
                        "docName": "",
                        "docYear": "",
                        "docType": "",
                        "siteCode": "5100000062",
                        "siteCodes": "",
                        "wordPlace": "2",
                        "orderBy": "1",
                        "column": "%E6%94%BF%E5%BA%9C%E6%96%87%E4%BB%B6",
                        "countKey": "0",
                        "docNameRight": "",
                        "docTypeRight": "",
                        "docYearRight": "",
                        "areaSearchFlag": "1",
                        "left_right_index": "0"
            }
            url = 'https://www.sc.gov.cn/so4/a?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)}, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        response.body.decode('utf8')
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="wordGuide Residence-permit"]')
        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('.//span[@class="sourceDateFont"]/text()').extract_first().strip()[5:].strip()

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row.xpath('./div[1]/a/text()').extract_first().strip()
                    url = row.xpath('./div[1]/a/@href').extract_first().strip()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '四川'
                    item['website'] = '四川省政府'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//td[@class="black14X STYLE1"]/div//p//text()|//td[@class="contText"]//p//text()').extract())

        yield item