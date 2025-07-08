from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


chrome_options = Options()
path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# chrome_options.add_argument("--no-proxy-server")  # 禁用代理
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

service = Service(r'D:\python\note\chromedriver-win64\chromedriver.exe')

browser = webdriver.Chrome(service=service, options=chrome_options)
url = 'https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number=%206406920901'
browser.get(url)
# browser.save_screenshot(r'D:\python\note\083_baidu.png')
import time
time.sleep(2)
input("按下任意键退出浏览器...")
browser.quit()