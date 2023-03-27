import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'http://fgw.gxzf.gov.cn/zwgk/wjzx/zcjd/t11278018.shtml'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = "utf8"
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace(u'\u2002', '')
                  for i in html.xpath('//div[@class="article-con"]/div[1]//p//text()'))

print(response.text)
print(content)