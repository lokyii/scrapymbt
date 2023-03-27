import scrapy
import json
from lxml import etree
from scrapymbt.items import *
import copy
import re

class ChinaiolSpider(scrapy.Spider):
    name = 'chinaiol'
    allowed_domains = ['chinaiol.com']
    start_urls = ['http://webapi.chinaiol.com/api/User/GetChannelMore?chinnelid=21&pageNumber=0',
                  'http://webapi.chinaiol.com/api/User/GetChannelMore?chinnelid=22&pageNumber=0']

    def parse(self, response):
        # response为json
        origin_url = response.url
        pattern = re.compile(r'\d+')
        result = pattern.findall(origin_url)
        channel_id = result[0]
        page_num = result[1]

        text = response.json().get('result').get('contentHtml')
        # html格式化
        text = etree.HTML(text)
        rows = text.xpath('//div[@class="layui-row layui-col-space15 mp15"]')
        count = 0  # 记录该咨询在请求中的序号

        for row in rows:
            title = row.xpath('.//h3[@class="tit"]/a/text()')[0].strip()
            url = 'http://www.chinaiol.com' + row.xpath('.//h3[@class="tit"]/a/@href')[0]
            keywords = ','.join(i for i in row.xpath('.//p[@class="tag"]/a/text()'))

            item = ScrapymbtItem()
            item['title'] = title
            item['url'] = url
            item['keywords'] = keywords

            count = count + 1

            if url is not None:
                yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item),
                                    'page_num': page_num, 'channel_id': channel_id, 'count': count})

    def item_parse(self, response):
        item = response.meta['item']
        page_num = response.meta['page_num']
        channel_id = response.meta['channel_id']
        count = response.meta['count']

        # 若URL分类为21，则为'中央空调'新闻；若URL分类为22，则为'供热采暖'新闻
        if channel_id == '21':
            item['website'] = '产业在线中央空调'
        else:
            item['website'] = '产业在线供热采暖'

        item['website_type'] = '行业门户'
        created_date = response.xpath('//div[@class="tit-detail mt10"]/span[1]/text()').extract_first()
        item['created_date'] = created_date
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="content"]//p//text()').extract())

        if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
            yield item

        # 若count=6，且该条资讯的created_date小于等于START_DATE，则请求下一页
        if count == 6 and created_date >= self.settings.get('START_DATE'):
            page_num = str(int(page_num) + 1)
            next_page = f'http://webapi.chinaiol.com/api/User/GetChannelMore?chinnelid={channel_id}&pageNumber={page_num}'
            yield scrapy.Request(url=next_page, callback=self.parse)


