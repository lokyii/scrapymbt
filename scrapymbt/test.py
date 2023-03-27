# -*- coding: utf-8 -*-
import datetime
import json
import re
import threading
import time
import math
from scrapymbt.settings import *
from scrapymbt.process import Value, FindStr

import requests
from lxml import etree
from fake_useragent import UserAgent


# headers={'User-Agent': str(UserAgent().random)}
# params = {
#             'q': '',
#             't': 'govall',
#             'advance': True,
#             'orpro': '碳达峰',
#             'andpro': '',
#             'notpro': '',
#             'inpro': '',
#             'pubmintimeYear': 2022,
#             'pubmintimeMonth': 1,
#             'pubmintimeDay': '',
#             'pubmaxtimeYear': 2022,
#             'pubmaxtimeMonth': 1,
#             'pubmaxtimeDay': '',
#             'searchfield': '',
#             'colid': '',
#             'timetype': 'timeqb',
#             'mintime': '',
#             'maxtime': '',
#             'sort': 'pubtime',
#             'sortType': 1,
#             'nocorrect': ''
# }
# response = requests.get('http://sousuo.gov.cn/s.htm?', params=params, headers=headers)
# response.encoding = "utf8"
# html = etree.HTML(response.text)
# rows = response.json()
# for row in rows['page']['content']:
#     created_date = row['PUBDATE'][:10]
#     print(created_date)
#     content = row['DOCCONTENT'].replace('\r', '').replace('\u3000', '').replace(u'\xa0', '').replace('\n', '')
#     print(content)
# print(response.text)


# from datetime import datetime
#
#
# currentMonth = datetime.now().month
# currentYear = datetime.now().year
#
# print(currentYear, currentMonth)
#
# import datetime
# import dateutil.relativedelta
# now = datetime.datetime.now()
# date = now + dateutil.relativedelta.relativedelta(months=-1)#上个月时间
# print(date)

title = "北京市发展和改革委员会关于印发进一步加强数据中心项目节能审查若干规定的通知"
content = "为从源头上推动数据中心持续提高能效碳效水平，强化全生命周期节能管理，促进数据中心高质量发展，高水平支撑数字经济标杆城市建设，根据《中华人民共和国节约能源法》《固定资产投资项目节能审查办法》(国家发展改革委令2016年第44号)、《关于优化营商环境调整完善北京市固定资产投资项目节能审查的意见》(京发改规〔2017〕4号)，研究制定了《关于进一步加强数据中心项目节能审查的若干规定》，现印发给你们，请认真贯彻执行。"
title_kw = Value(title, PROVINCE_POLICY_KW).return_multi_kw()
title_kw_num = Value(title, PROVINCE_POLICY_KW).keyword_count()
content_kw = Value(content, PROVINCE_POLICY_KW).return_multi_kw()
content_kw_num = Value(content, PROVINCE_POLICY_KW).keyword_count()
print(title_kw, title_kw_num)
print(content_kw, content_kw_num)