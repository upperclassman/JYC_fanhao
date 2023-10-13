import requests
from lxml import etree
import csv

# 定义要爬取的页面
urls = ['http://fanfu.people.com.cn/index1.html']
for i in range(1, 8):
    url = 'http://fanfu.people.com.cn/index' + str(i) + '.html'
    urls.append(url)

# 定义csv文件的表头
csv_file = open('news2.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['标题', '内容'])

# 开始爬取
for url in urls:
    response = requests.get(url)
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    titles = html.xpath('//div[@class="fl"]/ul/li/a/text()')
    links = html.xpath('//div[@class="fl"]/ul/li/a/@href')
    real = 'http://fanfu.people.com.cn/index'
    for link in links:

        reallink=real+link
        response = requests.get(reallink)
        response.encoding = 'gbk'
        html = etree.HTML(response.text)
        content = html.xpath('//div[@class="show_text"]/p/text()')
        content = ''.join(content)
        writer.writerow([titles[links.index(link)], content])

csv_file.close()