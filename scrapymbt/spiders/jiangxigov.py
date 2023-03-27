import copy
import scrapy
from fake_useragent import UserAgent
from lxml import html
from scrapymbt.items import ScrapymbtItem


class JiangxigovSpider(scrapy.Spider):
    name = 'jiangxigov'
    allowed_domains = ['jiangxi.gov.cn']

    # 省政府信息公开和部门信息公开
    def start_requests(self):
        begin = self.settings.get('START_DATE').replace('-', '')
        end = self.settings.get('END_DATE').replace('-', '')

        # param_list前者为人民政府政策文件，后者为发改委政策发布
        param_list = [{"websiteid": "360000000000000", "cateid": "1517", "tpl": "49"},
                      {"websiteid": "360000000005000", "cateid": "622", "tpl": "15"}]
        for keyword in self.settings.get('PROVINCE_POLICY_KW'):
            for param in param_list:
                formdata = {
                    "websiteid": param["websiteid"],
                    "q": "",
                    "p": "1",
                    "pg": "20",
                    "cateid": param["cateid"],
                    "pos": "",
                    "pq": keyword,
                    "oq": "",
                    "eq": "",
                    "begin": begin,
                    "end": end,
                    "tpl": param["tpl"]
                }

                url = 'http://sousuo.jiangxi.gov.cn/jsearchfront/interfaces/cateSearch.do'
                yield scrapy.FormRequest(url=url, formdata=formdata, headers={'User-Agent': str(UserAgent().random)},
                                         meta={'keyword': copy.deepcopy(keyword)})

    def parse(self, response):
        keyword = response.meta['keyword']
        result = response.json()
        if 'result' in result:
            rows = result['result']
            for row in rows:
                selector = html.etree.HTML(row)
                title = ''.join(i.strip() for i in selector.xpath('.//div[@class="jcse-news-title"]/a/text()|.//div[@class="jcse-result-box"]/div[1]/span[2]/a/text()'))
                url = selector.xpath('.//div[@class="jcse-news-url"]/a/text()|.//div[@class="jcse-result-box"]/table/tbody/tr[4]/td/a/text()')[0]
                created_date = selector.xpath('.//span[@class="jcse-news-date"]/text()|.//div[@class="jcse-result-box"]/table/tbody/tr[2]/td[4]/text()')[0]
                tag = selector.xpath('.//div[@class="jcse-result-box"]/div[1]/span[1]/text()')
                if len(tag) != 0:
                    tag = tag[0].replace("\r", "").replace("\n", "").strip()

                if self.settings.get('START_DATE') <= created_date <= self.settings.get('END_DATE'):
                    if tag != '领导干部任免':
                        item = ScrapymbtItem()
                        item['created_date'] = created_date
                        item['title'] = title
                        item['url'] = url
                        item['keywords'] = keyword
                        item['province'] = '江西'
                        item['website'] = '江西省政府'
                        item['website_type'] = '政策法规'

                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)})

    def item_parse(self, response):
        response.body.decode('utf8')
        item = response.meta['item']
        item['content'] = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//*[@id="zoom"]//p//text()|//div[@class="bg_middle"]//p//text()').extract())

        yield item

