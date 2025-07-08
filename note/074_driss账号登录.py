from DrissionPage import Chromium,ChromiumPage
# 新方法 
# articles.zsxq.com/id 80qs4ehgfz6t.html  说明文档
browser =Chromium() 
page = browser.latest_tab
# page.get("https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number=%206406920901")
page.get("https://www.baidu.com")

#案例3热悉陆
page.get(url= 'https://gitee.com/login', retry=3, interval=2, timeout=15)

#跳转到登录页面
if page.ele('x://input[@id="user_login"]'): 
#定位到账号文本框，获取文本框元素
    page.ele('x://input[@id="user_login"]').input("musk998")
    page.ele('x://input[@id="user_password"]').input("zhuan3000wan")
    page.ele('x://input[@value="登 录"]').click()


print('获取到cookies',page.cookies())

