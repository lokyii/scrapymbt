from urllib.parse import urlencode

import requests
from lxml import etree
from fake_useragent import UserAgent
keyword = '绿色低碳'
year = '2021'
month = '12'

# params = {
#                         'q': '',
#                         't': 'govall',
#                         'advance': 'true',
#                         'orpro': keyword,
#                         'andpro': '',
#                         'notpro': '',
#                         'inpro': keyword,
#                         'pubmintimeYear': year,
#                         'pubmintimeMonth': month,
#                         'pubmintimeDay': '',
#                         'pubmaxtimeYear': year,
#                         'pubmaxtimeMonth': month,
#                         'pubmaxtimeDay': '',
#                         'searchfield': '',
#                         'colid': '',
#                         'timetype': 'timeqb',
#                         'mintime': '',
#                         'maxtime': '',
#                         'sort': 'pubtime',
#                         'sortType': 1,
#                         'nocorrect': ''
#             }
# url = 'http://sousuo.gov.cn/s.htm?' + urlencode(params)
# headers = {'User-Agent': str(UserAgent().random)}
# response = requests.get(url, headers=headers)
# response.encoding = "utf8"
# print(response.text)
# html = etree.HTML(response.text)
# rows = html.xpath('//div[@class="result"]/ul/li')
# next_page_url = html.xpath('//*[@id="snext"]/@href')
# print(len(next_page_url))
# for row in rows:
#     created_date = row.xpath('./p[2]/span/text()')[0].strip()[5:].replace('.', '-')
#     print(created_date)

url = 'http://www.gov.cn/zhengce/zhengceku/2022-01/20/content_5669455.htm'
response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//*[@class="pages_content"]//p//text()'))
print(response.text)
print(content)