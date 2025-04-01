import requests
import urllib3
from lxml import etree
import csv
import time
# 禁用 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 1. 定义要抓取的URL
urls = ["https://javdb.com/actors/AvaP?page=14"]
urls += [f'https://javdb.com/actors/AvaP?page={i}' for i in range(15, 21)]

# 2. 定义CSV文件及标题
with open('jiazisha1.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['标题', '内容'])

    # 3. 定义请求函数，带重试机制
    def fetch_with_retries(url, retries=10):
        for attempt in range(retries):
            try:
                response = requests.get(url, verify=False)
                response.encoding = 'utf-8'
                return response
            except requests.RequestException as e:
                print(f"尝试第 {attempt + 1} 次请求 {url} 失败: {e}")
                time.sleep(1)  # 等待1秒后再重试
        print(f"请求 {url} 仍然失败，已达到最大重试次数。")
        return None  # 返回空以指示失败

    # 4. 开始抓取数据
    for url in urls:
        response = fetch_with_retries(url)
        if response is None:
            continue  # 如果请求失败，跳过当前URL

        html = etree.HTML(response.text)
        titles = html.xpath('//div[@class="video-title"]/strong/text()')
        links = html.xpath('//div[@class="item"]/a/@href')
        real = 'https://javdb.com'

        for link in links:
            reallink = real + link
            response = fetch_with_retries(reallink)
            if response is None:
                continue  # 如果请求失败，跳过当前视频链接

            html = etree.HTML(response.text)

            subtitle_span_text = html.xpath('(//span[contains(@class, "tag is-warning is-small is-light")]/text())[1]')
            if subtitle_span_text and "字幕" in subtitle_span_text[0]:
                content = html.xpath('(//span[contains(@class, "tag is-warning is-small is-light")]/text())[1]/ancestor::a/@href')
                content = ''.join(content)
            else:
                content = html.xpath('(//div[@class="magnet-name column is-four-fifths"]/a)[1]/@href')
                content = ''.join(content)

            # 写入标题和内容到CSV
            writer.writerow([titles[links.index(link)], content])

            # 为了尊重服务器，延迟请求
            time.sleep(1)  # 在请求之间睡眠1秒