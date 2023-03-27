import copy
import scrapy
from fake_useragent import UserAgent
from lxml import html
from scrapymbt.items import ScrapymbtItem


class ShandongfgwSpider(scrapy.Spider):
    name = 'shandongfgw'
    allowed_domains = ['fgw.shandong.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE').replace('-', '')
        end = self.settings.get('END_DATE').replace('-', '')

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            formdata = {
                            "websiteid": "370000000087000",
                            "q": keyword,
                            "p": "1",
                            "pg": "20",
                            "cateid": "15598",
                            "pos": "title,content,_default_search",
                            "pq": "",
                            "oq": "",
                            "eq": "[object HTMLInputElement]",
                            "begin": begin,
                            "end": end,
                            "tpl": "452"
            }
            url = 'http://fgw.shandong.gov.cn/jsearchfront/interfaces/cateSearch.do'
            yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                     meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        result = response.json()
        if 'result' in result:
            rows = result['result']
            for row in rows:
                selector = html.etree.HTML(row)
                title = "".join(i.replace("<em>", "").replace("</em>", "") for i in selector.xpath('.//div[@class="jcse-news-title"]/a/text()'))
                url = selector.xpath('.//div[@class="jcse-news-url"]/a/text()')[0]
                created_date = selector.xpath('.//span[@class="jcse-news-date"]/text()')[0]

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = title
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '山东'
                    item['website'] = '山东省发改委'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="art_con"]//p//text()').extract())

        yield item


