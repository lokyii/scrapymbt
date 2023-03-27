from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent

from scrapymbt.items import *
import copy
from scrapymbt.process import Value


# 中央人民政府
class GovSpider(scrapy.Spider):
    name = 'gov'
    allowed_domains = ['gov.cn']

    def start_requests(self):
        year = self.settings.get('START_DATE')[:4]
        month = self.settings.get('START_DATE')[5:7]

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        'q': '',
                        't': 'govall',
                        'advance': 'true',
                        'orpro': keyword,
                        'andpro': '',
                        'notpro': '',
                        'inpro': keyword,
                        'pubmintimeYear': year,
                        'pubmintimeMonth': month,
                        'pubmintimeDay': '',
                        'pubmaxtimeYear': year,
                        'pubmaxtimeMonth': month,
                        'pubmaxtimeDay': '',
                        'searchfield': '',
                        'colid': '',
                        'timetype': 'timeqb',
                        'mintime': '',
                        'maxtime': '',
                        'sort': 'pubtime',
                        'sortType': 1,
                        'nocorrect': ''
            }
            url = 'http://sousuo.gov.cn/s.htm?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="result"]/ul/li')
        next_page_url = response.xpath('//*[@id="snext"]/@href')

        if rows is not None:
            for row in rows:
                created_date = row.xpath('./p[2]/span/text()').extract_first().strip()[5:].replace('.', '-')

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    title = ''.join(i. strip() for i in row.xpath('./h3/a/text()').extract())
                    item['title'] = title
                    url = row.xpath('./h3/a/@href').extract_first()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['website'] = '中央政府'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

        if len(next_page_url) != 0:
            yield scrapy.Request(url=next_page_url.extract_first().strip(), callback=self.parse,
                                 headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')  # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        item = response.meta['item']

        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@class="pages_content"]//p//text()').extract())

        yield item



