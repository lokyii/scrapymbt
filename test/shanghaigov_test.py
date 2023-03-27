import requests
from lxml import etree
from fake_useragent import UserAgent

url = 'https://search.sh.gov.cn/searchResult'
data = {
    'text': "绿色工业",
    'pageNo': "1",
    'newsPageNo': "2",
    'pageSize': "20",
    'resourceType': "",
    'channel': "政务公开",
    'category1': "",
    'category2': "",
    'category3': "",
    'category4': "",
    'category5': "",
    'category6': "xxgk",
    'category7': 'www.shanghai.gov.cn',
    'sortMode':	"2",
    'searchMode': "",
    'timeRange': "4",
    'accurateMode': "",
    'district': "",
    'street': "",
    'stealthy':	"1",
    'searchText': "建筑节能"
}
headers = {'User-Agent': str(UserAgent().random)}
response = requests.post(url, data=data, headers=headers)
response.encoding = "utf8"
html = etree.HTML(response.text)
rows = html.xpath('//div[@class="result result-elm"]')
for row in rows:
    created_date = row.xpath('.//div[@class="entry-news-content"]/div[1]/font[1]/text()|./div[@class="restcont"]/div[1]/font[1]/text()')[0].strip()
    title = row.xpath('./a/@title')[0].strip()
    print(created_date, title)