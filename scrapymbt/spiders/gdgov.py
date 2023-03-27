import time
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import *
import copy
from scrapymbt.process import Value


class GdgovSpider(scrapy.Spider):
    name = 'gdgov'
    allowed_domains = ['gd.gov.cn']

    def start_requests(self):
        START_DATE = self.settings.get('START_DATE') + ' 00:00:00'
        END_DATE = self.settings.get('END_DATE') + ' 23:59:59'

        start_date_array = time.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
        time_from = int(time.mktime(start_date_array))
        end_date_array = time.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
        time_to = int(time.mktime(end_date_array))

        # 前者为省政府网站代号，后者为省发改委
        site_id_list = ["2", "135"]
        for site_id in site_id_list:
            for keyword in self.settings.get('PROVINCE_POLICY_KW'):
                formdata = {
                                "gdbsDivision": "440000",
                                "keywords": keyword,
                                "page": "1",
                                "position": "all",
                                "range": "site",
                                "recommand": "1",
                                "service_area": "1",
                                "site_id": site_id,
                                "sort": "time",
                                "time_from": str(time_from),
                                "time_to": str(time_to)
                }

                url = 'https://search.gd.gov.cn/api/search/file'
                yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                         meta={'formdata': copy.deepcopy(formdata)})

    def parse(self, response):
        formdata = response.meta['formdata']
        keyword = formdata["keywords"]
        result = response.json()
        rows = result['data']['list']
        total_no = result['data']['total']

        if total_no != 0:
            if total_no > 20:
                if total_no % 20 == 0:
                    page_num = total_no % 20
                else:
                    page_num = (total_no % 20) + 1

                if int(formdata["page"]) < page_num:
                    formdata["page"] = str(int(formdata["page"]) + 1)
                    yield scrapy.FormRequest(url='https://search.gd.gov.cn/api/search/file',
                                             formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                             callback=self.parse, meta={'formdata': copy.deepcopy(formdata)})

        if len(rows) != 0:
            for row in rows:
                created_date = row['pub_time']
                url = row['url']
                title = row['title'].replace('<em>', '').replace('</em>', '').replace('&mdash;', '-').\
                            replace('&ldquo;', '-').replace('&rdquo;', '-')

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = title
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '广东'
                    item['website'] = '广东省政府'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="article-content"]/p//text()|//div[@class="zw"]/p//text()').extract())

        yield item
