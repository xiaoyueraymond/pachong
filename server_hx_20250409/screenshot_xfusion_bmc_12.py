#!C:\Python312\python.exe
import pdb

from mytools import *
from selenium import webdriver
import argparse
from PIL import Image
import numpy as np
options = webdriver.ChromeOptions()
options.add_argument('--test-type')
# options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-urlfetcher-cert-requests')
#
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
import time
#
# image_save = ImageGrab.grab()
# D:\chrome-driver-125-06422
# driver_path = Service(executable_path=r"D:\ChromeDriver\chromedriver.exe")  # 122
driver_path = Service(executable_path=r"D:\chrome-driver-125-06422\chromedriver.exe")

driver = webdriver.Chrome(service=driver_path,options=options)
# zoom_out= "document.body.style.zoom='0.5'"
# driver.execute_script(zoom_out)
driver.maximize_window()
# driver.s
# zoom_out= "document.body.style.zoom='0.5'"
# driver.execute_script(zoom_out)
#
parser = argparse.ArgumentParser(description='Query  information from the xFusion iBMC ).')
parser.add_argument('-H', '--host', dest='host', default='192.168.3.126',
                    help='specify the IP Address or hostname of the target iBMC,default ip is 192.168.2.100')

args = parser.parse_args()
host =args.host
timestr = get_datetime_str()
##
if os.name == 'nt':
    if os.path.exists("d:"):
        logdir = 'd:\\logs\\'
    else:
        logdir = 'c:\\logs\\'
elif os.name == 'posix':
    logdir = '/tmp/'
else:
    msg = 'Can not determine the system arch, please contact the Developer for help'
    print(msg)
#
if not os.path.exists(logdir):
    os.mkdir(logdir)
    msg = f" {logdir} not exist ,now create it "
    mf.display(msg)
log_diag_dir = logdir + 'dump_info'
logfile = logdir + 'xfusion_redfish.log'

cmd = f"echo 123456 >{logfile}"
os.system(cmd)
loglevel = logging.INFO
# 提前设置好显式等待，作为一个统一入口
wait = WebDriverWait(driver,10)
prefix = f"{logdir}/{timestr}_"
homepage=prefix + "homepage.png"
sysinfo =prefix + "sysinfo.png"
processor = prefix +"processor.png"
memoryinfo = prefix + "memory.png"
networkinfo = prefix +"network.png"
other_info = prefix + "other.png"

# 测试数据准备
username  = "Administrator"
password  = "Admin@9000"

# 提前设置好显式等待，作为一个统一入口
host = args.host
url = 'https://' + host
driver.get(url)

# login_name
# login_pwd
# login_button_submit
# el = wait.until(EC.presence_of_element_located(('id','account')))
el = wait.until(EC.presence_of_element_located(('id','account')))
driver.find_element('id','navLanguageLabel').click()  ## memu language
driver.find_element('id','en-US').click() ## choose English
time.sleep(3)
# pdb.set_trace()
# driver.find_element()
# driver.find_element('xpath','//*[@id="languageID"]/a[1]').click()
# time.sleep(5)
# wait.until(EC.title_is('京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！'))
# driver.get_screenshot_as_file('d://jd首页.jpg')
# driver.find_element('id','account').send_keys(username)
# print('首页保存完成')
#
# order_el = driver.find_element("link text",'我的订单')
# order_el.click()
# time.sleep(3)
# name used for saved screenshot does not match file type. It should end with a `.png` extension
# driver.get_screenshot_as_file('d://jd订单.png')
# element_username.send_keys('Administrator')
driver.find_element('id','account').send_keys(username)
driver.find_element('id','loginPwd').send_keys(password)
driver.find_element('id','btLogin').click()

# element_password.send_keys('Admin@9000')

time.sleep(8)
# pdb.set_trace()

window_height = driver.get_window_size()['height']
print(f"window height is {window_height}")

page_height = driver.execute_script('return document.documentElement.scrollHeight')  # 页面高度
print(f"windows heigh:{window_height}   and  page heigh is {page_height}")

driver.save_screenshot('qq.png')

if page_height > window_height:
    n = page_height // window_height  # 需要滚动的次数
    base_mat = np.atleast_2d(Image.open('qq.png'))  # 打开截图并转为二维矩阵
    print(f"the first picture image is with hight == f{len(base_mat)} ,and result is f{len(base_mat[1])}")

    for i in range(n):
        driver.execute_script(f'document.documentElement.scrollTop={window_height * (i + 1)};')
        time.sleep(.5)
        driver.save_screenshot(f'qq_{i}.png')  # 保存截图
        mat = np.atleast_2d(Image.open(f'qq_{i}.png'))  # 打开截图并转为二维矩阵
        pdb.set_trace()
        print(f"the first picture image is with hight == f{len(mat)} ,and result is f{len(mat[1])}")
        base_mat = np.append(base_mat, mat, axis=0)     # 拼接图片的二维矩阵 axis=0 是垂直拼接，axis=1 是水平拼接
    Image.fromarray(base_mat).save('hao123.png')



driver.save_screenshot(homepage)
# pdb.set_trace()
# driver.find_element('link text','English').click()
time.sleep(8)
driver.find_element('link text','System').click()
driver.save_screenshot(sysinfo)
# image_save.save('d:/logs/peter_info.png')

time.sleep(8)
driver.find_element('id','infoTitelId').click()
# zoom_out= "document.body.style.zoom='0.5'"
# driver.execute_script(zoom_out)
time.sleep(8)
driver.save_screenshot(processor)

driver.find_element('id','memTitelId').click()
time.sleep(8)
driver.save_screenshot(memoryinfo)
# pdb.set_trace()
time.sleep(8)
driver.save_screenshot(sysinfo)
# driver.save_screenshot("")
# driver.save_screenshot(homepage)
time.sleep(300)

