from xml import etree
import requests
from fake_useragent import UserAgent
from lxml import etree
from pyquery import PyQuery as pq

url = 'http://www.hvacjournal.cn/Category_25/Index_1.aspx'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = 'utf8'
print(response.text)

html = etree.HTML(response.text)
rows = html.xpath('//div[@class="listBox"]/li')

if len(rows) != 0:
    for row in rows:
        if row != rows[5] and row != rows[11] and row != rows[17]:
            created_date = row.xpath('./span/text()')[0].strip()
            # title = row.xpath('.//span[@class="title"]/text()')[0].strip()
            # url = row.xpath('.//a[@class="bdurl"]/@href')[0].strip()
            # keywords = ','.join(i.strip() for i in row.xpath('.//div[@class="d3"]/div[@class="fl"]/a/text()'))

            print(created_date)