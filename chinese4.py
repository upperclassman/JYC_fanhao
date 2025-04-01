from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from bs4 import BeautifulSoup

# 启动浏览器
driver = webdriver.Chrome()  # 确保您已安装适合版本的 ChromeDriver
driver.get('https://accounts.douban.com/passport/login')

# 等待用户名输入框加载
try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    username.send_keys('15949594501')  # 输入用户名
except Exception as e:
    print(f"发生错误: {e}")

# 等待用户输入验证码
input("请完成验证码并按 Enter 键来继续...")

# 访问评论页面
driver.get('https://movie.douban.com/subject/36534110/comments?status=P')

# 用于存储所有评论的列表
all_comments = []

# 翻页爬取
while True:
    # 获取页面内容
    time.sleep(2)  # 等待页面加载
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 找到所有评论
    comments = soup.find_all('span', class_='short')

    # 如果没有更多评论，则停止
    if not comments:
        break

        # 提取评论文本
    for comment in comments:
        all_comments.append(comment.text)

        # 查找“下一页”按钮并点击，如果没有则退出
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
        next_button.click()
        time.sleep(2)  # 等待下一页加载
    except Exception as e:
        print("没有找到下一页，停止爬取:", e)
        break

    # 关闭浏览器
driver.quit()

# 创建 DataFrame
df = pd.DataFrame(all_comments, columns=['评论'])

# 保存到 Excel 文件
file_name = 'douban_comments.xlsx'
df.to_excel(file_name, index=False)

# 提示保存状态
if not df.empty:  # 检查 DataFrame 是否为空
    print(f"所有评论已成功保存到 {file_name}")
else:
    print("没有评论可保存，文件未生成。")