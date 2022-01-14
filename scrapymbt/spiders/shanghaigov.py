import scrapy
from scrapymbt.items import *
import copy
from scrapymbt.process import Value
from fake_useragent import UserAgent


class ShanghaigovSpider(scrapy.Spider):
    name = 'shanghaigov'
    allowed_domains = ['shanghai.gov.cn']

    def start_requests(self):
        url = 'https://www.shanghai.gov.cn/nw12344/index.html'
        yield scrapy.Request(url=url, headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        next_page_index = response.url[-6]  # 获取本页页码的index
        # 下一页URL
        if next_page_index == 'x':
            next_page_num = 2
            next_page = "https://www.shanghai.gov.cn/nw12344/index_2.html"
        else:
            next_page_num = int(next_page_index) + 1
            next_page = f"https://www.shanghai.gov.cn/nw12344/index_{str(next_page_num)}.html"

        rows = response.xpath('//div[@class="col-md-8"]/ul/li')
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
                        url = 'https://www.shanghai.gov.cn' + url
                        item['url'] = url

                        item['title'] = title
                        item['province'] = '上海'

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                 headers={'User-Agent': str(UserAgent().random)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第5页停止
                    if next_page_num < 6:
                        if next_page is not None:
                            yield scrapy.Request(url=next_page, callback=self.parse,
                                                 headers={'User-Agent': str(UserAgent().random)})

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        item = response.meta['item']

        item['website'] = '上海市政府'
        item['website_type'] = '政策法规'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="ivs_content"]//text()').extract())

        yield item

