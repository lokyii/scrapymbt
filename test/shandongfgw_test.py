import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'http://fgw.shandong.gov.cn/art/2022/2/25/art_91410_10343188.html'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = "utf8"
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                  for i in html.xpath('//div[@class="art_con"]//p//text()'))

print(response.text)
print(content)