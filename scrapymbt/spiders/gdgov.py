import scrapy
from scrapymbt.items import *
import copy
from scrapymbt.process import Value


class GdgovSpider(scrapy.Spider):
    name = 'gdgov'
    allowed_domains = ['gd.gov.cn']
    start_urls = ['http://www.gd.gov.cn/zwgk/wjk/qbwj/index.html']

    def parse(self, response):
        next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()  # 下一页URL
        next_page_num = int(next_page[-6])  # 下一页的页码
        rows = response.xpath('//div[@class="viewList"]/ul/li')
        for row in rows:
            created_date = row.xpath('./span[@class="date"]/text()').extract_first().strip()

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    title = row.xpath('./span[@class="name"]/a/text()').extract_first().strip()

                    # 若标题包含特定关键字，则进一步解析
                    is_useful = Value(title, self.settings.get('PROVINCE_POLICY_KW')).return_value()
                    if is_useful is not None:
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        url = row.xpath('./span[@class="name"]/a/@href').extract_first()
                        item['url'] = url
                        item['title'] = title
                        item['province'] = '广东'

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第5页停止
                    if next_page_num < 6:
                        if next_page is not None:
                            yield scrapy.Request(url=next_page, callback=self.parse)

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = '广东省政府'
        item['website_type'] = '政策法规'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="zw"]//text()').extract())

        yield item

