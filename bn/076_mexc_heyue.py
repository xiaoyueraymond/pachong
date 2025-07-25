import asyncio
import json
import os
import smtplib
import ssl
import threading
import time
import pytz
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote, urlencode
import requests
from bs4 import BeautifulSoup

# ================================================  配置  ================================================

# ====================  主要  ====================
# 过滤列表,存在以下字符串时,不推送邮件
filterList = ["【全球首發】MEXC將上線"]
# 检测间隔(秒)
sleepTime = 3600
# 数据存放位置,无需改动
folder = "/www/wwwroot/musk/test/bn"
# 日志时间格式化
timeFormat = "%Y/%m/%d %H:%M:%S"

# ====================  邮箱  ====================
SENDER_EMAIL = "13042063262@163.com"
SENDER_PASSWORD = "FGc8jrbvcNtGVW5J"  # 使用授权码
RECEIVER_EMAIL = "musk130@qq.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465

# ====================  代理  ====================
# 由于墙存在,测试使用,放在服务器时应该置空
# proxies = {"http": "http://localhost:7890", "https": "http://localhost:7890"}
proxies = {}

# ================================================  邮件  ================================================


def get_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')  # 设置为北京时间
    return datetime.now(tz)


def send_email(title, body):
    """发送电子邮件，body为邮件内容"""
    subject = title + "网站公告更新"
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print(
        "["
        + get_beijing_time().strftime(timeFormat)
        + "] [INFO] ["
        + title
        + "] 邮件发送成功"
    )


# ================================================  币安  ================================================

def binance():
    dir = folder + "/binance"
    url = "https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "aliyungf_tc=55a6a6958a3b7b1efd067cbc6cf63f219c450ffb22613538cce4ed638fa158d2; theme=dark; bnc-uuid=fbbd7acd-11a1-48ce-9770-e7e4a149bc3b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219564f04b62ca8-0e563f11c4dd18-26011a51-2073600-19564f04b632c75%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk1NjRmMDRiNjJjYTgtMGU1NjNmMTFjNGRkMTgtMjYwMTFhNTEtMjA3MzYwMC0xOTU2NGYwNGI2MzJjNzUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; sajssdk_2015_cross_new_user=1; BNC_FV_KEY=336cb1afc028a809b0f772ff59e5ebefe4d35afb; BNC_FV_KEY_T=101-oK4Q9dQCL%2FHpDOOYwdJPiSVsjz9FwGUKTPOGu%2FjM1c1vETJZBaOaM5kBMY17ffg1vY%2FH7ugkNy%2BV2hODeNY4Tg%3D%3D-6p6OdvDt0bB4RsitZf%2B1Rg%3D%3D-54; BNC_FV_KEY_EXPIRE=1741176824558; aws-waf-token=bec70e14-21e7-4a70-a32d-c74934c6ee57:AQoAaX89LmoAAAAA:M9tzIh4jkPOF2QqkgHy7aNV8XVFE2g6lf+g3Hd08ozj4s5d7CPqYSq7rQP5h0oR+DWkVpPJVAGAgIjEbHQfVA+mWhmEcvTTmY6dvqwdQxIhF0Ojwbq+5NUUpDVDBDljA+KntH9M1QdSV5WZHMH/uo7MeseEtxi6TJ/0kpzm3UdYbnAvw+aS6Bnk2sZE3K++V1D2XaGs1",
        "Priority": "u=0, i",
        "Referer": "https://www.marketwebb.blue/zh-CN/support/announcement/list/48",
        "Sec-CH-UA": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    res = requests.get(url,headers=headers)

    if res.status_code != 200:
        print(
            "["
            + str(get_beijing_time().strftime(timeFormat))
            + "] [ERROR] 币安访问状态码: "
            + str(res.status_code)
        )
      
    html = BeautifulSoup(res.text, "html.parser")
    print(res.text)
#     data = html.find(id="__APP_DATA").get_text()
#     info = json.loads(data)
#     # print (info["appState"]["loader"]["dataByRouteId"])
#     articles = info["appState"]["loader"]["dataByRouteId"]["d34e"]["catalogDetail"]["articles"]
#     filePath = dir + "/history.json"
#     if os.path.exists(filePath):
#         with open(filePath, "r", encoding="utf-8") as file:
#             history = json.loads(file.read())
#         if articles[0]["id"] != history[0]["id"]:
#             date = time.strftime(
#                 "%Y-%m-%d %H:%M:%S", time.localtime(articles[0]["releaseDate"] / 1000)
#             )
#             title = articles[0]["title"]
#             link = (
#                 "https://www.binance.com/zh-CN/support/announcement/"
#                 + articles[0]["code"]
#             )
#             isSend = True
#             for name in filterList:
#                 if name in title:
#                     isSend = False
#                     break
#             if isSend:
#                 send_email(
#                     # "币安",  + str(get_beijing_time().strftime(timeFormat)) + "\n " + "标题: " + title + "\n时间: " + date + "链接: " + link
#                 )
#             with open(filePath, "w", encoding="utf-8") as file:
#                 file.write(json.dumps(articles, indent=4))
#     else:
#         if not os.path.exists(dir):
#             os.makedirs(dir)
#         with open(filePath, "w", encoding="utf-8") as file:
#             file.write(json.dumps(articles, indent=4))

