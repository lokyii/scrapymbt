import scrapy
from urllib.parse import urlencode
from scrapymbt.settings import *
from scrapymbt.items import *
import copy


#  中国政府采购网
class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['ccgp.gov.cn']

    def start_requests(self):
        base_url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=2'
        start_date = self.settings.get('START_DATE').replace('-', ':')
        end_date = self.settings.get('END_DATE').replace('-', ':')
        page_num = 1

        headers = {
            'Host': 'search.ccgp.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/83.0.4103.106 Safari/537.36'
        }

        cookies = [{
                    "Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd": "1637118745",
                    "Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1637047042",
                    "Hm_lvt_9459d8c503dd3c37b526898ff5aacadd": "1635822828,1635920317,1637047056",
                    "Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5": "1635822814,1637047026",
                    "JSESSIONID": "xf8r4ZVTIVInZTwuqj_jBEy10QPoJbnSnw4Q9jeCBjVkF8k1uWSD!-659192651",
                    "td_cookie": "3076853793",
                    "domain": "ccgp.gov.cn"

        }]

        for keyword in BID_KW:
            params = {
                'searchtype': '2',
                'page_index': page_num,
                'bidSort': '0',
                'pinMu': '0',
                'bidType': '7',
                'kw': keyword,
                'start_time': start_date,
                'end_time': end_date,
                'timeType': '6'
            }
            params = urlencode(params)
            url = base_url + params

            yield scrapy.Request(url, headers=headers, cookies=cookies, meta={'keyword': keyword})

    def parse(self, response):
        keyword = response.meta.get('keyword')
        response.encoding = "utf8"
        rows = response.xpath('//ul[@class="vT-srch-result-list-bid"]/li')  /html/body/div[5]/div[2]/div/div/div[1]/ul
        for row in rows:
            item = ScrapymbtItem()
            item['created_date'] = row.xpath('./div/div[2]/span/text()').extract_first().strip()

            url = row.xpath('./li/a/@href').extract_first()
            item['url'] = url
            title = row.xpath('./li/a/text()').extract_first().strip()
            item['title'] = title
            keywords = ','.join(i for i in row.xpath('./div/div[2]/div[2]/a/text()').extract())
            item['keywords'] = keyword


            item['province'] = Value(keywords, self.settings.get('PROVINCE')).return_value()
            item['content_type'] = Value(keywords, self.settings.get('KEYWORD_TAB')).return_value()
            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = '中国政府采购网'
        item['website_type'] = '中标公告'
        item['content'] = ' '.join(i.strip().replace('\r', '').replace('\u3000', '')
                                   for i in response.xpath('//*[@class="vF_detail_content"]/'
                                                           'div[@class= "Section0"]//text()').extract())



        yield item
