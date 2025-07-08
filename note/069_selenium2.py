from selenium import webdriver
from selenium.webdriver.edge.service import Service

# # 设置 EdgeDriver 的路径
# PATH = "D:\\python\\note\\edge\\msedgedriver.exe"  # 使用完整的路径，包括 msedgedriver.exe
# service = Service(executable_path=PATH)

# # 初始化 WebDriver 并打开网页
# driver = webdriver.Edge(service=service)

# # 打开百度网站
# driver.get("http://www.baidu.com")
# # import os
# # print(os.path.exists("D:\\python\\note\\edge\\msedgedriver.exe"))

# 设置 EdgeDriver 的路径
PATH = "D:\\python\\note\\chromedriver-win64\\chromedriver.exe"  # 使用完整的路径，包括 msedgedriver.exe
service = Service(executable_path=PATH)

# 初始化 WebDriver 并打开网页
driver = webdriver.Chrome(service=service)

# 打开百度网站
driver.get("https://elines.coscoshipping.com")
input("按下任意键退出浏览器...")
driver.quit()
# import os

# print(os.path.exists("D:\\python\\note\\chrome-win64\\chromedriver.exe"))



