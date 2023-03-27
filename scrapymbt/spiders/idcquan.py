import copy
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


class IdcquanSpider(scrapy.Spider):
    name = 'idcquan'
    allowed_domains = ['idcquan.com']

    def start_requests(self):
        url_list = [{'url': 'http://news.idcquan.com/index6_1.shtml', 'website': 'IDC圈-IDC新闻'},
                    {'url': 'http://dc.idcquan.com/index6_1.shtml', 'website': 'IDC圈-IDC设施'},
                    {'url': 'http://www.idcquan.com/tech/index_1.shtml', 'website': 'IDC圈-IDC节能'},
                    {'url': 'http://zt.idcquan.com/zhoukan/1.shtml', 'website': 'IDC圈-一周最HOT'},
                    {'url': 'http://www.idcquan.com/review/1.shtml', 'website': 'IDC圈-IDC圈时评'},
                ]

        for i in url_list:
            yield scrapy.Request(url=i['url'], meta={'website': copy.deepcopy(i['website'])},
                                 headers={'User-Agent': str(UserAgent().random)})

    def parse(self, response):
        website = response.meta['website']
        response.body.decode('utf8')
        rows = response.xpath('//div[@class="news clearfix"]')

        for row in rows:
            created_date = row.xpath('./span[@class="date"]/text()').extract_first().strip()[:10]

            # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    item['created_date'] = created_date
                    url = row.xpath('.//a[@class="bdurl"]/@href').extract_first().strip()
                    item['url'] = url
                    title = row.xpath('.//span[@class="title"]/text()').extract_first().strip()
                    item['title'] = title
                    item['website'] = website
                    keywords_list = row.xpath('.//div[@class="d3"]/div[@class="fl"]/a/text()').extract()
                    if keywords_list is not None:
                        keywords = ','.join(i.strip() for i in keywords_list)
                    item['keywords'] = keywords

                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                if row == rows[-1]:
                    current_page_no = response.url.split(".")[-2][-1]  # 目前页码
                    next_page_no = int(current_page_no)+1  # 下一页页码
                    if next_page_no < 11:
                        if website == "IDC圈-IDC新闻":
                            next_page = f"http://news.idcquan.com/index6_{str(next_page_no)}.shtml"
                        elif website == "IDC圈-IDC设施":
                            next_page = f"http://dc.idcquan.com/index6_{str(next_page_no)}.shtml"
                        elif website == "IDC圈-IDC节能":
                            next_page = f'http://www.idcquan.com/tech/index_{str(next_page_no)}.shtml'
                        elif website == "IDC圈-IDC圈时评":
                            next_page = f'http://www.idcquan.com/review/{str(next_page_no)}.shtml'

                        yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True,
                                             meta={'website': copy.deepcopy(website)},
                                             headers={'User-Agent': str(UserAgent().random)})

            # 若资讯的日期小于START_DATE，则结束循环
            else:
                break

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['website_type'] = '行业门户'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="clear deatil article-content fontSizeSmall BSHARE_POP"]/p//text()').extract())

        yield item

# 可能需要设置代理
