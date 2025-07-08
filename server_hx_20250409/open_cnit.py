#!C:\Python312\python.exe
from selenium import webdriver
#
options = webdriver.ChromeOptions()
options.add_argument('--test-type')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-urlfetcher-cert-requests')
#
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
#
driver_path = Service(executable_path=r"D:\ChromeDriver\chromedriver.exe")
driver = webdriver.Chrome(service=driver_path,options=options)
driver.maximize_window()

# 提前设置好显式等待，作为一个统一入口
wait = WebDriverWait(driver,10)

# 测试数据准备
username  = "admin"
password  = "admin#254"
url  = "https://192.168.3.116"

# 提前设置好显式等待，作为一个统一入口




driver.get(url)

# username
# password
# login_button_submit
el = wait.until(EC.presence_of_element_located(('id','username')))

driver.find_element('id','username').send_keys(username)
# element_username.send_keys('Administrator')
driver.find_element('id','password').send_keys(password)
# element_password.send_keys('Admin@9000')
#
driver.find_element('xpath','//*[@id="login-main"]/div[3]/div/div[2]/div[1]/form/button').click()
# element_submit.click()
# driver.maximize_window()
time.sleep(3600)