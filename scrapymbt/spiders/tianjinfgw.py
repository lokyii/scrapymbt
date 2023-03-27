import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class TianjinfgwSpider(scrapy.Spider):
    name = 'tianjinfgw'
    allowed_domains = ['fzgg.tj.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE')
        end = self.settings.get('END_DATE')
        time = begin + ',' + end

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        "code": "cf10197d3aca4978af345f3df5975786",
                        "advancedQuery.includesFull": keyword,
                        "orderBy": "time",
                        "pageSize": "10",
                        "searchWord": "",
                        "siteId": "91",
                        "time": time,
                        "timeOrder": "desc",
                        "type": "2222"
            }
            url = 'http://fzgg.tj.gov.cn/igs/front/search.jhtml?' + urlencode(params)
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
                    item['title'] = row['title'].replace("<em>", "").replace("</em>", "").strip()
                    url = row['url']
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '天津'
                    item['website'] = '天津市发改委'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="xlrllt"]/div/div[1]//p//text()').extract())

        yield item



