from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd

# 初始化浏览器并获取最新的标签页
browser = Chromium()
page = browser.latest_tab

url = 'https://www.marketwebb.blue/zh-CN/support/announcement/list/48'
page.get(url)

a = page.ele('x://h3[@class="typography-body1-1"]').text
print(a)