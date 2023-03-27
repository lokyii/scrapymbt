import copy
import re
import scrapy
import json
from fake_useragent import UserAgent
from lxml import html

from scrapymbt.items import *


class ZhejianggovSpider(scrapy.Spider):
    name = 'zhejianggov'
    allowed_domains = ['zj.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE').replace('-', '')
        end = self.settings.get('END_DATE').replace('-', '')
        # param_list[0]为省政府请求参数，param_list[1]为省发改委请求参数
        param_list = [{"websiteid": "330000000000000", "tpl": "1569", "cateid": "372"},
                      {"websiteid": "330000000000005", "tpl": "2330", "cateid": "370"}]

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            for param in param_list:
                formdata = {
                    "websiteid": param["websiteid"],
                    "pg": "10",
                    "p": "1",
                    "tpl": param["tpl"],
                    "cateid": param["cateid"],
                    "word": keyword,
                    "checkError": "1",
                    "isContains": "1",
                    "q": keyword,
                    "begin": begin,
                    "end": end,
                    "timetype": "5",
                    "sortType": "2"
                }

                url = 'http://search.zj.gov.cn/jsearchfront/interfaces/cateSearch.do'
                yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                         meta={'formdata': copy.deepcopy(formdata)})

    def parse(self, response):
        formdata = response.meta['formdata']
        result = response.json()
        rows = result['result']
        total_no = result['total']

        if total_no is not None:
            if total_no > 10:
                if total_no % 10 == 0:
                    page_num = total_no % 10
                else:
                    page_num = (total_no % 10) + 1

                if int(formdata['p']) < page_num:
                    formdata['p'] = str(int(formdata['p']) + 1)
                    yield scrapy.FormRequest(url='http://search.zj.gov.cn/jsearchfront/interfaces/cateSearch.do',
                                             formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                             callback=self.parse, meta={'formdata': copy.deepcopy(formdata)})

        if rows is not None:
            for row in rows:
                selector = html.etree.HTML(row)
                created_date = selector.xpath('.//div[@class="sourceTime"]/span[2]/text()')[0][3:]
                url_text = selector.xpath('.//div[@class="newsDescribe"]/a/@href')[0]
                pattern = '.*url=(.*)&q=.*'
                url = re.match(pattern, url_text).group(1).replace('%2F', '/').replace('%3A', ':')
                title = ''.join(i.strip().replace('\r', '').replace('\n', '').replace('\u200b', '').replace(" ", "")
                                for i in selector.xpath('.//div[@class="titleWrapper"]/a/text()'))
                source = selector.xpath('.//div[@class="sourceTime"]/span[1]/text()')[0][3:6]

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE') and source == '浙江省':
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    item['title'] = title
                    item['url'] = url
                    item['keywords'] = formdata['word']
                    item['province'] = '浙江'
                    item['website'] = '浙江省政府'
                    item['website_type'] = '政策法规'

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="zoom"]//p//text()|//div[@class="article-conter"]//p//text()').extract())

        yield item

        # url = 'http://www.zj.gov.cn/art/2021/12/7/art_1229019364_2378478.html' 获取不了内容