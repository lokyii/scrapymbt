import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class AnhuigovSpider(scrapy.Spider):
    name = 'anhuigov'
    allowed_domains = ['ah.gov.cn']

    def start_requests(self):
        # 前者为省政府搜索网址，后者为省发改委的
        param_list = [{"view": "政务公开", "dsId": 'www.ah.gov.cn'}, {"view": "信息公开", "dsId": 'fgw.ah.gov.cn'}]
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            for param in param_list:
                params = {
                            "page": "1",
                            "view": param["view"],
                            "dsId": param["dsId"],
                            "dateOrder": "2",
                            "format": "1",
                            "contentScope": "2",
                            "tr": "4",
                            "startDate": "null",
                            "endDate": "null",
                            "includeKeywords": "null",
                            "excludeKeyword": "null",
                            "includeAllKeywords": "null",
                            "compWord": "null",
                            "searchType": "null",
                            "q": keyword

                }
                url = 'https://www.ah.gov.cn/ahso/search?' + urlencode(params)
                yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)},
                                     headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        response.body.decode('utf8')
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="mainResult"]/div[@class="result"]')
        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('./div[2]/div[1]/div/span/text()').extract_first().strip()

                if created_date >= self.settings.get('START_DATE'):
                    if created_date <= self.settings.get('END_DATE'):
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        item['title'] = row.xpath('./div[1]/a/@title').extract_first().strip()
                        url = "https://www.ah.gov.cn/ahso/" + row.xpath('./div[1]/a/@href').extract_first().strip()
                        item['url'] = url
                        item['keywords'] = keyword
                        item['province'] = '安徽'
                        item['website'] = '安徽省政府'
                        item['website_type'] = '政策法规'

                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})
                else:
                    break

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="wzcon j-fontContent"]//p//text()|//div[@class="j-fontContent newscontnet minh300"]/p//text()'
                                                          '|//*[@id="zoom"]//text()|//div[@class="wenzhang_main j-fontContent"]/p//text()').extract())

        yield item

