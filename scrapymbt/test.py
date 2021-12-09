import datetime
import json
import re
import threading
import time
import math

import requests
from lxml import etree
'''
url = 'http://webapi.chinaiol.com/api/User/GetChannelMore?chinnelid=21&pageNumber=0'
# response = requests.get(url)
# origin_url = response.url
pattern =re.compile(r'\d+')
result = pattern.findall(url)
channel_id = result[0]
page_num = str(int(result[1]) + 1)
next_page = f'http://webapi.chinaiol.com/api/User/GetChannelMore?chinnelid={channel_id}&pageNumber={page_num}'
print(next_page)
'''

'''# text = response.json().get('result').get('contentHtml')
# text = etree.HTML(text)
# rows = text.xpath('//div[@class="layui-row layui-col-space15 mp15"]')

for row in rows:
    title = row.xpath('.//h3[@class="tit"]/a/text()')[0]
    url = 'http://www.chinaiol.com' + row.xpath('.//h3[@class="tit"]/a/@href')[0]
    keywords = ','.join(i for i in row.xpath('.//p[@class="tag"]/a/text()'))
    print(title)
    print(url)
    print(keywords)
'''

'''
url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=2'
keyword = '中央空调'
start_time = '2021:10:01'
end_time = '2021:11:16'
page_num = 1
Tag =2

params = {
    'searchtype': '2',
    'page_index': page_num,
    'bidSort': '0',
    'pinMu': '0',
    'bidType': '7',
    'kw': keyword,
    'start_time': start_time,
    'end_time': end_time,
    'timeType': '6'
}
headers = {
    'Cookie': 'Cookie: Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1635822814,1637047026; td_cookie=3076853793; '
              'Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1635822828,1635920317,1637047056; '
              'Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1637047042; '
              'JSESSIONID=xf8r4ZVTIVInZTwuqj_jBEy10QPoJbnSnw4Q9jeCBjVkF8k1uWSD!-659192651; '
              'Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1637118745',
    'Host': 'search.ccgp.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/83.0.4103.106 Safari/537.36'
}

response = requests.get(url, headers=headers, params=params)
response.encoding = "utf8"
etree(response.text)

'''



#
# website_type = '暖通家' + data.xpath('//*[@class="pos"]/a[2]/text()')[0]
# content = ''.join(i.replace('\r', '').replace('\u3000', '') for i in data.xpath('//*[@id="article"]//text()'))
# print(website_type)
# print(content)

# rows = response.xpath('//ul[@class="vT-srch-result-list-bid"]/li')
# kw = response.xpath('//*[@id="kw"]/@value')
#
# for row in rows:
#     mix = row.xpath('./span/text()')
#     url = row.xpath('./li/a/@href')[0]
#     title = row.xpath('./li/a/text()')
#     keywords = kw
#     province = row.xpath('./span/a/text()')[0]
#     # project =
#     print(mix)
#     print(url)
#     print(title)
#     print(keywords)
#     print(province)
#     # print(project)
#     print('-------------------------------------------------------')


# content = ' '.join(i.strip().replace('\r', '').replace('\u3000', '')
#                   for i in response.xpath('//*[@class="vF_detail_content"]/div[@class= "Section0"]//text()'))
#
# print(content)



# from scrapymbt.process import *
# from scrapymbt.settings import *
# from urllib.parse import quote, unquote
#
# kw = '2021%3A10%3A01'
# start_date = START_DATE.replace('-', ':')
# print(quote(start_date))

# from scrapymbt.process import *
# keywords = "海林,楼宇自控,北京"
# product = Value(keywords, PRODUCT).return_value()
# print(product is None)