# # ================================================  欧易  ================================================


# def okx():
#     dir = folder + "/okx"
#     url = "https://www.okx.com/zh-hans/help/section/announcements-new-listings"
#     res = requests.get(url, proxies=proxies)

#     if res.status_code != 200:
#         print(
#             "["
#             + get_beijing_time().strftime(timeFormat)
#             + "] [ERROR] 欧易访问状态码: "
#             + res.status_code
#         )

#     html = BeautifulSoup(res.text, "html.parser")
#     data = html.find(id="appState").get_text()
#     info = json.loads(data)

#     articles = info["appContext"]["initialProps"]["sectionData"]["articleList"]["items"]

#     filePath = dir + "/history.json"
#     if os.path.exists(filePath):
#         with open(filePath, "r", encoding="utf-8") as file:
#             history = json.loads(file.read())
#         if articles[0]["id"] != history[0]["id"]:
#             date = datetime.strptime(
#                 articles[0]["publishTime"], "%Y-%m-%dT%H:%M%z"
#             ).strftime(timeFormat)
#             title = articles[0]["title"]
#             link = "https://www.okx.com/zh-hans/help/" + articles[0]["slug"]
#             isSend = True
#             for name in filterList:
#                 if name in title:
#                     isSend = False
#                     break
#             if isSend:
#                 send_email(
#                     "欧易", "标题: " + title + "\n时间: " + date + "链接: " + link
#                 )
#             with open(filePath, "w", encoding="utf-8") as file:
#                 file.write(json.dumps(articles, indent=4))
#     else:
#         if not os.path.exists(dir):
#             os.makedirs(dir)
#         with open(filePath, "w", encoding="utf-8") as file:
#             file.write(json.dumps(articles, indent=4))


# # ================================================  火币  ================================================


# def htx():
#     dir = folder + "/htx"
#     url = "https://www.htx.com/-/x/support/public/getList/v2?language=zh-cn&page=1&limit=10&oneLevelId=360000031902&twoLevelId=360000039942"
#     res = requests.get(url, proxies=proxies)

#     if res.status_code != 200:
#         print(
#             "["
#             + get_beijing_time().strftime(timeFormat)
#             + "] [ERROR] 火币访问状态码: "
#             + res.status_code
#         )

#     info = json.loads(res.text)

#     articles = info["data"]["list"]

#     filePath = dir + "/history.json"
#     if os.path.exists(filePath):
#         with open(filePath, "r", encoding="utf-8") as file:
#             history = json.loads(file.read())
#         if articles[0]["id"] != history[0]["id"]:
#             date = time.strftime(
#                 "%Y-%m-%d %H:%M:%S", time.localtime(articles[0]["showTime"] / 1000)
#             )
#             title = articles[0]["title"]
#             link = "https://www.htx.com/zh-cn/support/" + str(articles[0]["id"])
#             isSend = True
#             for name in filterList:
#                 if name in title:
#                     isSend = False
#                     break
#             if isSend:
#                 send_email(
#                     "火币", "标题: " + title + "\n时间: " + date + "链接: " + link
#                 )
#             with open(filePath, "w", encoding="utf-8") as file:
#                 file.write(json.dumps(articles, indent=4))
#     else:
#         if not os.path.exists(dir):
#             os.makedirs(dir)
#         with open(filePath, "w", encoding="utf-8") as file:
#             file.write(json.dumps(articles, indent=4))


# ================================================  MEXC  ================================================


def mexc():
    dir = folder + "/mexc"
    url = "https://www.mexc.com/help/announce/api/zh-TW/section/360000254192/articles?page=1&perPage=20"
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] MEXC访问状态码: "
            + res.status_code
        )

    info = json.loads(res.text)

    articles = info["data"]["results"]
    titles = [item['title'] for item in articles]
    filePath = dir + ".txt"
    existing_titles = set()
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            existing_titles = set(file.read().splitlines())
#cd /www/wwwroot/musk/test/bn
#screen -S mexcheyue python3  mexc_heyue.py
    # 将新的标题写入文件并执行函数a
    with open(filePath, "a", encoding="utf-8") as file:
        for title in titles:
            if title not in existing_titles:
                beijing_time = get_beijing_time().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{beijing_time}\n{title}\n")
                existing_titles.add(title)  # 将新标题添加到已存在的标题集合
                if "【全球首發】" in title:
                     send_email("MEXC", f"北京时间: {beijing_time}, 标题: {title}")


