from urllib.parse import urlencode
import requests
from fake_useragent import UserAgent
from lxml import etree
import time
import datetime

timestamp = int(round(time.time()*1000))

params = {
            "siteCode": "1400000045",
            "tab": "zcwj",
            "timestamp": timestamp,
            "wordToken": "b111854dd598da6241ea1c497600c452",
            "page": "1",
            "pageSize": "20",
            "qt": "\"绿色建筑\"",
            "timeOption": "2",
            "startDateStr": "2022-02-01",
            "endDateStr": "2022-02-28",
            "sort": "dateDesc",
            "keyPlace": "0",
            "fileType": "",
            "adv": "1"
}
url = 'https://api.so-gov.cn/s'
response = requests.post(url, data=params, headers={'User-Agent': str(UserAgent().random)})
# content = response.json()

print(response.text)
# print(content)