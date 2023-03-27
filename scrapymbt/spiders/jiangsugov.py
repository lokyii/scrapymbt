import copy
import re
import scrapy
import json
from fake_useragent import UserAgent
from lxml import html
from scrapymbt.items import *

class JiangsugovSpider(scrapy.Spider):
    name = 'jiangsugov'
    allowed_domains = ['jiangsu.gov.cn']

    def start_requests(self):
        begin = self.settings.get('START_DATE').replace('-', '')
        end = self.settings.get('END_DATE').replace('-', '')
        websiteid_list = ["320000000100000", "320000000200000"]  # 前者为省政府，后者为省级部门

        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            for websiteid in websiteid_list:
                formdata = {
                        "websiteid": websiteid,
                        "q": keyword,
                        "p": "1",
                        "pg": "20",
                        "cateid": "29",
                        "pos": "",
                        "pq": "",
                        "oq": "",
                        "eq": "",
                        "begin": begin,
                        "sortType": "0",
                        "end": end,
                        "tpl": "38"
                }

                url = 'http://www.jiangsu.gov.cn/jsearchfront/interfaces/cateSearch.do'
                yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                         meta={'formdata': copy.deepcopy(formdata)})

    def parse(self, response):
        formdata = response.meta['formdata']
        result = response.json()
        if len(result) != 0:  # 若返回空白字典，字典的长度为0
            rows = result['result']
            total_no = result['total']

            if total_no is not None:
                if total_no > 20:
                    if total_no % 20 == 0:
                        page_num = total_no % 20
                    else:
                        page_num = (total_no % 20) + 1

                    if int(formdata['p']) < page_num:
                        formdata['p'] = str(int(formdata['p']) + 1)
                        yield scrapy.FormRequest(url='http://www.jiangsu.gov.cn/jsearchfront/interfaces/cateSearch.do',
                                                 formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                                 callback=self.parse, meta={'formdata': copy.deepcopy(formdata)})

            if rows is not None:
                for row in rows:
                    selector = html.etree.HTML(row)
                    created_date = selector.xpath('.//span[@class="jcse-news-date"]/text()')[0].strip()[-10:]
                    url = selector.xpath('.//div[@class="jcse-news-url"]/a/text()')[0]

                    if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        item['url'] = url
                        item['keywords'] = formdata['q']
                        item['province'] = '江苏'
                        item['website'] = '江苏省政府'
                        item['website_type'] = '政策法规'

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                 headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['title'] = response.xpath('//table[@class="xxgk_table"]/tbody/tr[3]/td[2]//text()|//meta[@name="ArticleTitle"]/@content|/html/body/div[1]/div[5]/div/div[2]/div[2]/text()').extract_first()
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="article_content"]/p//text()|//*[@id="Zoom"]/p//text()|//div[@class="main-txt"]/p//text()').extract())

        yield item

        # 有部分网页的content获取不了 url= 'http://www.jiangsu.gov.cn/art/2021/12/14/art_46144_10191305.html'
