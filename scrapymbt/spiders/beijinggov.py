import scrapy
from scrapymbt.items import *
import copy
from scrapymbt.process import Value
from fake_useragent import UserAgent


class BeijingfgwSpider(scrapy.Spider):
    name = 'beijinggov'
    allowed_domains = ['beijing.gov.cn']

    def start_requests(self):
        url = 'http://www.beijing.gov.cn/zhengce/zhengcefagui/index.html'
        yield scrapy.Request(url=url, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        next_page_index = response.url[-6]  # 获取本页页码的index
        # 下一页URL
        if next_page_index == 'x':
            next_page_num = 1
            next_page = "http://www.beijing.gov.cn/zhengce/zhengcefagui/index_1.html"
        else:
            next_page_num = int(next_page_index) + 1
            next_page = f"http://www.beijing.gov.cn/zhengce/zhengcefagui/index_{str(next_page_num)}.html"

        rows = response.xpath('//div[@class="listBox"]/ul/li')
        for row in rows:
            created_date = row.xpath('./span/text()').extract_first().strip()

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    title = row.xpath('./a/text()').extract_first().strip()

                    # 若标题包含特定关键字，则进一步解析
                    is_useful = Value(title, self.settings.get('PROVINCE_POLICY_KW')).return_value()
                    if is_useful is not None:
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        url = row.xpath('./a/@href').extract_first()
                        url = 'http://www.beijing.gov.cn/zhengce/zhengcefagui/' + url[2:]
                        item['url'] = url

                        item['title'] = title
                        item['province'] = '北京'

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                 headers={'User-Agent': str(UserAgent().random)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第5页停止
                    if next_page_num < 5:
                        if next_page is not None:
                            yield scrapy.Request(url=next_page, callback=self.parse,
                                                 headers={'User-Agent': str(UserAgent().random)})

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = '北京市政府'
        item['website_type'] = '政策法规'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="mainText"]/div/p/text()').extract())

        yield item
        # 疑问：虽然xpath一样，但有部分详情页的content为空，而且用requests获取并没有问题
        # 如：http://www.beijing.gov.cn/zhengce/zhengcefagui/202112/t20211207_2554935.html


