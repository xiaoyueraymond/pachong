import json
import os
import re
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
sleepTime = 10
# 数据存放位置,无需改动
folder = "data/虚拟币公告"
# 日志时间格式化
timeFormat = "%Y/%m/%d %H:%M:%S"
cookie = "aws-waf-token=fbc88880-fb1a-4556-b519-64f1bc2d949d:AAoAtLJCBBEyAAAA:ya/SJXRXiK2LqeqhQDQcCoWr9I45a6lamJLqjs96IFD8UcvaDuXBe3xlIZAnR+z2b7eWjiLs7cZKKP9MXnHgQ5KMJ+uzmkv7YFh2z8+E+THdhhB6aOkdPYXSEbL10XJwEoKFWgsfBxZHhBBN8j5yD1qtdR0qJVY8wA7b1+uphtg7BTLObpaeDuNniG1SLAFbkFf/vHtrJA=="

# ====================  邮箱  ====================
SENDER_EMAIL = "13042063262@163.com"
SENDER_PASSWORD = "FGc8jrbvcNtGVW5J"  # 使用授权码
RECEIVER_EMAIL = "musk130@qq.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465

# ====================  代理  ====================
# 由于墙存在,测试使用,放在服务器时应该置空
proxies = {}

# ================================================  邮件  ================================================


def ms_timestamp_to_bj_time(ms_timestamp):
    # 将毫秒时间戳转换为秒
    timestamp_in_seconds = ms_timestamp / 1000

    # 创建一个datetime对象，并设定其为UTC时间
    utc_time = datetime.utcfromtimestamp(timestamp_in_seconds)

    # 定义从UTC到北京时间的时差
    bj_tz = timezone(timedelta(hours=8))

    # 转换为北京时间
    bj_time = utc_time.replace(tzinfo=timezone.utc).astimezone(bj_tz)

    # 格式化时间为字符串并返回
    return bj_time.strftime("%Y-%m-%d %H:%M:%S")


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
    dir = folder + "/binance2"
    url = "https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN"
    res = requests.get(url, proxies=proxies, headers={"cookie": cookie})

    if res.status_code != 200:
        print(
            "["
            + get_beijing_time().strftime(timeFormat)
            + "] [ERROR] 币安访问状态码: "
            + str(res.status_code)
        )
        return

    html = BeautifulSoup(res.text, "html.parser")
    # print(html)
    data = html.find(id="__APP_DATA").get_text()
    info = json.loads(data)

    articles = info["appState"]["loader"]["dataByRouteId"]["d34e"]["catalogDetail"][
        "articles"
    ]
    # print(json.dumps(articles))
    # exit()
    filePath = dir + "/history.json"
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            history = json.loads(file.read())
        if articles[0]["id"] != history[0]["id"]:
            date = ms_timestamp_to_bj_time(articles[0]["releaseDate"])
            title = articles[0]["title"]
            if "添加种子标签" in title:
                match = re.search(r"\((.*?)\)", title)
                if match:
                    a_content = match.group(1)
                    # print(a_content)
                    a(a_content)
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


def a(name):
    print(name)
    ## 自定义方法


def main():
    while True:
        print("[" + get_beijing_time().strftime(timeFormat) + "] [INFO] 开始检测")
        threading.Thread(target=binance).start()
        time.sleep(sleepTime)


if __name__ == "__main__":
    main()
