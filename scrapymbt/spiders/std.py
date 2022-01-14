import scrapy
from scrapymbt.items import *
import copy


class StdSpider(scrapy.Spider):
    name = 'std'
    allowed_domains = ['std.samr.gov.cn']

    def start_requests(self):
        for keyword in self.settings.get('STD_KW'):
            url = f'http://std.samr.gov.cn/search/stdPage?q={keyword}&tid=&pageNo=1'
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        rows = response.xpath('//div[@class="row"]/div')
        for row in rows:
            item = StandardItem()
            url = None

            # 国标状态
            status = row.xpath('.//div[@class="post-head"]//tr/td[2]/span/text()').extract_first().strip()
            pid = row.xpath('.//div[@class="post-head"]//tr/td[1]/a/@pid').extract_first()
            if status == '正在起草' or status == '正在征求意见':
                # 正在起草国标有下达日期
                notice_date = row.xpath('./div[@class="panel-footer"]/time/text()').extract_first().strip()
                # 若该国标的下达日期（正在起草）大于等于START_DATE且小于等于END_DATE, 则进行解析
                if self.settings.get('START_DATE') <= notice_date <= self.settings.get('END_DATE'):
                    item['notice_date'] = notice_date
                    url = f'http://std.samr.gov.cn/gb/search/gbDetailed?id={pid}'  # 落在上月区间，才执行爬虫

            elif status == '即将实施':
                # 即将实施国标有发布日期和实施日期
                publish_date = row.xpath('./div[@class="panel-footer"]/time[1]/text()').extract_first().strip()
                effect_date = row.xpath('./div[@class="panel-footer"]/time[2]/text()').extract_first().strip()
                # 若该国标的发布日期（即将实施）大于等于START_DATE且小于等于END_DATE, 则进行解析
                if self.settings.get('START_DATE') <= publish_date <= self.settings.get('END_DATE'):
                    item['publish_date'] = publish_date
                    item['effect_date'] = effect_date
                    url = f'http://std.samr.gov.cn/gb/search/gbDetailed?id={pid}'  # 落在上月区间，才执行爬虫

            item['status'] = status
            item['url'] = url
            item['title'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                    for i in row.xpath('.//div[@class="post-head"]//tr/td[1]/a//text()').extract())
            item['keyword'] = keyword

            if url is not None:
                yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

    def item_parse(self, response):
        item = response.meta['item']

        item['website_type'] = '国家标准'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@class="row"]/div/div//p//text()').extract())

        yield item


