#!C:\Python312\python.exe
from selenium import webdriver
import argparse
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
#
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-H', '--host', dest='host', default='192.168.3.1',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')

args = parser.parse_args()
host =args.host

# 提前设置好显式等待，作为一个统一入口
wait = WebDriverWait(driver,10)

# 测试数据准备
username  = "Administrator"
password  = "852963nwt@"

# 提前设置好显式等待，作为一个统一入口
host = args.host
url = 'https://' + host
driver.get(url)

# login_name
# login_pwd
# login_button_submit
el = wait.until(EC.presence_of_element_located(('id','userpassword_ctrl')))

driver.find_element('id','userpassword_ctrl').send_keys(password)
# element_username.send_keys('Administrator')
driver.find_element('id','loginbtn').click()
# element_password.send_keys('Admin@9000')
# driver.maximize_window()
el = wait.until(EC.presence_of_element_located(('id','devicecontrol')))
driver.find_element('id','devicecontrol').click()
time.sleep(3600)
