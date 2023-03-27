# -*- coding: utf-8 -*-

import json
import requests
from fake_useragent import UserAgent
from lxml import html, etree

# param_list前者为人民政府政策文件，后者为发改委政策发布
param = {"websiteid": "360000000000000", "cateid": "1517", "tpl": "49"}


formdata = {
    "websiteid": param["websiteid"],
    "q": "",
    "p": "1",
    "pg": "20",
    "cateid": param["cateid"],
    "pos": "",
    "pq": '绿色低碳',
    "oq": "",
    "eq": "",
    "begin": '20220201',
    "end": '20220228',
    "tpl": param["tpl"]
}

url = 'http://sousuo.jiangxi.gov.cn/jsearchfront/interfaces/cateSearch.do'
result = requests.post(url=url, data=formdata, headers={'User-Agent': str(UserAgent().random)})
data = result.json()
if 'result' in data:
    rows = data['result']
    for row in rows:
        selector = html.etree.HTML(row)
        title = ''.join(i.strip() for i in selector.xpath(
            './/div[@class="jcse-news-title"]/a/text()|.//div[@class="jcse-result-box"]/div[1]/span[2]/a/text()'))
        url = selector.xpath(
            './/div[@class="jcse-news-url"]/a/text()|.//div[@class="jcse-result-box"]/table/tbody/tr[4]/td/a/text()')[0]
        created_date = selector.xpath(
            './/span[@class="jcse-news-date"]/text()|.//div[@class="jcse-result-box"]/table/tbody/tr[2]/td[4]/text()')[
            0]
        tag = selector.xpath('.//div[@class="jcse-result-box"]/div[1]/span[1]/text()')
        if len(tag) != 0:
            tag = tag[0].replace("\r", "").replace("\n", "").strip()
        print(title, url, created_date, tag)

# url = 'http://www.jiangxi.gov.cn/art/2022/1/21/art_64505_3840985.html'
# headers = {'User-Agent': str(UserAgent().random)}
# response = requests.get(url, headers=headers)
# response.encoding = "utf8"
# html = etree.HTML(response.text)
# content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
#                   for i in html.xpath('//*[@id="zoom"]//p//text()|//div[@class="bg_middle"]//p//text()'))
#
# print(response.text)
# print(content)
#
# tag = None
# print(tag != ['领导干部任免'])