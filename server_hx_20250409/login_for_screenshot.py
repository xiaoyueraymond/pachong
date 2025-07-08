from DrissionPage import ChromiumPage, ChromiumOptions
import pdb
import time
from mytools import get_datetime_str
co = ChromiumOptions()
# co.set_argument('--start-maximized')

timestamp = get_datetime_str()

def get_full_page_screenshot(instance,keyword,addtional_str):
    """
    instance: page view
    keyword: text in the page that is clickable
    addtional_str : to identify the proc ,like 20240_06_18_180818
    """
    # time.sleep(1)
    mystr = f"tx:{keyword}"
    instance.ele(mystr).click()
    time.sleep(2)
    path = f"d:\\logs\\{timestamp}_{keyword}.jpg"
    instance.get_screenshot(path=path,full_page=True)
    return

# 创建页面对象，并启动或接管浏览器

page = ChromiumPage(addr_or_opts=co)


#
# 跳转到登录页面
page.get('https://192.168.2.100')
try:
    page.ele(('id','navLanguageLabel')).click()
    page.ele(('id','en-US')).click()
    print("successfully change the language to english!!!")
    # page.ele()
except:
    pass


# 定位到账号文本框，获取文本框元素
ele = page.ele('#account')
# 输入对文本框输入账号
ele.input('Administrator')
# 定位到密码文本框并输入密码
page.ele('#loginPwd').input('Admin@9000')
# 点击登录按钮
# get_full_page_screenshot(page,"login",timestamp)
login_file =  f"d:\\logs\\{timestamp}_login.jpg"
page.get_screenshot(path=login_file,full_page=True)
page.ele('#btLogin').click()
#
print("successfully login with default username: Administrator and password: Admin@9000")
#
time.sleep(8)
# 尝试关闭IP登录信息
#
# pdb.set_trace()
# try:
page.ele("tx:Home").click()
time.sleep(3)
get_full_page_screenshot(page,"Home",timestamp)
# page.get_screenshot(path='homepage.jpg',full_page=True)
myele = page.ele(('id','app'))
myele.get_screenshot(path='d:/homepage.jpg')
time.sleep(3)
pdb.set_trace()
#
page.ele("tx:System").click()
time.sleep(3)
get_full_page_screenshot(page,"System",timestamp)
# page.get_screenshot(path='System.jpg',full_page=True)
# pdb.set_trace()
page.ele("tx:Processors").click()
time.sleep(3)
get_full_page_screenshot(page,"Processors",timestamp)
# page.get_screenshot(path='Processors.jpg',full_page=True)
#Memory
time.sleep(3)
get_full_page_screenshot(page,"Memory",timestamp)
time.sleep(3)
get_full_page_screenshot(page,'Network Adapter',timestamp)
#
#

