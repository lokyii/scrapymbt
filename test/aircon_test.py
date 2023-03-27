from datetime import datetime
from lxml import etree
import requests
from fake_useragent import UserAgent

# times = '2022/5/24 9:14:00'
# t = times.split(" ")[0].replace("/", "-")
# t = datetime.strptime(t, '%Y-%m-%d').strftime('%Y-%m-%d')
# print(t, type(t))

url = 'http://www.aircon.com.cn/news/htmfiles/77116.shtml'
headers = {'User-Agent': str(UserAgent().random)}
response = requests.get(url, headers=headers)
response.encoding = "gb18030"
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                  for i in html.xpath('//*[@class="textblock"]//text()'))
print(content)