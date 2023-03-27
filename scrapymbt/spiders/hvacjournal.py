import copy
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class HvacjournalSpider(scrapy.Spider):
    name = 'hvacjournal'
    allowed_domains = ['hvacjournal.cn']
    start_urls = ['http://www.hvacjournal.cn/Category_25/Index_1.aspx']

    def parse(self, response):
        rows = response.xpath('//div[@class="listBox"]/li')

        for row in rows:
            if row != rows[5] and row != rows[11] and row != rows[17]:
                created_date = row.xpath('./span/text()').extract_first().strip()

                # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
                if created_date >= self.settings.get('START_DATE'):
                    if created_date <= self.settings.get('END_DATE'):
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        url = 'http://www.hvacjournal.cn' + row.xpath('./a/@href').extract_first().strip()
                        item['url'] = url
                        title = row.xpath('./a/text()').extract_first().strip()
                        item['title'] = title
                        item['keywords'] = ""

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                    # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                    if row == rows[-1]:
                        current_page_no = response.url.split(".")[-2][-1]  # 目前页码
                        next_page_no = int(current_page_no) + 1  # 下一页页码
                        if next_page_no < 6:
                            next_page = f"http://www.hvacjournal.cn/Category_25/Index_{str(next_page_no)}.aspx"
                            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True,
                                                 headers={'User-Agent': str(UserAgent().random)})

                # 若资讯的日期小于START_DATE，则结束循环
                else:
                    break

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['website'] = '暖通空调'
        item['website_type'] = '行业门户'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="fontzoom"]//text()').extract())

        yield item
