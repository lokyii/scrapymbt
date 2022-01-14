import scrapy
from scrapymbt.items import *
import copy
from scrapymbt.process import Value


# 中央人民政府
class GovSpider(scrapy.Spider):
    name = 'gov'
    allowed_domains = ['gov.cn']
    # 最新政策，部门解读，专家解读，媒体解读；政务联播-部门，政务联播-地方
    start_urls = ['http://sousuo.gov.cn/column/30469/0.htm', 'http://sousuo.gov.cn/column/30474/0.htm',
                  'http://sousuo.gov.cn/column/30593/0.htm', 'http://sousuo.gov.cn/column/40048/0.htm',
                  'http://sousuo.gov.cn/column/30613/0.htm', 'http://sousuo.gov.cn/column/30902/0.htm']

    def parse(self, response):
        next_page = response.xpath('//div[@class="newspage cl"]/ul/li[last()]/a[@class="next"]/@href').extract_first()
        next_page_num = int(next_page[-5])  # 下一页的页码
        rows = response.xpath('//div[@class="list list_1 list_2"]/ul/li')
        for row in rows:
            created_date = row.xpath('./h4/span[@class="date"]/text()').extract_first().strip()
            created_date = created_date.replace('.', '-')  # 将日期转换成YYYY-MM-DD格式

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    title = row.xpath('./h4/a/text()').extract_first().strip()

                    # 若标题包含特定关键字，则进一步解析
                    is_useful = Value(title, self.settings.get('PROVINCE_POLICY_KW')).return_value()
                    if is_useful is not None:
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        url = row.xpath('./h4/a/@href').extract_first()
                        item['url'] = url
                        item['title'] = title
                        # 除政务联播-地方为各省份政策，其余为全国政策
                        item['province'] = '全国'
                        if response.url.split('/')[-2] == '30902':
                            item['province'] = Value(title, self.settings.get('PROVINCE')).return_value()

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    # 循环到第20页停止
                    if next_page_num < 20:
                        if next_page is not None:
                            yield scrapy.Request(url=next_page, callback=self.parse)

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        response.body.decode('utf8')  # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        item = response.meta['item']

        item['website'] = '中央政府'
        item['website_type'] = '政策法规'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@class="pages_content"]//text()').extract())

        yield item



