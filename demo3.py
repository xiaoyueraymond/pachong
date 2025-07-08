import asyncio
import json
import os
import smtplib
import ssl
import threading
import time
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote, urlencode

import requests
from bs4 import BeautifulSoup

# ================================================  配置  ================================================

# ====================  主要  ====================
# 过滤列表,存在以下字符串时,不推送邮件
filterList = ["合约", "合約"]
# 检测间隔(毫秒)
sleepTime = 60
# 数据存放位置,无需改动
folder = "data/虚拟币公告"
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
proxies = {"http": "http://localhost:7890", "https": "http://localhost:7890"}

# ================================================  邮件  ================================================


def get_beijing_time():
    # 创建一个时区对象，表示东八区
    sha_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")

    # 获取当前的 UTC 时间
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)

    # 将 UTC 时间转换为北京时间
    beijing_now = utc_now.astimezone(sha_tz)

    return beijing_now


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
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] 币安访问状态码: "
            + res.status_code
        )

    html = BeautifulSoup(res.text, "html.parser")
    data = html.find(id="__APP_DATA").get_text()
    info = json.loads(data)

    articles = info["appState"]["loader"]["dataByRouteId"]["d9b2"]["catalogs"][0][
        "articles"
    ]

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(articles[0]["releaseDate"] / 1000)
            )
            title = articles[0]["title"]
            link = (
                "https://www.binance.com/zh-CN/support/announcement/"
                + articles[0]["code"]
            )
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "币安", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


# ================================================  欧易  ================================================


def okx():
    dir = folder + "/okx"
    url = "https://www.okx.com/zh-hans/help/section/announcements-new-listings"
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] 欧易访问状态码: "
            + res.status_code
        )

    html = BeautifulSoup(res.text, "html.parser")
    data = html.find(id="appState").get_text()
    info = json.loads(data)

    articles = info["appContext"]["initialProps"]["sectionData"]["articleList"]["items"]

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date = datetime.strptime(
                articles[0]["publishTime"], "%Y-%m-%dT%H:%M%z"
            ).strftime(timeFormat)
            title = articles[0]["title"]
            link = "https://www.okx.com/zh-hans/help/" + articles[0]["slug"]
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "欧易", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


# ================================================  火币  ================================================


def htx():
    dir = folder + "/htx"
    url = "https://www.htx.com/-/x/support/public/getList/v2?language=zh-cn&page=1&limit=10&oneLevelId=360000031902&twoLevelId=360000039942"
    res = requests.get(url, proxies=proxies)

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] 火币访问状态码: "
            + res.status_code
        )

    info = json.loads(res.text)

    articles = info["data"]["list"]

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(articles[0]["showTime"] / 1000)
            )
            title = articles[0]["title"]
            link = "https://www.htx.com/zh-cn/support/" + str(articles[0]["id"])
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "火币", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


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
    articles = sorted(  # 存在置顶问题,需要重新排序
        articles, key=lambda article: article["createdAt"], reverse=True
    )

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date = datetime.strptime(
                articles[0]["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
            ).strftime(timeFormat)
            title = articles[0]["title"]
            link = "https://www.mexc.com/zh-TW/support/articles/" + str(
                articles[0]["id"]
            )
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "MEXC", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


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
                    "GATE", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


# ================================================  BITGET  ================================================


def bitget():
    dir = folder + "/bitget"
    url = "https://www.bitget.cloud/v1/cms/helpCenter/content/section/helpContentDetail"
    params = {
        "pageNum": 1,
        "pageSize": 10,
        "params": {
            "sectionId": "5955813039257",
            "languageId": 1,
            "firstSearchTime": int(time.time() * 1000),
        },
    }
    res = requests.post(
        url,
        data=json.dumps(params),
        headers={"Content-Type": "application/json"},
        proxies=proxies,
    )

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] BITGET访问状态码: "
            + res.status_code
        )

    info = json.loads(res.text)

    articles = info["data"]["items"]

    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["contentId"] != history[0]["contentId"]:
            date = date = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(int(articles[0]["showTime"]) / 1000),
            )
            title = articles[0]["title"]
            link = "https://www.bitget.cloud/zh-CN/support/articles/" + str(
                articles[0]["contentId"]
            )
            isSend = True
            for name in filterList:
                if name in title:
                    isSend = False
                    break
            if isSend:
                send_email(
                    "BITGET", "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))


def main():
    while True:
        print("[" + get_beijing_time().strftime(timeFormat) + "] [INFO] 开始检测")
        threading.Thread(target=binance).start()
        threading.Thread(target=okx).start()
        threading.Thread(target=htx).start()
        threading.Thread(target=mexc).start()
        threading.Thread(target=gate).start()
        threading.Thread(target=bitget).start()
        time.sleep(sleepTime)
        # binance()
        # okx()
        # htx()
        # mexc()
        # gate()
        # bitget()


if __name__ == "__main__":
    main()
