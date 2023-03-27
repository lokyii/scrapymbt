import copy
import scrapy
from fake_useragent import UserAgent
from datetime import datetime
from scrapymbt.items import ScrapymbtItem


class AirconSpider(scrapy.Spider):
    name = 'aircon'
    allowed_domains = ['aircon.com.cn']
    start_urls = ['http://www.aircon.com.cn/']

    def parse(self, response):
        rows = response.xpath('//*[@id="Article"]/li')
        for row in rows:
            created_date = row.xpath('.//span[@class="time"]/text()').extract_first().strip()
            created_date = datetime.strptime(created_date, '%Y-%m-%d').strftime('%Y-%m-%d')

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    url = row.xpath('.//span[@class="content"]/a/@href').extract_first()
                    item['url'] = url
                    title = row.xpath('.//span[@class="content"]/a/@title').extract_first().strip()
                    item['title'] = title

                    #将文章作者记为关键字，若文章作者为艾肯网编辑，则关键字为空
                    keywords = row.xpath('.//span[@class="author-name"]/text()').extract_first()
                    if "艾肯网" in keywords:
                        keywords = ""
                    item['keywords'] = keywords

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         dont_filter=True)
                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    formdata = {
                        "action": "newsmore",
                        "pageindex": "3",
                        "channelid": "20007,20004",
                        "columnid": "1",
                        "loopid": "",
                        "loopcount": ""
                    }

                    next_page = 'http://www.aircon.com.cn/home/index_json1.asp?columnid=1&pageIndex=3'
                    yield scrapy.FormRequest(url=next_page, formdata=formdata,
                                             headers={'User-Agent': str(UserAgent().random)},
                                             callback=self.next_parse, meta={'formdata': copy.deepcopy(formdata)})
            else:
                break

    def next_parse(self, response):
        formdata = response.meta['formdata']
        pageindex = formdata["pageindex"]
        pageindex_int = int(pageindex)

        result = response.json()
        if len(result) != 0:  # 若返回空白字典，字典的长度为0
            rows = result['lists']

            if rows is not None:
                for row in rows:
                    created_date = row['times'].split(" ")[0].replace("/", "-")
                    created_date = datetime.strptime(created_date, '%Y-%m-%d').strftime('%Y-%m-%d')

                    if created_date >= self.settings.get('START_DATE'):
                        if created_date <= self.settings.get('END_DATE'):
                            item = ScrapymbtItem()
                            item['created_date'] = created_date
                            url = row['link']
                            item['url'] = url
                            item['title'] = row['title']
                            keywords = row['writer']
                            if "艾肯网" in keywords:
                                keywords = ""
                            item['keywords'] = keywords

                            if url is not None:
                                yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                     headers={'User-Agent': str(UserAgent().random)})

                        # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                        if row == rows[-1]:
                            # 循环到第50页停止
                            if pageindex_int <= 50:
                                formdata = {
                                    "action": "newsmore",
                                    "pageindex": str(pageindex_int+1),
                                    "channelid": "20007,20004",
                                    "columnid": "1",
                                    "loopid": "",
                                    "loopcount": ""
                                }
                                next_page = f'http://www.aircon.com.cn/home/index_json1.asp?columnid=1&pageIndex={str(pageindex_int+1)}'
                                yield scrapy.FormRequest(url=next_page, formdata=formdata,
                                                         headers={'User-Agent': str(UserAgent().random)},
                                                         callback=self.next_parse,
                                                         meta={'formdata': copy.deepcopy(formdata)})
                    else:
                        break

    def item_parse(self, response):
        response.body.decode('gb18030')
        item = response.meta['item']

        item['website'] = '艾肯网-中央空调'
        item['website_type'] = '行业门户'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//section[@class="textblock"]//text()').extract())

        yield item
