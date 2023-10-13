import urllib3
import requests
from lxml import etree
import csv

# 1.定义要爬取的页面
urls = ["https://javdb.com/actors/3JwN?page=2&sort_type=0&t=d%2C15"]
for i in range(2, 5):
# 2.定义页码
    url = 'https://javdb.com/actors/3JwN?page=' + str(i)+'&sort_type=0&t=d%2C15'
    urls.append(url)

# 定义csv文件的表头
csv_file = open('qianjing.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['标题', '内容'])

# 开始爬取
content = ""
for url in urls:
    urllib3.disable_warnings()
    response = requests.get(url,verify=False)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    titles = html.xpath('//div[@class="video-title"]/strong/text()')
    links = html.xpath('//div[@class="item"]/a/@href')
    real = 'https://javdb.com'
    for link in links:
#(//a[.//span[@class="tag is-warning is-small is-light"]])[1]/@href
        reallink=real+link
        response = requests.get(reallink)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        subtitle_span_text = html.xpath('(//span[contains(@class, "tag is-warning is-small is-light")]/text())[1]')

        if subtitle_span_text and "字幕" in subtitle_span_text[0]:
            # 如果包含"字幕"，获取其父<a>标签的href链接
            content = html.xpath(
                '(//span[contains(@class, "tag is-warning is-small is-light")]/text())[1]/ancestor::a/@href')
            content = ''.join(content)
            writer.writerow([titles[links.index(link)], content])
        else:
            # 如果没有找到包含指定class的<span>标签，获取十个中的第一个链接
            # 如果不包含字幕，获取第一个<a>标签的href链接
            content = html.xpath('(//div[@class="magnet-name column is-four-fifths"]/a)[1]/@href')
            content = ''.join(content)
            writer.writerow([titles[links.index(link)], content])


csv_file.close()