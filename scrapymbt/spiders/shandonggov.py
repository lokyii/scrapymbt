import copy
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class ShandonggovSpider(scrapy.Spider):
    name = 'shandonggov'
    allowed_domains = ['shandong.gov.cn']

    # 山东省人民政府-政策文件
    def start_requests(self):
        year = self.settings.get('START_DATE')[:4]

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            params = {
                'vc_name': '',
                'field_1218': keyword,
                'field_1244': '',
                'field_1243': year,
                'field_1222': '',
                'field_1221': '',
                'download': '',
                'strSelectID': '1221, 1222, 1235, 1243, 1244, 1245, 1344',
                'i_columnid': '107851',
                'field': 'vc_name:1:0,field_1218:1:0,field_1222:1:1,field_1243:1:0,field_1244:1:0,field_1245:1:,field_1221:1:0',
                'initKind': 'FieldForm',
                'type': '0, 0, 0, 0, 0, 0',
                'currentplace': '',
                'splitflag': '',
                'fullpath': '0'
            }
            url = 'http://www.shandong.gov.cn/module/search/index.jsp?' + urlencode(params)
            yield scrapy.Request(url=url, meta={'keyword': copy.deepcopy(keyword)}, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        response.body.decode('utf8')
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="wip_col_listul"]/ul/li')
        if len(rows) != 0:
            for row in rows:
                created_date = row.xpath('./span/text()').extract_first().strip()[:10]

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = row.xpath('./a/text()').extract_first().strip()
                    url = 'http://www.shandong.gov.cn/' + row.xpath('./a/@href').extract_first()[6:]
                    item['url'] = url
                    item['keywords'] = keyword
                    item['province'] = '山东'
                    item['website'] = '山东省政府'
                    item['website_type'] = '政策法规'

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="wip_art_con"]//p//text()').extract())

        yield item

        # 同一url_domain搜不同关键词会返回相同URL，所以当存在item的keywords被覆盖的情况
        # content为空的url：http://www.shandong.gov.cn/art/2022/1/20/art_107851_117019.html