import scrapy
from scrapymbt.items import *
from scrapymbt.process import Value
import copy

# 暖通家爬虫
class HvacrhomeSpider(scrapy.Spider):
    name = 'hvacrhome'
    allowed_domains = ['hvacrhome.com']
    # catid=4为暖通家新闻页，catid=8为暖通家产品页
    start_urls = ['https://www.hvacrhome.com/news/list.php?catid=4', 'https://www.hvacrhome.com/news/list.php?catid=8']

    def parse(self, response):
        next_page = response.xpath('//div[@class="pages"]/a[10]/@href').extract_first()  # 下一页URL
        next_page_num = int(next_page.split('=')[-1])  # 下一页的页码
        rows = response.xpath('//div[@class="listbox"]/ul/li')
        for row in rows:
            created_date = row.xpath('./div/div[2]/span/text()').extract_first().strip()

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    url = row.xpath('./div/div[1]/a/@href').extract_first()
                    item['url'] = url
                    title = row.xpath('./div/div[1]/a/text()').extract_first().strip()
                    item['title'] = title
                    keywords = ','.join(i for i in row.xpath('./div/div[2]/div[2]/a/text()').extract())
                    item['keywords'] = keywords
                    item['brand'] = Value(keywords, self.settings.get('BRAND')).return_value()
                    item['project'] = Value(keywords, self.settings.get('PROJECT')).return_value()
                    # 若在关键字中匹配不到产品，再与标题匹配
                    product = Value(keywords, self.settings.get('PRODUCT')).return_value()
                    if product is None:
                        product = Value(title, self.settings.get('PRODUCT')).return_value()

                    item['product'] = product
                    item['province'] = Value(keywords, self.settings.get('PROVINCE')).return_value()
                    item['content_type'] = Value(keywords, self.settings.get('KEYWORD_TAB')).return_value()
                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第50页停止
                    if next_page_num <= 50:
                        if next_page is not None:
                            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = '暖通家' + response.xpath('//*[@class="pos"]/a[2]/text()').extract_first()
        item['website_type'] = '行业门户'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="article"]//text()').extract())

        yield item


# scrapy.requests()仍然有重复内容，需在插入数据库设置防止插入重复数据
