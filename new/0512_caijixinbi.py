from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import os
import os
from datetime import datetime


# 获取今天的日期
today_date = time.strftime("%Y%m%d")  # Get today's date in YYYYMMDD format

# 初始化浏览器并获取最新的标签页
browser = Chromium()
page = browser.latest_tab
# mexc_url = "https://www.mexc.com/zh-TW/support/categories/360000254192?handleDefaultLocale=keep"

def mexc_get_url():
    # 设置文件路径
    
    mexc_url = "https://www.mexc.com/zh-TW/newlisting"

    # 假设这里使用了某个浏览器自动化工具（例如 selenium）来获取页面元素
    page.get(mexc_url)
    elements_symbols = page.eles("x://div[@class='name card_withEllipsis__pZ_OY']", timeout=1)
    elements_time = page.eles("x://div[@class='time card_value__Q83Tj']", timeout=1)

    # 读取文件中的已有 URL 列表
    if os.path.exists(mexc_symbol_path_1):
        with open(mexc_symbol_path_1, 'r', encoding='utf-8') as file:
            existing_urls = file.read().splitlines()
    else:
        existing_urls = []

    symbols_list=[]
    # 遍历获取的元素并构建 URL
    for i in range(len(elements_symbols)):
        search_url = elements_symbols[i].text + "|" + elements_time[i].text
        symbols_list.append(elements_symbols[i].text + "/USDT")
        print(search_url)
        # 检查 URL 是否已经存在，若不存在则添加到文件
        # if search_url not in existing_urls:
        #     with open(mexc_symbol_path_1, 'a', encoding='utf-8') as file:
        #         file.write(search_url + '\n')
        #     existing_urls.append(search_url)  # 更新已有的 URL 列表
    
    print(symbols_list)



def mexc_get_url_search():

    # Read existing hrefs to avoid duplicates
    existing_hrefs = set()
    if os.path.exists(mexc_symbol_search_path_2):
        with open(mexc_symbol_search_path_2, 'r', encoding='utf-8') as f:
            existing_hrefs = {line.strip() for line in f if line.strip()}

    # Read URLs/queries from input file
    queries = []
    if os.path.exists(mexc_symbol_path_1):
        with open(mexc_symbol_path_1, 'r', encoding='utf-8') as f:
            queries = [line.strip() for line in f if line.strip()]
    else:
        print(f"Input file {mexc_symbol_path_1} not found.")
        return

    # Assuming page is a global or pre-initialized browser automation object
    for query in queries:
        try:
            # Navigate to the search page
            page.get(query)
            # Assuming page.get includes a wait for page load; add delay if needed
            page.wait.load_start()

            # Locate the element with text "陽光普照"
            # page.ele('x://input[@id="su"]').click() 
            elements = page.eles('x://ul[@class="search_searchResult-community__YBtQM"]//li//a')
            for ele in elements:
                href =  ele.attr('href')
                if href and href not in existing_hrefs:
                    # Append new href to the output file
                    with open(mexc_symbol_search_path_2, 'a', encoding='utf-8') as f:
                        f.write(f"{href}\n")
                    existing_hrefs.add(href)
                    print(f"Saved href: {href}")
                else:
                    print(f"{href}已经存在")
        except Exception as e:
            print(f"Error processing {query}: {str(e)}")


mexc_symbol_path_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"mexc_symbol_path_1_{today_date}.txt")
mexc_symbol_search_path_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"mexc_symbol_search_path_2_{today_date}.txt")
# 调用函数
mexc_get_url()


