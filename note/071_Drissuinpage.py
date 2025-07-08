from DrissionPage import Chromium,ChromiumPage
# 新方法
browser =Chromium()
page = browser.latest_tab
# page.get("https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number=%206406920901")
page.get("https://www.baidu.com")

#browser.quit()或者ab.close()
##老方法
# browser =ChromiumPage()
# browser.get("https://www.baidu.com/")
# page.ele('x://*[@id="kw"]').input("python")
# page.ele('x://*[@id="su"]').click()
# print(page.ele('tag:input').attr('name'))
# for tag_p in page.eles("x://body//p"):
#     print(tag_p.text)
#精确匹配
#https://www.bilibili.com/video/BV1ut421M7T1/?spm_id_from=333.788.player.switch&vd_source=2e750606d6f336aa5b5186e2fecafc53
# print(page.ele('@class=title-content-title').text)
# #模糊匹配
# print(page.ele('@class:title-content-title').text)

import logging
import pytz
from datetime import datetime

# 创建一个时区对象（北京时间）
tz = pytz.timezone('Asia/Shanghai')

# 自定义时间格式
class BeijingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # 获取当前时间并转换为北京时间
        ct = datetime.fromtimestamp(record.created, tz)
        return ct.strftime('%Y-%m-%d %H:%M:%S')

# 设置日志配置
logging.basicConfig(level=logging.INFO)

# 创建logger对象
logger = logging.getLogger(__name__)

# 创建handler（控制台输出）
console_handler = logging.StreamHandler()

# 使用自定义的北京时区时间格式
formatter = BeijingFormatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 将handler添加到logger
logger.addHandler(console_handler)

logger.info("开始定位元素标签")

# 假设 page.ele 是你用来定位元素的方法
# if page.ele('@class=title-content-title'):
#     print(page.ele('@class=title-content-title').text)
#     logger.info("定位成功")
# else:
#     logger.error("定位失败")

#获取标签属性值
# print(page.ele('x://*[@id="s-top-more"]/div[1]/a[1]/img').attr('src'))

#超时参数
page.ele('x://*[@id="s-top-more"]/div[1]/a[1]/img',timeout=1).attr('src')

#XPATH语法
# blog.csdn.net/weixin 43411585/article/details/128908199

#设定浏览器路径
# co = Chromiumoptions().set_paths(browser_path=r"C:\ProgramFiles(x86)\Microsoft\Edge\Application\msedge.exe")

# #默认情况下，程序使用 9222 端日 浏览器可执行文件路径为'chrome'
# page =ChromiumPage(co) 
# #创建对象# 
# page.get('http://g1879.gitee.io/DrissionPageDocs')
# # 案例1,尝试3次，间隔2秒
# page.get( ur: 'http://g1879.gitee.io/DrissionPageDocs', retry=3, interval=2,timeout=15) 

# #获取html
# print(">>>>>>>>>>>>>>>>>>>>>>>>\n当前概述html", page.html)
# print(">>>>>>>>>>>>>>>>>>>>>>>>\n当前概述html", page.ele('x://*[@id=“-概述"]').html)
# print(">>>>>>>>>>>>>>>>>>>>>>>>\n当前版本信息text",page.ele('x://p[contains(text(),"最新版本")]').text)
# print(">>>>>>>>>>>>>>>>>>>>>>>>\ngit链接属性值",page.ele('x://p[contains(text(),"项目地址")]/a').attr('href'))
# #page.quit() #关闭浏览器
# print(f">>>(n当前对象控制的列面地址和端口:fpage.addreshn测胞器请求头:fpage.user_agent;n是否正在加状态:fpage.states.is_loading)fpage.states.ready_state)")


#案例2熟悉
page.get(url='https://www.baidu.com', retry=3, interval=2, timeout=15)

page.ele('x://*[@id="kw"]').input('DrissionPage') 
# 输入文本
page.ele('x://input[@id="su"]').click() 
# 点击按钮
page.wait.load_start() 
#等待页面跳转
links =page.eles('x://h3') 
# 获取所有结果
for link in links: 
#遍历并打印结果
    print("标题",link.text,"链接",link.ele("x:/a").attr('href'))