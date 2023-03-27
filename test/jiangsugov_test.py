import re

import requests
from lxml import etree
from fake_useragent import UserAgent

keyword = '高品质住宅'
begin = '20211201'
end = '20211231'

# data = {
#                 "websiteid": "320000000200000",
#                 "q": keyword,
#                 "p": "1",
#                 "pg": "20",
#                 "cateid": "29",
#                 "pos": "",
#                 "pq": "",
#                 "oq": "",
#                 "eq": "",
#                 "begin": begin,
#                 "sortType": "0",
#                 "end": end,
#                 "tpl": "38"
#         }
#
# url = 'http://www.jiangsu.gov.cn/jsearchfront/interfaces/cateSearch.do'
# response = requests.post(url=url, data=data, headers={'User-Agent': str(UserAgent().random)})
# result = response.json()
# if len(result) != 0:
#     rows = result['result']
#     total_no = result['total']
#     print(total_no)

# if rows is not None:
#     for row in rows:
#         # print(row)
#         html = etree.HTML(row)
#         created_date = html.xpath('.//span[@class="jcse-news-date"]/text()')[0].strip()[-10:]
#         url = html.xpath('.//div[@class="jcse-news-url"]/a/text()')[0]
#         print(created_date, url, )
#         print('***************************************')

# url = 'http://www.jiangsu.gov.cn/art/2021/12/30/art_46144_10244386.html'
url = 'http://www.jiangsu.gov.cn/art/2021/12/20/art_46144_10220441.html'
response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
# print(response.text)
html = etree.HTML(response.text)
# title = html.xpath('//meta[@name="ArticleTitle"]/@content')[0].strip()
title = html.xpath('//table[@class="xxgk_table"]/tbody/tr[3]/td[2]//text()')[0].strip()
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//div[@class="article_content"]/p//text()|//*[@id="Zoom"]/p//text()|/html/body/div/div[4]/div/div/div[2]//p//text()'))
print(title)
print(content)


