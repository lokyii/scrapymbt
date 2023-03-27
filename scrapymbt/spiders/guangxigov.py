import copy
import scrapy
import json

from fake_useragent import UserAgent

from scrapymbt.items import *
from urllib.parse import urlencode


class GuangxigovSpider(scrapy.Spider):
    name = 'guangxigov'
    allowed_domains = ['gxzf.gov.cn']

    def start_requests(self):
        year = self.settings.get('START_DATE')[:4]

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                'index': 'file2-index-alias',
                'type': 'governmentdocuments',
                'pageNumber': '1',
                'pageSize': '10',
                'filter[AVAILABLE]': 'true',
                'filter[fileNum-like]': "",
                'filter[Effectivestate]': "0",
                'filter[fileYear]': year,
                'filter[fileYear-lte]': "",
                'filter[FileName,DOCCONTENT,fileNum-or]': keyword,
                'siteId': '14',
                'filter[SITEID]': '3',
                'orderProperty': "",
                'orderDirection': ""
            }
            url = 'http://www.gxzf.gov.cn/igs/front/search/list.html?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'params': copy.deepcopy(params)})

    def parse(self, response):
        response.body.decode('utf8')
        params = response.meta['params']
        rows = response.json()
        total_no = int(rows['page']['total'])
        if total_no != 0:
            if int(params['pageNumber']) < rows['page']['totalPages']:
                params['pageNumber'] = str(int(params['pageNumber']) + 1)
                url = 'http://www.gxzf.gov.cn/igs/front/search/list.html?' + urlencode(params)
                yield scrapy.FormRequest(url=url, headers={'User-Agent': str(UserAgent().random)},
                                         callback=self.parse, meta={'params': copy.deepcopy(params)})

            for row in rows['page']['content']:
                created_date = row['PUBDATE'][:10]

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row['FileName'].replace('<br/>', '')
                    item['url'] = row['DOCPUBURL']
                    item['keywords'] = params['filter[FileName,DOCCONTENT,fileNum-or]']
                    item['province'] = '广西'
                    item['website'] = '广西自治区政府'
                    item['website_type'] = '政策法规'
                    item['content'] = row['DOCCONTENT'].replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace('\n', '').replace('\u2002', '')

                    yield item

