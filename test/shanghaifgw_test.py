import requests
from lxml import etree

url = 'https://ss.shanghai.gov.cn/fgwxxgk/search?q=%E7%BB%BF%E8%89%B2%E4%BD%8E%E7%A2%B3&publishStartDate=2022-02-01&publishEndDate=2022-02-28&searchType=fgwSearch&page=1&contentScope=2&dateOrder=2&tr=1&format=1&uid=0000017d-a20b-5fb2-e255-77dd586307b3&sid=0000017d-a20b-5fb2-7cc2-30c52f89b3f3&re=2&all=1&siteId=zwgk.fgw.sh.gov.cn'
result = requests.get(url)
response = etree.HTML(result.text)
rows = response.xpath('//div[@class="result "]')

if len(rows) != 0:
    for row in rows:
        created_date = row.xpath('.//div[@class="content"]/font[1]/text()')[0]
        print(created_date)

print(result.text)