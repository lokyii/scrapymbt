from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent
from lxml import etree

params = {
                "page": "1",
                "view": "政务公开",
                "dsId": "www.ah.gov.cn",
                "dateOrder": "2",
                "format": "1",
                "contentScope": "2",
                "tr": "4",
                "startDate": "",
                "endDate": "",
                "includeKeywords": "",
                "excludeKeyword": "",
                "includeAllKeywords": "",
                "compWord": "",
                "searchType": "",
                "q": "优化"
            }
# url = 'https://www.ah.gov.cn/ahso/search?' + urlencode(params)
# headers = {'User-Agent': str(UserAgent().random)}
# response = requests.get(url, headers=headers)
# response.encoding = "utf8"
# html = etree.HTML(response.text)
#
# rows = html.xpath('//div[@class="mainResult"]/div[@class="result"]')
# if len(rows) != 0:
#     for row in rows:
#         created_date = row.xpath('./div[2]/div[1]/div/span/text()')[0].strip()
#         title = row.xpath('./div[1]/a/@title')[0].strip()
#         url = row.xpath('./div[1]/a/@href')[0].strip()
#
#         print(created_date, title, url)

# headers = {'User-Agent': str(UserAgent().random)}
# response = requests.get(url, headers=headers)
# response.encoding = "utf8"
# html = etree.HTML(response.text)
# content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
#                   for i in html.xpath('//*[@id="zoom"]/p//text()|//div[@class="detail-txt"]/p//text()|//div[@class="tys-main-zt-show"]/p//text()'))
#
# print(content)

# url = 'http://fzggw.ah.gov.cn/ywdt/ztzl/ahswdfzxdjh/zcfb/146429651.html'
# res = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
# res.encoding = 'utf-8'
# response = etree.HTML(res.text)
# content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
#                                   for i in response.xpath('//div[@class="wzcon j-fontContent"]//p//text()|//div[@class="j-fontContent newscontnet minh300"]/p//text()|//*[@id="zoom"]//text()|//div[@class="wenzhang_main j-fontContent"]/p//text()'))

url = 'https://www.ndrc.gov.cn/xxgk/jd/jd/202201/t20220125_1313163.html?code=&state=123'
res = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
res.encoding = 'utf-8'
response = etree.HTML(res.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
                                  for i in response.xpath('//div[starts-with(@class,"article_con")]//text()'))




print(content)




