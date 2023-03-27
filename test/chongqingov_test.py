import datetime
import random
import time

import requests
from fake_useragent import UserAgent
from lxml import etree
from requests_html import HTMLSession

from scrapymbt.settings import *

# now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
# START_DATE = START_DATE + ' 00:00:00'
# END_DATE = END_DATE + ' 23:59:59'
#
# start_date_array = time.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
# beginDateTime = str(int(time.mktime(start_date_array)) * 1000)
# end_date_array = time.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
# endDateTime = str(int(time.mktime(end_date_array)) * 1000)
#
# # param_list[0]为市政府参数，param_list[1]为市发改委参数
# param_list = [{"tenantId": "7", "areaCode": ""}, {"tenantId": "85", "areaCode": "500000112"}]
#
# value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
# headers = {
#             'Host': 'www.cq.gov.cn',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
#             'Accept': 'application/json, text/javascript, */*; q=0.01',
#             'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#             'Accept-Encoding': 'gzip, deflate',
#             'Content-Type': 'application/json',
#             'X-Requested-With': 'XMLHttpRequest',
#             'Content-Length': '549',
#             'Origin': 'http://www.cq.gov.cn',
#             'Connection': 'keep-alive',
#             'Referer': 'http://www.cq.gov.cn/cqgovsearch/search.html?searchWord=%E7%A2%B3&tenantId=7&configTenantId=7&dataTypeId=9&sign=0467d3a6-9d03-4df6-d32d-8c260c1370ab&pageSize=10&seniorBox=0&advancedFilters=&isAdvancedSearch=0',
#             'Cookie': 'SESSION=NGRkNjdhYzAtM2ZiNy00ODdlLWFlYWEtZTViN2QyMTk2Njhh; _trs_uv=kzgsb84t_3486_6h4v; JSESSIONID=A40DBF234651ABD9BF215F2A5D4B1C31; _trs_user=; _trs_ua_s_1=kzi25awu_3486_cv2p; td_cookie=2501488204'
#
# }
#
# data = {"id":"7","tenantId":7,"searchWord":"碳","dataTypeId":"9","pageNo":1,"pageSize":"10","orderBy":"related","searchBy":"title","appendixType":"","granularity":"ALL","beginDateTime":"","endDateTime":"","isSearchForced":0,"filters":[],"pager":{},"searchInfo":{},"dataTypes":[],"configTenantId":"7","historySearchWords":["碳","碳中和","绿色建筑","数据中心"],"operationType":"search","seniorBox":"0","isDefaultAdvanced":0,"isAdvancedSearch":0,"advancedFilters":[],"customFilters":[],"areaCode":""}
#
# url = 'http://www.cq.gov.cn/irs/front/search'

url = 'http://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/xzgfxwj/szf/202201/t20220124_10334603.html'
response = requests.get(url, headers={'User-Agent': str(UserAgent().random)})
response.encoding = 'utf-8'
html = etree.HTML(response.text)
content = ''.join(i.strip().replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace(u'\u2002', '')
                                  for i in html.xpath('//div[starts-with(@class,"view TRS_UEDITOR trs_paper_default")]//p//text()'))
print(response.text)
print(content)




