# 中电能协数据中心节能技术委员会微信公众号爬虫
import ast
import copy
import re
import time
from urllib.parse import urlencode
import scrapy
from fake_useragent import UserAgent
from scrapymbt.items import ScrapymbtItem


# 每次要根据fiddler抓包，改首页的cookies和后面翻页网址的参数
# 下一页返回的结果为json
class GdctWeixinPaSpider(scrapy.Spider):
    name = 'gdct_weixin_pa'
    allowed_domains = ['mp.weixin.qq.com']

    def start_requests(self):
        # 每次更新pass_ticket和 wap_sid2
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA3NjUxNTM4Nw==&scene=124#wechat_redirect"
        cookies = {
            'appmsg_token': '1194_3IWCUAPNWwWI5z%2Bm6Aq15d4ClHLVK5Ii9jZmH2hBmUvkeRMpcr70JcwtMX244Yr01TShZuj25_feBW1A',
            'rewardsn': '',
            'wxtokenkey': '777',
            'wxuin': '874450003',
            'devicetype': 'Windows10x64',
            'version': '63040026',
            'lang': 'zh_CN',
            'pass_ticket': 'AF+D1kO6wUoyHTJhNeEze+KMefHJqr8IrYLlu4DkuqBq0CdvoYOUUQA3GcsiMCuiOcN/dmp5lHuGvVt46Fdh8g==',
            'wap_sid2': 'CNOY/KADEooBeV9ISnBJc1k4dG4ySTNlUllwRVlQV25taGhBaEdzMVhpMEM0WG5MOFg5RWdYcTZIdi1haEQyUmZnMEFyNlZURUpxUXJWXzk2Sng5M0xYWUo2djgwSlpKdy1KZ3hCOE1VLVJIT2lTWm9EeHU4ejN6SDc3ZFRYdDhyOG14X2RDd0k4VFVaZ1NBQUF+MJTbhKEGOA1AlU4='
        }

        params = {}

        yield scrapy.Request(url=url, headers={'User-Agent': str(UserAgent().random)}, cookies=cookies,
                             meta={'params': params, 'cookies': cookies})

    def parse(self, response):
        print(response.text)
        params = response.meta['params']
        cookies = response.meta['cookies']

        result = re.search(r"var msgList = '(.*?)'", response.text).group(1)  # 匹配出首页结果，呈现出“一条主要拉几条次要”的形式
        result = result.replace("&quot;", "").replace("&nbsp", "").replace("amp;", "")  # 删除无关字符
        rows = result.split("{comm_msg_info:")[1:]  # 获取首页所有行数

        for row in rows:
            # 用正则表达式匹配，match和 search是匹配一次，匹配不成功返回None， findall匹配所有，匹配不成功返回空列表。
            timeStamp = re.search(r"datetime:(\d+),", row).group(1)  # 匹配发布时间
            # 时间戳文本变为YYYY-MM-DD格式
            timeArray = time.localtime(int(timeStamp))
            created_date = time.strftime("%Y-%m-%d", timeArray)

            if created_date >= self.settings.get('START_DATE'):
                if created_date <= self.settings.get('END_DATE'):
                    item = ScrapymbtItem()
                    url = re.search(r"content_url:(.*?),", row).group(1)
                    title = re.search(r"title:(.*?),", row).group(1)

                    item["created_date"] = created_date
                    item["url"] = url
                    item["title"] = title
                    item["keywords"] = "数据中心"
                    item["website"] = "数据中心节能技术委员会"
                    item["website_type"] = "行业门户"

                    yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                         headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

                    # 若存在次要信息,则将次要信息提取出来储存；可能存在有多条次要信息的情况
                    rows_position = row.find("multi_app_msg_item_list")
                    title_pattern = re.compile(r"title:(.*?),")
                    url_pattern = re.compile(r"content_url:(.*?),", )
                    other_info_no = len(title_pattern.findall(row)) - 1

                    if other_info_no != 0:
                        for i in range(other_info_no):
                            item = ScrapymbtItem()
                            url = url_pattern.findall(row, rows_position)[i]
                            title = title_pattern.findall(row, rows_position)[i]

                            item["created_date"] = created_date
                            item["url"] = url
                            item["title"] = title
                            item["keywords"] = "数据中心"
                            item["website"] = "数据中心节能技术委员会"
                            item["website_type"] = "行业门户"
                            yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                                 headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

                # 若首页最后一条结果日期大于上月第一天，请求下一页结果
                if row == rows[-1]:
                    # 每次要更新key、pass_ticket和appmsg_token，其他不变
                    if len(params) == 0:
                        offset = "10"
                    else:
                        offset = str(int(params["offset"]) + 10)
                    params = {
                        "action": "getmsg",
                        "__biz": "MzA3NjUxNTM4Nw==",  # biz参数是公众号的ID
                        "f": ["json", "json"],
                        "offset": offset,  # 起始条数（后面可用作翻页功能）
                        "count": "10",  # 返回条数
                        "is_ok": "1",
                        "scene": "124",
                        "uin": "ODc0NDUwMDAz",  # uin是用户的ID
                        # key是微信客户端补充上的参数
                        "key": "140bdc387030f4128d5156433a767b9ae2ce38d458943837da761a4cdfd8b3baf62b043496d20022b5798c54f205b95feb3d8951a77829d278166400bad6bf1cf1d46af8103c961c44aa21532d66746fb483e043c743c7c7c2364de17429d4ea3da28d2b80be3bc687943584933595e041abb2622905b6c3a24774a891457606",
                        "pass_ticket": "AF%2BD1kO6wUoyHTJhNeEze%2BKMefHJqr8IrYLlu4DkuqAOKjOtgI25ikD0vak7CXYGbGwyr5jr63mhovmJv3MdWw%3D%3D",
                        "wxtoken": "",  # 空
                        "appmsg_token": "1210_EWNkabaUyV9%252BnoQTaDRnyVez-oKD10W1z9028g~~",  # token
                        "x5": "0"
                    }

                    # 注意拼接url时，scrapy的urlencode方法不会自动添加问号
                    next_page = "https://mp.weixin.qq.com/mp/profile_ext?" + urlencode(params)
                    yield scrapy.Request(url=next_page, callback=self.parse, meta={'params': params, 'cookies': cookies},
                                         headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

            else:
                break

    def next_parse(self, response):
        params = response.meta['params']
        cookies = response.meta['cookies']
        result = response.json()

        if len(result) != 0:  # 若返回空白字典，字典的长度为0
            next_offset = result['next_offset']  # 下一页起始条数
            rows = ast.literal_eval(result['general_msg_list'])['list']  # 将字符串格式的值转为字典后在提取列表

            for row in rows:
                timeStamp = row["comm_msg_info"]["datetime"]   # 发布时间
                # 时间戳文本变为YYYY-MM-DD格式
                timeArray = time.localtime(int(timeStamp))
                created_date = time.strftime("%Y-%m-%d", timeArray)

                if created_date >= self.settings.get('START_DATE'):
                    if created_date <= self.settings.get('END_DATE'):
                        item = ScrapymbtItem()
                        url = row["app_msg_ext_info"]["content_url"]
                        title = row["app_msg_ext_info"]["title"]

                        item["created_date"] = created_date
                        item["url"] = url
                        item["title"] = title
                        item["keywords"] = "数据中心"
                        item["website"] = "数据中心节能技术委员会"
                        item["website_type"] = "行业门户"

                        yield scrapy.Request(url=url, callback=self.item_parse, meta={'item': copy.deepcopy(item)},
                                             headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

                        # 若存在次要信息,则将次要信息提取出来储存；可能存在有多条次要信息的情况

                        other_info_no = len(row["app_msg_ext_info"]["multi_app_msg_item_list"])

                        if other_info_no != 0:
                            for i in row["app_msg_ext_info"]["multi_app_msg_item_list"]:
                                item = ScrapymbtItem()
                                url = i['content_url']
                                title = i['title']

                                item["created_date"] = created_date
                                item["url"] = url
                                item["title"] = title
                                item["keywords"] = "数据中心"
                                item["website"] = "数据中心节能技术委员会"
                                item["website_type"] = "行业门户"
                                yield scrapy.Request(url=url, callback=self.item_parse,
                                                     meta={'item': copy.deepcopy(item)},
                                                     headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

                    # 若最后一条结果日期大于上月第一天，请求下一页结果
                    if row == rows[-1]:
                        params['next_offset'] = next_offset
                        next_page = "https://mp.weixin.qq.com/mp/profile_ext?" + urlencode(params)
                        yield scrapy.Request(url=next_page, callback=self.next_parse, meta={'params': params, 'cookies': cookies},
                                             headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

                else:
                    break

    def item_parse(self, response):
        item = response.meta['item']
        content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                          for i in response.xpath('//*[@id="js_content"]//text()').extract())
        # 删除文章结束后的无关内容
        end_position = content.find("END")
        if end_position != -1:
            content = content[:end_position]

        item['content'] = content
        yield item


