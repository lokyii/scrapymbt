import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class HunangovSpider(scrapy.Spider):
    name = 'hunangov'
    allowed_domains = ['hunan.gov.cn']

    def start_requests(self):
        # 前者为省政府网站代号，后者为省发改委
        # 为政府文件
        cateid_list = ['001000000', '102000000']
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            for cateid in cateid_list:
                params = {
                    'q': keyword,
                    'searchfields': '',
                    'sm': '1',
                    'columnCN': '',
                    'p': '0',
                    'timetype': 'timeyn'
                }
                url = f'https://searching.hunan.gov.cn/hunan/{cateid}/file?' + urlencode(params)
                yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)}, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        response.body.decode('utf8')
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="boxlist-main"]/div[@class="resultbox"]')
        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('./ul/li[4]/p/text()').extract_first().strip()

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row.xpath('./div/a/@title').extract_first().strip()
                    url = row.xpath('./div/a/@href').extract_first().strip()
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '湖南'
                    item['website'] = '湖南省政府'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="content"]//p//text()|//div[@class="detail-txt"]/p//text()|//div[@class="tys-main-zt-show"]/p//text()').extract())

        yield item