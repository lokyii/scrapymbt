import scrapy
from scrapymbt.items import *
import copy
from scrapymbt.process import Value, FindStr


# 国家发改委
class NdrcSpider(scrapy.Spider):
    name = 'ndrc'
    allowed_domains = ['ndrc.gov.cn']
    # 发展改革委令，规范性文件，公告，规划文本，通知，政策解读
    start_urls = ['https://www.ndrc.gov.cn/xxgk/zcfb/fzggwl/index.html?code=&state=123',
                  'https://www.ndrc.gov.cn/xxgk/zcfb/ghxwj/index.html?code=&state=123',
                  'https://www.ndrc.gov.cn/xxgk/zcfb/gg/index.html?code=&state=123',
                  'https://www.ndrc.gov.cn/xxgk/zcfb/ghwb/index.html?code=&state=123',
                  'https://www.ndrc.gov.cn/xxgk/zcfb/tz/index.html?code=&state=123',
                  'https://www.ndrc.gov.cn/xxgk/jd/jd/index.html?code=&state=123']

    def parse(self, response):
        response.body.decode('utf8')  # 爬取下来的编码是ISO-8859-1格式，需要转化为utf-8格式
        index = FindStr(response.url, '/', 6).return_nth_place()  # 获取源URL'/'第6次出现的位置
        base_url = response.url[:index]  # 获取内容页的源URL

        next_page_index = response.url[index+6]  # 获取本页页码的index
        # 下一页URL
        if next_page_index == 'h':
            next_page_num = 1
            next_page = base_url + "index_1.html?code=&state=123"
        else:
            next_page_num = int(next_page_index) + 1
            next_page = base_url + f"index_{str(next_page_num)}.html?code=&state=123"

        rows = response.xpath('//div[@class="list"]/ul/li')
        for row in rows:
            if row != rows[5] and row != rows[11] and row != rows[17] and row != rows[23] and row != rows[29]:
                created_date = row.xpath('./span/text()').extract_first().strip()
                created_date = created_date.replace('/', '-')  # 将日期转换成YYYY-MM-DD格式

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
                            url = base_url + url[2:]
                            item['url'] = url
                            item['title'] = title

                            # 除规划文本/通知有各省份政策，其余为全国政策
                            item['province'] = '全国'
                            if response.url.split('/')[-2] == 'ghwb' or response.url.split('/')[-2] == 'tz':
                                province = Value(title, self.settings.get('PROVINCE')).return_value()
                            if province is not None:
                                item['province'] = province

                            if url is not None:
                                yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)})

                    # 如果列表页最后一条资讯的创建日期大于等于START_DATE，则进入下一页
                    if row == rows[-2]:
                        # 循环到第5页停止
                        if next_page_num < 5:
                            if next_page is not None:
                                yield scrapy.Request(url=next_page, callback=self.parse)

                # 若资讯的日期小于START_DATE，则结束循环
                else:
                    break

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']

        item['website'] = '国家发改委'
        item['website_type'] = '政策法规'
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace('\u2003', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[@class="article_con article_con_notitle"]//text()').extract())

        yield item


