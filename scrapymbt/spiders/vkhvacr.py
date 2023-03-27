import scrapy
from scrapymbt.items import *
import copy


class VkhvacrSpider(scrapy.Spider):
    name = 'vkhvacr'
    allowed_domains = ['vkhvacr.com']
    start_urls = ['http://www.vkhvacr.com/c/hotpump.html?page=1']

    def parse(self, response):
        page_num = int(response.url.split('=')[1])
        rows = response.xpath('//div[@class="article-content"]/div[@class="article-item re"]')
        for row in rows:
            created_date = row.xpath('./div[3]/div/div[2]/text()').extract_first().strip()

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    url = 'http://www.vkhvacr.com' + row.xpath('./div[3]/a[1]/@href').extract_first()
                    item['url'] = url
                    title = row.xpath('./div[3]/a[1]/text()').extract_first().strip()
                    item['title'] = title
                    keywords = row.xpath('./div[3]/div/div[1]/span[2]/a/span/text()').extract_first()
                    item['keywords'] = keywords

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         dont_filter=True)
                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第10页停止
                    if page_num <= 10:
                        next_page = f'http://www.vkhvacr.com/c/hotpump.html?page={page_num + 1}'
                        yield scrapy.Request(next_page)
            else:
                break

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = 'V客暖通网热泵'
        item['website_type'] = '行业门户'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="w-68 left"]/div[@class="content"]/p/text()').extract())

        yield item

