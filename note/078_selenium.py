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

button = browser.find_element(By.ID, 'su')
# content = browser.page_source
# print(button)
# button = browser.find_element(By.XPATH,'//iput[@id="kw"]')
# print(button)
# button = browser.find_element(By.TAG_NAME,'input')
# print(button)
# button = browser.find_element(By.CSS_SELECTOR,'kw')
print(button)
#https://www.youtube.com/watch?v=ylgStw0jxrc&list=PLmOn9nNkQxJH39Kc0suTsx7qxMGc_Cp1-&index=80
#获取标签的属性
print(button.get_attribute('class'))
print(button.tag_name)
a = browser.find_element(By.LINK_TEXT,'新闻')
print(a.text)
# input("按下任意键退出浏览器...")
# browser.quit()