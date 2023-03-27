import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'http://fzgg.tj.gov.cn/zwgk_47325/zcfg_47338/zcwjx/fgwj/202202/t20220223_5811773.html'
response = requests.get(url=url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in html.xpath('//*[@id="xlrllt"]/div/div[1]//p//text()'))

print(response.text)
print(content)

