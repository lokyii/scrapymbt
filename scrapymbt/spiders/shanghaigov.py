import scrapy
from scrapymbt.items import *
import copy
from fake_useragent import UserAgent


class ShanghaigovSpider(scrapy.Spider):
    name = 'shanghaigov'
    allowed_domains = ['shanghai.gov.cn']

    def start_requests(self):
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            formdata = {
                'text': keyword,
                'pageNo': "1",
                'newsPageNo': "1",
                'pageSize': "20",
                'resourceType': "",
                'channel': "政务公开",
                'category1': "",
                'category2': "",
                'category3': "",
                'category4': "",
                'category5': "",
                'category6': "xxgk",
                'category7': 'www.shanghai.gov.cn',
                'sortMode': "2",
                'searchMode': "",
                'timeRange': "4",
                'accurateMode': "",
                'district': "",
                'street': "",
                'stealthy': "1",
                'searchText': keyword
            }
            url = 'https://search.sh.gov.cn/searchResult'
            yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                     meta={'formdata': copy.deepcopy(formdata)})

    def parse(self, response):
        response.body.decode('utf8')
        formdata = response.meta['formdata']
        rows = response.xpath('//div[@class="result result-elm"]')
        for row in rows:
            created_date = row.xpath('.//div[@class="entry-news-content"]/div[1]/font[1]/text()|./div[@class="restcont"]/div[1]/font[1]/text()').extract_first().strip()
            if created_date is not None:
                # 若该资讯的创建日期大于等于START_DATE且小于等于END_DATE, 则进行解析
                if created_date >= self.settings.get('START_DATE'):
                    if created_date <= self.settings.get('END_DATE'):
                        item = ScrapymbtItem()

                        item['created_date'] = created_date
                        url = row.xpath('.//div[@class="other"]/div[2]/a[2]/@href').extract_first()
                        item['url'] = url
                        item['title'] = row.xpath('./a/@title').extract_first().strip()
                        item['province'] = '上海'
                        item['keywords'] = formdata['searchText']
                        item['website'] = '上海市政府'
                        item['website_type'] = '政策法规'

                        if url is not None:
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                 headers={'User-Agent': str(UserAgent().random)})

                    # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则发送下一页请求
                    if row == rows[-1]:
                        formdata['pageNo'] = str(int(formdata['pageNo']) + 1)
                        formdata['newsPageNo'] = str(int(formdata['newsPageNo']) + 1)
                        yield scrapy.FormRequest(url=url, callback=self.parse, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                                 meta={'formdata': copy.deepcopy(formdata)})

                # 若资讯的日期小于START_DATE，则结束循环
                else:
                    break

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="ivs_content"]//text()').extract())

        yield item

