import scrapy
from bs4 import BeautifulSoup



# class BaiduSpider(scrapy.Spider):
#     #爬虫的名字
#     name = "baidu"
#     #允许访问的域名
#     allowed_domains = ["https://www.byhy.net/auto/selenium/01/"]
#     #起始的URl的地址
#     start_urls = ["https://www.byhy.net/auto/selenium/01/"]

# #进入note 创建项目 scrapy genspider + 项目名 + 地址
# #关闭rboot协议# ROBOTSTXT_OBEY = True
# #进入note 创建项目 scrapy genspider baidu www.baidu.com
# #是执行了start urls之后 执行的方法方法中的response 就是返回的那个对象
# #相当于 response =urllib.request.urlopen()response =requests.get()


#     def parse(self, response):
#         print('--------------------------------test：scrapy crawl baidu-----------------------------------')
#         #获取响应的字符串
#         html_content = response.text
#         # print(content)
#         #获取二进制数据
#         content_erjinzhi = response.body
#         # print(content_erjinzhi)
#         soup = BeautifulSoup(html_content, 'html.parser')
#         print("-----------------------------------3------------------------------------")
#         # 找到 id 为 "_1" 的 <h2> 标签
#         md_content_div = soup.find('div', class_='md-content')

#         # 如果找到 md-content 内的 <div> 标签，继续查找第一个 <p> 标签
#         if md_content_div:
#             first_p_tag = md_content_div.find('p')
            
#             # 如果找到 <p> 标签，再查找其中的 <a> 标签
#             if first_p_tag:
#                 first_a_tag = first_p_tag.find('a')
                
#                 # 如果找到 <a> 标签，打印它的文本
#                 if first_a_tag:
#                     print(f"Text of the first <a> tag: {first_a_tag.get_text()}")
#                 else:
#                     print("没有找到 <a> 标签")
#             else:
#                 print("没有找到 <p> 标签")
#         else:
#             print("没有找到 class='md-content' 的 <div> 标签")
# #cd D:\python\note\scrapy_baidu_091\scrapy_baidu_091\spiders
# #scrapy crawl baidu

#-------------093汽车之家
# https://www.youtube.com/watch?v=7Kaq_ixKqJ4&list=PLmOn9nNkQxJH39Kc0suTsx7qxMGc_Cp1-&index=93

class BaiduSpider(scrapy.Spider):
    #爬虫的名字
    name = "baidu"
    #允许访问的域名
    allowed_domains = ["https://www.autohome.com.cn/price/brandid_15/"]
    #起始的URl的地址
    start_urls = ["https://www.autohome.com.cn/price/brandid_15/"]

    def parse(self, response):
        print('--------------------------------test：scrapy crawl baidu-----------------------------------')
        #获取响应的字符串
        # html_content = response.text
        # print(html_content)
        name_list = response.xpath('//a[@class="tw-text-hover tw-mr-2 tw-text-[18px] tw-font-[500]"]/text()')
        price_list = response.xpath('//a[@class="tw-text-[16px] tw-font-[500] !tw-text-[#f60]"]/text()')
        for i in range(len(name_list)):
            print(name_list[i].extract(), ':' ,price_list[i].extract())


#scrapy shell www.baidu.com

