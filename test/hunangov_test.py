from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent
from lxml import etree

# params = {
#                 'q': '绿色低碳',
#                 'searchfields': '',
#                 'sm': '1',
#                 'columnCN': '',
#                 'p': '0',
#                 'timetype': 'timeyn'
#             }
# url = 'https://searching.hunan.gov.cn/hunan/001000000/file?' + urlencode(params)
# headers = {'User-Agent': str(UserAgent().random)}
# response = requests.get(url, headers=headers)
# response.encoding = "utf8"
# html = etree.HTML(response.text)
#
# rows = html.xpath('//div[@class="boxlist-main"]/div[@class="resultbox"]')
# if len(rows) != 0:
#     for row in rows:
#         created_date = row.xpath('./ul/li[4]/p/text()')[0]
#         print(created_date)

# url = 'http://ydyl.hunan.gov.cn/ydyl/fgzc/gnflfgzc/202103/t20210326_15075096.html'
url = 'http://www.hunan.gov.cn/zqt/zcsd/202201/t20220114_22462387.html'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = "utf8"
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                  for i in html.xpath('//div[@class="content"]//p//text()|//div[@class="detail-txt"]/p//text()|//div[@class="tys-main-zt-show"]/p//text()'))

print(response.text)
print(content)

