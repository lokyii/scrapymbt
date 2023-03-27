from urllib.parse import urlencode
import requests
from fake_useragent import UserAgent
from lxml import etree

# params = {
#                 'vc_name': '',
#                 'field_1218': "数据中心",
#                 'field_1244': '',
#                 'field_1243': "2022",
#                 'field_1222': '',
#                 'field_1221': '',
#                 'download': '',
#                 'strSelectID': '1221, 1222, 1235, 1243, 1244, 1245, 1344',
#                 'i_columnid': '107851',
#                 'field': 'vc_name:1:0,field_1218:1:0,field_1222:1:1,field_1243:1:0,field_1244:1:0,field_1245:1:,field_1221:1:0',
#                 'initKind': 'FieldForm',
#                 'type': '0, 0, 0, 0, 0, 0',
#                 'currentplace': '',
#                 'splitflag': '',
#                 'fullpath': '0'
#             }
# url = 'http://www.shandong.gov.cn/module/search/index.jsp?' + urlencode(params)
# res = requests.get(url=url, headers={'User-Agent': str(UserAgent().random)})
#
# res.encoding = 'utf-8'
# response = etree.HTML(res.text)
# rows = response.xpath('//div[@class="wip_col_listul"]/ul/li')
# if len(rows) != 0:
#     for row in rows:
#         created_date = row.xpath('./span/text()')[0].strip()[:10]
#         title = row.xpath('./a/text()')[0].strip()
#         detail_url = 'http://www.shandong.gov.cn/' + row.xpath('./a/@href')[0][6:]
#
#         detail_res = requests.get(detail_url, headers={'User-Agent': str(UserAgent().random)})
#         detail_res.encoding = 'utf-8'
#         detail_response = etree.HTML(detail_res.text)
#         content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '') for i in
#                           detail_response.xpath('//div[@class="wip_art_con"]/p//text()'))
#         print(created_date, title, url, detail_url, content)

url = 'http://www.shandong.gov.cn/art/2022/1/29/art_107851_117227.html'
res = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
res.encoding = 'utf-8'
response = etree.HTML(res.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '') for i in response.xpath('//div[@class="wip_art_con"]//p//text()'))

print(res.text)
print(content)