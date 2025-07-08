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
filterList = ["测试", "测试"]
# 检测间隔(秒)
sleepTime = 10
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
# proxies = {"http": "http://localhost:7890", "https": "http://localhost:7890"}
proxies = {}

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
            + str(get_beijing_time().strftime(timeFormat))
            + "] [ERROR] 币安访问状态码: "
            + res.status_code
        )

    html = BeautifulSoup(res.text, "html.parser")
    data = html.find(id="__APP_DATA").get_text()
    info = json.loads(data)
    # print (info["appState"]["loader"]["dataByRouteId"])
    articles = info["appState"]["loader"]["dataByRouteId"]["d34e"]["catalogDetail"]["articles"]
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
                    # "币安",  + str(get_beijing_time().strftime(timeFormat)) + "\n " + "标题: " + title + "\n时间: " + date + "链接: " + link
                )
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(json.dumps(articles, indent=4))
    else:
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(json.dumps(articles, indent=4))

# ================================================  欧易  ================================================



# ================================================  MEXC  ================================================
import requests
import json
import ccxt 
import pandas as pd
from datetime import datetime

# 定义获取MEXC新币信息的函数
# def mexc():
#     folder = "/path/to/folder"  # 你需要定义文件夹路径
#     url = "https://www.mexc.com/api/operation/new_coin_calendar?timestamp=1739586412859"
#     proxies = {}  # 如果需要代理，请在这里配置

#     res = requests.get(url, proxies=proxies)

#     if res.status_code != 200:
#         print(
#             "["
#             + get_beijing_time().strftime("%Y-%m-%d %H:%M:%S")  # 假设 get_beijing_time() 是其他地方定义的
#             + "] [ERROR] MEXC访问状态码: "
#             + str(res.status_code)
#         )
#         return

#     info = json.loads(res.text)
#     articles = info["data"]["newCoins"]
#     articles = articles[3:]

#     for i in range(len(articles)):
#         print(articles[i]['vcoinName'], ':', articles[i]['firstOpenTime'])

#         # 调用 max_price 函数获取 OHLCV 数据
#         max_price(articles[i]['vcoinName'], articles[i]['firstOpenTime'])
#         time.sleep(0.1)

# # 定义获取OHLCV数据并处理的函数
# def max_price(vcoin_name, first_open_time):
#     exchange_mexc = ccxt.mexc()

#     # 构造交易对的符号
#     symbol = f'{vcoin_name}/USDT'
#     timeframe = '1m'
#     since = first_open_time  # 使用首次开盘时间作为 since 参数
#     limit = 1

#     try:
#         bars = exchange_mexc.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        
#         # 将OHLCV数据转换为DataFrame
#         df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])
        
#         # 将'时间'列从毫秒转换为日期时间
#         df['时间'] = pd.to_datetime(df['时间'], unit='ms')

#         # 设置时区为北京时间（CST）
#         df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

#         print(bars)
#         print(df)
#     except Exception as e:
#         print(f"获取 {vcoin_name} 数据时发生错误: {e}")

# # 调用 mexc 函数开始执行
# mexc()

from datetime import datetime
import pytz
import ccxt
import pandas as pd

# 假设你已经安装了ccxt和pandas库
# 给定的时间字符串
symbol_list = [
    ("2025-02-15 18:00:00", "AICE"),
    ("2025-02-13 12:15:00", "BROWNIE"),
    ("2025-02-13 16:00:00", "GMRT"),
    ("2025-02-13 22:00:00", "BERAFI"),
    ("2025-02-13 22:05:00", "SHELL"),
    ("2025-02-13 22:10:00", "ASKJ"),
    ("2025-02-12 16:00:00", "DIAM"),
    ("2025-02-12 16:00:00", "MERGE"),
    ("2025-02-12 18:00:00", "AVL"),
    ("2025-02-12 18:00:00", "SCOT"),
    ("2025-02-12 20:00:00", "KAON"),
    ("2025-02-11 16:00:00", "SCC"),
    ("2025-02-11 17:00:00", "KOKU"),
    ("2025-02-11 17:20:00", "STRDY"),
    ("2025-02-11 18:00:00", "HVLO"),
    ("2025-02-11 18:40:00", "HARRYBOLZ"),
    ("2025-02-11 19:00:00", "M")
]

# 假设你使用的交易所是MEXC，确保你已安装并配置好ccxt
exchange_mexc = ccxt.mexc()

# 构造交易对的符号
vcoin_name = 'BTC'  # 例子：替换成你想交易的币种
symbol = f'{vcoin_name}/USDT'
timeframe = '1m'
limit = 1

# 循环遍历symbol_list
for i in range(len(symbol_list)):
    # 获取symbol_list中的时间字符串
    since_str = symbol_list[i][0]
    
    # 将时间字符串转换为datetime对象
    since_datetime = datetime.strptime(since_str, "%Y-%m-%d %H:%M:%S")
    
    # 将datetime对象转换为UTC的timestamp（毫秒）
    since_timestamp = int(since_datetime.replace(tzinfo=pytz.timezone('Asia/Shanghai')).astimezone(pytz.utc).timestamp() * 1000)

    # 获取OHLCV数据
    bars = exchange_mexc.fetch_ohlcv(symbol, timeframe=timeframe, since=since_timestamp, limit=limit)
    
    # 将OHLCV数据转换为DataFrame
    df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])
    
    # 将'时间'列从毫秒转换为日期时间
    df['时间'] = pd.to_datetime(df['时间'], unit='ms')
    
    # 设置时区为北京时间（CST）
    df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai') 

    # 打印符号和最后一根K线的收盘价
    print(symbol_list[i][1], ":", bars[0][-2])

    

