#-*- coding:utf-8 -*-

from urllib.parse import unquote, urlencode
# name = '%E6%94%BF%E5%BA%9C%E6%96%87%E4%BB%B6'
# url_decode_name = unquote(name)
# print(url_decode_name)
import requests
from fake_useragent import UserAgent
from lxml import etree

# params = {
#                         "allSearchWord": "数据中心",
#                         "orSearchType": "1",
#                         "pageSize": "10",
#                         "pageNum": "0",
#                         "docName": "",
#                         "docYear": "",
#                         "docType": "",
#                         "siteCode": "5100000062",
#                         "siteCodes": "",
#                         "wordPlace": "2",
#                         "orderBy": "1",
#                         "column": "%E6%94%BF%E5%BA%9C%E6%96%87%E4%BB%B6",
#                         "countKey": "0",
#                         "docNameRight": "",
#                         "docTypeRight": "",
#                         "docYearRight": "",
#                         "areaSearchFlag": "1",
#                         "left_right_index": "0"
#             }
# url = 'https://www.sc.gov.cn/so4/a?' + urlencode(params)
# response = requests.get(url=url, headers={'User-Agent': str(UserAgent().random)})
# html = etree.HTML(response.text)
# rows = html.xpath('//div[@class="wordGuide Residence-permit"]')
#
# if len(rows) != 0:
#     for row in rows:
#         created_date = row.xpath('./div[2]/div/p[2]/span/text()')[0].strip()[5:].strip()
#         title = row.xpath('./div[1]/a/text()')[0].strip()
#         url = row.xpath('./div[1]/a/@href')[0].strip()
#         print(created_date, title, url)

url = 'https://www.sc.gov.cn/10462/zfwjts/2022/1/29/4de9bf4702644ff98bfc6c3a4c03957d.shtml'
response = requests.get(url=url, headers={'User-Agent': str(UserAgent().random)})
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//td[@class="black14X STYLE1"]/div//p//text()|//td[@class="contText"]//p//text()'))

print(response.text)
print(content)


