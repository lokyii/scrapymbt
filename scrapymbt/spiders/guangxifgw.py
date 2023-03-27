import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class GuangxifgwSpider(scrapy.Spider):
    name = 'guangxifgw'
    allowed_domains = ['fgw.gxzf.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE')
        end = self.settings.get('END_DATE')
        time = begin + ',' + end

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                        "timeOrder": "desc",
                        "code": "ca9582b3d498473c90215e777b8ad339",
                        "orderBy": "time",
                        "pageSize": "10",
                        "time": time,
                        "pageNumber": "1",
                        "sortByFocus": "true",
                        "siteId": "89",
                        "sitename": "自治区发展改革委",
                        "sitetype": "自治区部门",
                        "name": "自治区发展改革委",
                        "siteclass": "发展和改革",
                        "searchWord": keyword
            }
            url = 'http://fgw.gxzf.gov.cn/igs/front/search.jhtml?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)}, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.json()
        if rows['page']['total'] != '0':
            for row in rows['page']['content']:
                # 发布日期有2个：trs_time和PUBDATE
                if 'trs_time' in row:
                    created_date = row['trs_time'][:10]
                if 'PUBDATE' in row:
                    created_date = row['PUBDATE'][:10]

                if 'title' in row:
                    title = row['title'].replace("<em>", "").replace("</em>", "").replace(" ", "")
                if 'DOCTITLE' in row:
                    title = row['DOCTITLE'].replace("<em>", "").replace("</em>", "").replace(" ", "")

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = title
                    url = row['url']
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '广西'
                    item['website'] = '广西自治区发改委'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace(u'\u2002', '')
                                  for i in response.xpath('//div[@class="article-con"]/div[1]//p//text()').extract())

        yield item

