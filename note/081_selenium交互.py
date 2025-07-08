from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--no-proxy-server")  # 禁用代理
service = Service(r'D:\python\note\chromedriver-win64\chromedriver.exe')

browser = webdriver.Chrome(service=service, options=chrome_options)
url = 'https://www.baidu.com'
browser.get(url)
import time 
time.sleep(2)
#获取文本框的对象
input2 = browser.find_element(By.ID,'kw')
input2.send_keys('周杰伦')
time.sleep(2)
button = browser.find_element(By.ID,'su')
button.click()
time.sleep(2)

# 滑到底部
js_bottom ='document.documentElement.scrollTop=100000'
browser.execute_script(js_bottom)
time.sleep(2)
#获取下一页的按钮
next = browser.find_element(By.XPATH,'//a[@class="n"]')
next.click()
time.sleep(2)
browser.back()
time.sleep(2)
browser.forward()
time.sleep(2)
# input("按下任意键退出浏览器...")
browser.quit()