import requests
from lxml import etree
from werkzeug.user_agent import UserAgent

url = 'http://www.vkhvacr.com/detail/44728.html'
response = requests.get(url=url)
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//div[@class="w-68 left"]/div[@class="content"]/p/text()'))
print(content)