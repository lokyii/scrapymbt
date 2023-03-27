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
# 下一页返回的结果为Html
class GdctWeixinPaSpider(scrapy.Spider):
    name = 'gdct_weixin_pa_01'
    allowed_domains = ['mp.weixin.qq.com']

    def start_requests(self):
        # 每次更新appmsg_token和 wap_sid2
        cookies = {
            'wxuin': '874450003',
            'devicetype': 'Windows10x64',
            'version': '63040026',
            'lang': 'zh_CN',
            'pass_ticket': 'AltEP6q1Bo1tVkxjZ9Dq0N/YYskvKtDxIfKhT6tOhQqhG/eTtQ5navmVgv48',
            'wap_sid2': 'CNOY/KADEooBeV9IRU1wQ2U3b2k3SERpMmxBMWhSS241MUVrZDc1WXJDVGY4UkZZVElGN1FrcDM1YW5jemlHTzBxRXE4TVlrU0h4NXZkbUVJZGMyc0YxS3dDZWpYeGFDVGx2dVozVXZRTmZ5M20wVFNFUEtYdHVfWTRTUDBISFRtMnc1VnFxaDBJYk0zSVNBQUF+MPSAlZYGOA1AlU4='

        }
        # 'rewardsn': '',
        # 'wxtokenkey': '777',
        # 'appmsg_token': '1168_g7nQArn2WwN4ddhnCrHK8IyNHg3H-mw0-EGRiZpE4vW6d5k0bsar9U18S8BOwtjDbB7ws-mHSj29qaup',

        params = {
            "action": "getmsg",
            "__biz": "MzA3NjUxNTM4Nw==",  # biz参数是公众号的ID
            "f": ["json", "json"],
            "offset": "10",  # 起始条数（后面可用作翻页功能）
            "count": "10",  # 返回条数
            "is_ok": "1",
            "scene": "124",
            "uin": "ODc0NDUwMDAz",  # uin是用户的ID
            # key是微信客户端补充上的参数
            "key": "c433b536fc98b3bd49cdbb38582bcd106f17da1fe602b51f89ba47ccacbb4ea6c156ef25d089fa2172b8552b22687d1ccbee54f94e28be8fc8df907b5b3272fd700d388118fa23dff3b0c0bb496b7e807a904eaa73aa877cb78b21812fc8deb0eb95f09fd4eed318373d5dbf9c4c83a2d14eab41d350f46e3c99eda3bd1642f6",
            "pass_ticket": "AltEP6q1Bo1+tVk+xjZ9Dq0N/YYskvKtDxIfKhT6tOhQqhG/eTtQ5+navmVgv+48",
            "wxtoken": "",  # 空
            "appmsg_token": "1173_XeD%2BPnuZsvRrqNU2jPV4uyby7_SKAP8Uip8j7w~~",  # token
            "x5": "0"
        }

        # 注意拼接url时，scrapy的urlencode方法不会自动添加问号
        next_page = "https://mp.weixin.qq.com/mp/profile_ext?" + urlencode(params)
        yield scrapy.Request(url=next_page, callback=self.parse, meta={'params': params, 'cookies': cookies},
                             headers={'User-Agent': str(UserAgent().random)}, cookies=cookies)

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
                    # 每次要更新key和appmsg_token，其他不变
                    offset = str(int(params["offset"]) + 10)
                    params["offset"] = offset
                    # 注意拼接url时，scrapy的urlencode方法不会自动添加问号
                    next_page = "https://mp.weixin.qq.com/mp/profile_ext?" + urlencode(params)
                    yield scrapy.Request(url=next_page, callback=self.parse,
                                         meta={'params': params, 'cookies': cookies},
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


