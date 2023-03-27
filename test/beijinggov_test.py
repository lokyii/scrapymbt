import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'http://fgw.beijing.gov.cn/fzggzl/yfxz/xzxk_sgs/202202/t20220208_2606047.htm'
response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//*[@id="mainText"]/div//p//text()|//div[@class="xl_content"]/div//p//text()'))
print(response.text)
print(content)

