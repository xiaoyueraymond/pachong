import urllib.request
import ccxt
from datetime import datetime
import pytz
import time
import sys  # Import sys to enable exiting the program
from pytz import timezone
import logging
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Get the current Python script file path
current_script_path = os.path.abspath(sys.argv[0])
current_script_directory = os.path.dirname(current_script_path)


# Specify the log file's relative path
log_file_path = os.path.join(current_script_directory, 'temp.log')

# Create a custom Formatter class to convert time to Beijing time
class BeijingTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        beijing_tz = timezone('Asia/Shanghai')
        return dt.astimezone(beijing_tz)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.strftime('%Y-%m-%d %H:%M:%S')

# Create log logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the log recording level to DEBUG

# Create a file handler, specify a log file path and encoding
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)  # Set the file handler level to WARNING
file_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create a stream handler to output logs to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Set the stream handler level to DEBUG
stream_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

l = logger


# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(service=Service(r'D:\python\note\chromedriver-win64\chromedriver.exe'))
wd.get('https://www.byhy.net/cdn2/files/selenium/sample1.html')
# 根据id选择元素，返回的就是该元素对应的WebElement对象

try:
    element = wd.find_element(By.ID, 'searchtext')
    # 点击
    element.click()
except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(0.3)

element = wd.find_element(By.ID, 'searchtext')
element.clear()
element.send_keys('科技')


elements = wd.find_elements(By.CLASS_NAME,'plant')
logger.debug(elements)

for i in elements:
    logger.debug(i)
# # 通过该 WebElement对象，就可以对页面元素进行操作了
# # 比如输入字符串到 这个 输入框里
# # element.send_keys('通讯\n')

# #关闭网页
elements_span =wd.find_elements(By.TAG_NAME,'span')
for i in elements_span:
    l.debug(i.text)



#在元素内部找内容

element = wd.find_element(By.ID,'container')
spans = element.find_elements(By.TAG_NAME,'span')
for span in spans:
    print(span.text)




#隐式等待
wd.implicitly_wait(10)
# 关闭浏览器
wd.quit()