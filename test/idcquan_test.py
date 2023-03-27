from xml import etree
import requests
from fake_useragent import UserAgent
from lxml import etree
from pyquery import PyQuery as pq

url = 'http://www.idcquan.com/review/1.shtml'
# url = 'http://news.idcquan.com/index6_2.shtml'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = 'utf8'
# response.encoding = 'unicode_escape'
print(response.text)

# html = etree.HTML(response.text)
# rows = html.xpath('//div[@class="news clearfix"]')
# if len(rows) != 0:
#     for row in rows:
#         created_date = row.xpath('./span[@class="date"]/text()')[0].strip()[:10]
#         title = row.xpath('.//span[@class="title"]/text()')[0].strip()
#         url = row.xpath('.//a[@class="bdurl"]/@href')[0].strip()
#         keywords = ','.join(i.strip() for i in row.xpath('.//div[@class="d3"]/div[@class="fl"]/a/text()'))
#
#         print(created_date, title, url, keywords)

# url = 'http://news.idcquan.com/tx/193197.shtml'
# url = 'http://news.idcquan.com/news/193196.shtml'
# url = 'http://news.idcquan.com/gjzx/193170.shtml'
url = 'http://www.idcquan.com/xw/194864.shtml'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = "utf8"
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                  for i in html.xpath('//div[@class="clear deatil article-content fontSizeSmall BSHARE_POP"]/p//text()'))
print(content)


# url = 'http://www.idcquan.com/tech/index_1.shtml'
# print(url.split(".")[-2][-1], type(url.split(".")[-2][-1]))