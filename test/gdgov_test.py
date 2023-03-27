import time

import requests
from lxml import etree
from fake_useragent import UserAgent

keyword = '绿色工业'

START_DATE = '2021-12-01' + ' 00:00:00'
END_DATE = '2021-12-31' + ' 23:59:59'

start_date_array = time.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
time_from = int(time.mktime(start_date_array))
end_date_array = time.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
time_to = int(time.mktime(end_date_array))

data = {
            "area": "",
            "dep": "",
            "division": "",
            "gb_end_time": "",
            "gb_fbjg": "",
            "gb_fwlb_wh": "",
            "gb_ppfs": "1",
            "gb_start_time": "",
            "gb_ztfl": "",
            "gdbsDivision": "440000",
            "keywords": keyword,
            "keywords_not": "",
            "onlineservice": "",
            "page": 1,
            "position": "all",
            "range": "site",
            "recommand": 1,
            "searchtype": "",
            "service_area": 1,
            "site_id": "2",
            "sort": "time",
            "time_from": time_from,
            "time_to": time_to,
            "type": ""
        }

url = 'https://search.gd.gov.cn/api/search/file'
response = requests.post(url=url, data=data, headers={'User-Agent': str(UserAgent().random)})
result = response.json()
rows = result['data']['list']
total_no = result['data']['total']
print(total_no, type(total_no))
# if len(rows) != 0:
#     for row in rows:
#         # print(row)
#         created_date = row['pub_time']
#         url = row['url']
#         title = row['title'].replace('<em>', '').replace('</em>', '').replace('&mdash;', '-')
#
#         print(created_date, url, title, )
#         print('***************************************')

# url = 'http://www.gd.gov.cn/gdywdt/gdyw/content/post_3774882.html'
# response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
# response.encoding = 'utf-8'
# # print(response.text)
# html = etree.HTML(response.text)
# content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '')
#                                   for i in html.xpath('//div[@class="article-content"]/p//text()|//div[@class="zw"]/p//text()'))
# print(content)
