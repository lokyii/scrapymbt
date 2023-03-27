import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent

from scrapymbt.items import ScrapymbtItem


class TianjingovSpider(scrapy.Spider):
    name = 'tianjingov'
    allowed_domains = ['tj.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE')
        end = self.settings.get('END_DATE')
        time = begin + ',' + end

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        "code": "78778b9ded5140d4984030cf8f469303",
                        "advancedQuery.includesFull": keyword,
                        "advancedQuery.root.keyword": keyword,
                        "pageSize": "10",
                        "searchWord": keyword,
                        "siteId": "34",
                        "sortByFocus": "true",
                        "time": time,
                        "type1": "2407"
            }
            url = 'http://www.tj.gov.cn/igs/front/search.jhtml?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)}, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.json()
        if rows['page']['total'] != '0':
            for row in rows['page']['content']:
                created_date = row['trs_time'][:10]

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row['title'].replace("<em>", "").replace("</em>", "")
                    url = row['url']
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '天津'
                    item['website'] = '天津市政府'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="xlrllt"]/div/div[1]//p//text()').extract())

        yield item


