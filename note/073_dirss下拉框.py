#https://www.bilibili.com/video/BV12b421H7Nf?spm_id_from=333.788.player.switch&vd_source=2e750606d6f336aa5b5186e2fecafc53
# 针对 select 标签的下拉列表
# dp提供了select类进行操作
# https://drissionpage.cn/ChromiumPage/ele operation/
#-点击列表顶元素进行选取针对单选的下拉框，每次仅能选择一个选项，可以在不同的选项中切换
# http://deal.ggzy.gov.cn/ds/deal/dealList.jsp

from DrissionPage import Chromium,ChromiumPage
# 新方法 
# articles.zsxq.com/id 80qs4ehgfz6t.html  说明文档
browser =Chromium() 
page = browser.latest_tab
# page.get("https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number=%206406920901")
page.get("https://www.baidu.com")


#g1879.gitee.io/drissionpagedocs/get start/installation 官方文档