# ================================================  GATE  ================================================



def gate():
    dir = folder + "/gate"
    url = "https://www.gate.io/zh/announcements/newlisted"
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] GATE访问状态码: "
            + res.status_code
        )
    html = BeautifulSoup(res.text, "html.parser")

    data = html.select(".article-list-content .article-list-item")

    articles = []

    for item in data:
        a = item.select_one(".article-list-item-content a")
        itemUrl = "https://www.gate.io" + a.attrs["href"]
        idSp = itemUrl.split("/")
        articles.append(
            {
                "id": idSp[idSp.__len__() - 1],
                "title": a.get_text().strip(),
                "url": itemUrl,
                "date": item.select_one(
                    "span[class='article-list-info-timer article-list-item-info-item']"
                )
                .get_text()
                .strip(),
            }
        )

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date3 = get_beijing_time().strftime(timeFormat)
            date = articles[0]["date"]
            title = articles[0]["title"]
            link = articles[0]["url"]
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "GATE", "标题: "  + title + "\n时间: " + date   + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


def gate3():
    dir = folder + "/gate"
    url = "https://www.gate.io/apiw/v2/pilot/markets?exchange_type=PILOT_ALL"
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] GATE访问状态码: "
            + res.status_code
        )

    articles = json.loads(res.text)["data"]
    # 测试
    # articles[0]["buy_start"] = int(articles[0]["buy_start"]) * 2
    newarticle = []
    timestamp = time.time()
    for article in articles:
        if int(article["buy_start"]) > timestamp:
            newarticle.append(article)
    if len(newarticle) == 0:
        return
    # print(newarticle)

    filePath = dir + "/history3.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        for article in newarticle:
            if article["show_pair"] in history:
                continue
            else:
                date = time.strftime(
                    timeFormat, time.localtime(int(article["buy_start"]))
                )
                title = "检测到新币 " + article["show_pair"] + " 将上线"
                link = "https://www.gate.io/zh/pilot" + article["seo_path"]
                send_email(
                    "GATE", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
        flist = json.loads("[]")
        for article in newarticle:
            flist.append(article["show_pair"])
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(flist, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            flist = json.loads("[]")
            for article in newarticle:
                flist.append(article["show_pair"])
                date = time.strftime(
                    timeFormat, time.localtime(int(article["buy_start"]))
                )
                title = "检测到新币 " + article["show_pair"] + " 将上线"
                link = "https://www.gate.io/zh/pilot" + article["seo_path"]
                send_email(
                    "GATE", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            file.write(json.dumps(flist, indent=4))


# ================================================  BITGET  ================================================

from lxml import etree


def bitget():
    dir = folder + "/bitget"
    url = "https://www.bitget.cloud/zh-CN/support/sections/5955813039257"


    headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }

    #url 请求资源路径#params 参数
    #kwargs 字典


    response =requests.get(url=url,headers=headers)
    content = response.text
    tree = etree.HTML(content)
    bitget_list = tree.xpath('//a[@class="ArticleList_item_title__u3fLL"]/text()')
    print(bitget_list)
    filePath = dir + ".txt"
    existing_titles = set()
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            existing_titles = set(file.read().splitlines())
#cd /www/wwwroot/musk/test/bn
#screen -S mexcheyue python3  mexc_heyue.py
    # 将新的标题写入文件并执行函数a
    with open(filePath, "a", encoding="utf-8") as file:
        for title in bitget_list:
            if title not in existing_titles:
                beijing_time = get_beijing_time().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{beijing_time}\n{title}\n")
                existing_titles.add(title)  # 将新标题添加到已存在的标题集合
                print(f'新增部分{title}')
                send_email("BITGET", f"北京时间: {beijing_time}, 标题: {title}")


def main():
    while True:
        print("[" + get_beijing_time().strftime(timeFormat) + "] [INFO] 开始检测")
        threading.Thread(target=binance).start()
        # threading.Thread(target=okx).start()
        # threading.Thread(target=htx).start()
        # threading.Thread(target=mexc).start()
        #threading.Thread(target=gate).start()
        #threading.Thread(target=gate3).start()
        # threading.Thread(target=bitget).start()
        time.sleep(sleepTime)


# 测试使用
# def main2():
#     while True:
#         print("[" + get_beijing_time().strftime(timeFormat) + "] [INFO] 开始检测")
#         threading.Thread(target=gate3).start()
#         time.sleep(sleepTime)


if __name__ == "__main__":
    main()
