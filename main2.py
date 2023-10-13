import urllib3
import requests
from lxml import etree
import csv

# 1.定义要爬取的页面
urls = ["https://javdb.com/actors/VgzW?page=1"]
for i in range(2, 11):
# 2.定义页码
    url = 'https://javdb.com/actors/VgzW?page=' + str(i)
    urls.append(url)

# 定义csv文件的表头
csv_file = open('yitiaoqimeixiang.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['标题', '内容'])

# 开始爬取
for url in urls:
    urllib3.disable_warnings()
    response = requests.get(url,verify=False)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    titles = html.xpath('//div[@class="video-title"]/strong/text()')
    links = html.xpath('//div[@class="item"]/a/@href')
    real = 'https://javdb.com'
    for link in links:

        reallink=real+link
        response = requests.get(reallink)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        content = html.xpath('(//div[@class="magnet-name column is-four-fifths"]/a)[1]/@href')
        content = ''.join(content)
        writer.writerow([titles[links.index(link)], content])

csv_file.close()