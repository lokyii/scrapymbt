import copy
import scrapy
import json
from scrapymbt.items import *
from urllib.parse import urlencode

class HubeigovSpider(scrapy.Spider):
    name = 'hubeigov'
    allowed_domains = ['hobei.gov.cn']

    def start_requests(self):
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                'index': 'hb-govdoc',
                'type': 'govdoc',
                'pageNumber': 1,
                'pageSize': 10,
                'filter[AVAILABLE]': True,
                'filter[fileYear]': 2022,
                'filter[FileName,DOCCONTENT,fileNum-or]': keyword,
                'siteId': 50,
                'filter[SITEID]': 54,
                'orderProperty': 'PUBDATE',
                'orderDirection': 'desc'
            }
            url = 'https://www.hubei.gov.cn/igs/front/search/list.html?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.json()
        if rows['page']['content'] is not None:
            for row in rows['page']['content']:
                created_date = row['PUBDATE'][:10]

                if created_date >= self.settings.get('START_DATE') <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row['FileName']
                    item['url'] = row['DOCPUBURL']
                    item['keywords'] = keyword
                    item['website'] = '湖北省政府'
                    item['website_type'] = '政策法规'
                    item['content'] = row['DOCCONTENT'].replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace('\n', '')

                    yield item


