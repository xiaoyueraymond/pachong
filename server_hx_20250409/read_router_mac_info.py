from DrissionPage import SessionPage
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

page = SessionPage()


#
# 跳转到登录页面
page.get('https://192.168.3.1')
pdb.set_trace()
try:
    print("start to login the router")
    page.ele('#userpassword_ctrl').input("852963nwt@")
    print("after enter the password")
    page.ele('#loginbtn').click()
    print("successfully change the language to english!!!")
    # page.ele()
except:
    pass

print("successfully login with default username: Administrator and password: Admin@9000")
#
time.sleep(3)
# 尝试关闭IP登录信息
#
# pdb.set_trace()
# try:

# time.sleep(3)
# get_full_page_screenshot(page,"Home",timestamp)
# # page.get_screenshot(path='homepage.jpg',full_page=True)
# myele = page.ele(('id','app'))
# myele.get_screenshot(path='d:/homepage.jpg')
# time.sleep(3)
# pdb.set_trace()
# #
page.ele(("id","devicecontrol")).click()
pdb.set_trace()
# time.sleep(3)
# get_full_page_screenshot(page,"System",timestamp)
# # page.get_screenshot(path='System.jpg',full_page=True)
# # pdb.set_trace()
# page.ele("tx:Processors").click()
# time.sleep(3)
# get_full_page_screenshot(page,"Processors",timestamp)
# # page.get_screenshot(path='Processors.jpg',full_page=True)
# #Memory
# time.sleep(3)
# get_full_page_screenshot(page,"Memory",timestamp)
# time.sleep(3)
# get_full_page_screenshot(page,'Network Adapter',timestamp)
#
#

