import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class ShanghaifgwSpider(scrapy.Spider):
    name = 'shanghaifgw'
    allowed_domains = ['gov.cn']

    def start_requests(self):
        start_date = self.settings.get('START_DATE')
        end_date = self.settings.get('END_DATE')

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        "q": keyword,
                        "publishStartDate": start_date,
                        "publishEndDate": end_date,
                        "searchType": "fgwSearch",
                        "page": "1",
                        "contentScope": "2",
                        "dateOrder": "2",
                        "tr": "1",
                        "format": "1",
                        "uid": "0000017d-a20b-5fb2-e255-77dd586307b3",
                        "sid": "0000017d-a20b-5fb2-7cc2-30c52f89b3f3",
                        "re": "2",
                        "all": "1",
                        "siteId": "zwgk.fgw.sh.gov.cn"
            }
            url = 'https://ss.shanghai.gov.cn/fgwxxgk/search?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="result "]')

        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('.//div[@class="content"]/font[1]/text()').extract_first().strip()

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row.xpath('./a/@title').extract_first().strip()
                    url = 'https://ss.shanghai.gov.cn' + row.xpath('./a/@href').extract_first()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '上海'
                    item['website'] = '上海市发改委'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')  # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        item = response.meta['item']

        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="ivs_content"]//p//text()').extract())

        yield item




