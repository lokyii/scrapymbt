import re

import requests
from lxml import etree
from fake_useragent import UserAgent

# keyword = '绿色工业'
# begin = '20211201'
# end = '20211231'
#
# data = {
#                         "websiteid": "330000000000000",
#                         "pg": "10",
#                         "p": "1",
#                         "tpl": "1569",
#                         "cateid": "372",
#                         "word": keyword,
#                         "checkError": "1",
#                         "isContains": "1",
#                         "q": keyword,
#                         "begin": begin,
#                         "end": end,
#                         "timetype": "5",
#                         "pos": "title,content,_default_search",
#                         "sortType": "2"
#                 }
#
# url = 'http://search.zj.gov.cn/jsearchfront/interfaces/cateSearch.do'
# response = requests.post(url=url, data=data, headers={'User-Agent': str(UserAgent().random)})
# result = response.json()
# rows = result['result']
# total_no = result['total']
#
# if rows is not None:
#     for row in rows:
#         print(row)
#         html = etree.HTML(row)
#         created_date = html.xpath('.//div[@class="sourceTime"]/span[2]/text()')[0][3:]
#         url_text = html.xpath('.//div[@class="newsDescribe"]/a/@href')[0]
#         pattern = '.*url=(.*)&q=.*'
#         url = re.match(pattern, url_text).group(1).replace('%2F', '/').replace('%3A', ':')
#         title = ''.join(i.strip().replace('\r', '').replace('\n', '')
#                         for i in html.xpath('.//div[@class="titleWrapper"]/a/text()'))
#         source = html.xpath('.//div[@class="sourceTime"]/span[1]/text()')[0][3:6]
#         print(created_date, url, title, source)
#         print('***************************************')

# url = 'http://fzggw.zj.gov.cn/art/2021/12/27/art_1229123366_2385158.html'
# url = 'http://www.zj.gov.cn/art/2021/12/22/art_1229019365_2382764.html'
url = 'http://kjt.zj.gov.cn/art/2022/1/19/art_1229080140_2390174.html'
response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//*[@id="zoom"]//p//text()|//div[@class="article-conter"]//p//text()'))
print(response.text)
print(content)
