import ccxt
from datetime import datetime
import pytz
import time
import sys  # Import sys to enable exiting the program
from pytz import timezone
import logging
import os
import sys
import pandas as pd
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
        + title
        + "] 邮件发送成功"
    )

# Get the current Python script file path
current_script_path = os.path.abspath(sys.argv[0])
current_script_directory = os.path.dirname(current_script_path)
# print(f"当前脚本文件路径: {current_script_path}")
# print(f"当前脚本文件所在目录: {current_script_directory}")

# Specify the log file's relative path
log_file_path = os.path.join(current_script_directory, 'temp.log')

# Create a custom Formatter class to convert time to Beijing time
class BeijingTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        beijing_tz = timezone('Asia/Shanghai')
        return dt.astimezone(beijing_tz)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.strftime('%Y-%m-%d %H:%M:%S')

# Create log logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the log recording level to DEBUG

# Create a file handler, specify a log file path and encoding
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)  # Set the file handler level to WARNING
file_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create a stream handler to output logs to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Set the stream handler level to DEBUG
stream_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# logger.debug('调试信息')
# logger.info('消息日志')
# logger.warning('警告日志')
# logger.error('错误日志')
# logger.critical('严重错误')

beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)
print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))





exchange_bn = ccxt.binanceusdm({
    # 'apiKey': '1J1Kyk7a6gL8nl7wklOHmFhaMkcRJ1RO9QytTLNMi5gRjKm3nkJOyiLp9cW3A4DT',
    # 'secret': 'qS7AfSQQOQp6o89qDkZGiLs0kSzYfR0PJoxodVBf3MmyUlmTUFVfWsD8BqPkJXWd'
})

exchange_bingx = ccxt.bingx()
# markets = exchange_mexc.fetch_markets()

exchange_kucoin = ccxt.kucoin()




#cd /www/wwwroot/musk/test
#

# print(exchange_bn.fetch_ticker('BTC/USDT'))
symbols = 'BTC/USDT'
timeframe = '1h'
limit = 48
bars = exchange_bn.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])

# 将时间列转换为日期时间对象
df['时间'] = pd.to_datetime(df['时间'], unit='ms')

# 设置时区为北京时间（中国标准时间，CST）
df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

# print(bars)
print(df)

symbols_list = ['HIPPO/USDT','DEGEN/USDT','AKT/USDT','BAN/USDT','SCRTUSDT',
                'SLERF/USDT','1000WHY/USDT','CHILLGUY/USDT','MORPHO/USDT','AERO/USDT',
                'KAIA/USDT','ORCA/USDT','ACX/USDT','VIRTUAL/USDT','KOMA/USDT',
                'ME/USDT','DEGO/USDT','AVA/USDT','VELODROME/USDT',
             'MOCA/USDT','VANA/USDT','PENGU/USDT','1000CAT/USDT','USUAL/USDT',
              'LUMIA/USDT','DF/USDT','PHA/USDT','ZEREBRO/USDT','AI16Z/USDT',
               'GRIFFAIN/USDT','BIO/USDT','SWARMS/USDT','ALCH/USDT','COOKIE/USDT',
                'PROM/USDT','SOLV/USDT','AVAAI/USDT','ARC/USDT','TRUMP/USDT',
                 'MELANIA/USDT','ANIME/USDT','PIPPIN/USDT','VVV/USDT','BERA/USDT','VINE/USDT','AIXBT/USDT','CGPT/USDT','HIVE/USDT'
                 ,'TST/USDT','1000CHEEMS/USDT','LAYER/USDT','HEI/USDT','B3/USDT','IP/USDT','SHELL/USDT','GPS/USDT','KAITO/USDT']


import time
from datetime import datetime
import pytz



# 创建北京时间的时区对象
beijing_tz = pytz.timezone('Asia/Shanghai')

# 获取北京时间的函数
def get_beijing_time():
    return datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')



while True:
    fudu_list = []
    max_fudu = []
    min_fudu = []
    sum_max_fudu = 0  # 最大 fudu 的和
    sum_min_fudu = 0  # 最小 fudu 的和   
    for i in symbols_list:
        bars = exchange_bn.fetch_ohlcv(i, timeframe=timeframe, limit=limit)
        time.sleep(0.1)
        fudu = (bars[-1][-2] - bars[0][-2]) / bars[0][-2] * 100  # 转换为百分比
        fudu = round(fudu, 2)  # 保留两位小数
        fudu_list.append((i, fudu))  # 将交易对和 fudu 值添加到列表中

    # 按 fudu 值进行排序
    fudu_list.sort(key=lambda x: x[1])

    # 获取最大和最小的 10 个 fudu 值
    max_fudu = fudu_list[-10:]
    min_fudu = fudu_list[:10]

    # 计算最大和最小 fudu 值的和
    sum_max_fudu = sum(fudu for _, fudu in max_fudu)
    sum_min_fudu = sum(fudu for _, fudu in min_fudu)

    # 打印最大和最小的 10 个 fudu 值以及北京时间
    current_time = get_beijing_time()
    print(f"时间: {current_time} - 最大 10 个 fudu:")
    for i, fudu in max_fudu:
        print(f'{i}  {fudu}%')

    print(f"\n时间: {current_time} - 最小 10 个 fudu:")
    for i, fudu in min_fudu:
        print(f'{i}  {fudu}%')



    # 打印最大和最小的 fudu 值的总和
    print(f"\n最大 10 个 fudu 的总和: {sum_max_fudu}%")
    print(f"最小 10 个 fudu 的总和: {sum_min_fudu}%")

    max_fudu2 = ",".join([str(item) for item in max_fudu])
    min_fudu2 = ",".join([str(item) for item in min_fudu])


    if sum_max_fudu > 350 or sum_max_fudu < -50:
        send_email(
                   str(current_time) + '：' + str(sum_max_fudu),max_fudu2
                )
    if sum_min_fudu < -300 or sum_min_fudu > 10:
                send_email(
                   str(current_time) + '：' + str(sum_min_fudu),min_fudu2
                )

    filename = f'/www/wwwroot/musk/test/bn/fudu_results.txt'

    # 保存最大和最小 fudu 值及其总和到文件中
    with open(filename, 'a', encoding='utf-8') as file:
        # file.write(f"时间: {current_time} - 最大 10 个 fudu:\n")
        file.write(f"时间: {current_time}")
        # for i, fudu in max_fudu:
        #     file.write(f'{i}  {fudu}%\n')

        # file.write(f"\n时间: {current_time} - 最小 10 个 fudu:\n")
        # for i, fudu in min_fudu:
        #     file.write(f'{i}  {fudu}%\n')

        file.write(f"\n最大 10 个 fudu 的总和: {sum_max_fudu}%\n")
        file.write(f"最小 10 个 fudu 的总和: {sum_min_fudu}%\n")
        file.write(f"\n")
        # file.write(f"-----------------------------------------------------------------------------------------分界线-----------------------------------------------------------------------------------------\n")
  
    #cd /www/wwwroot/musk/test/bn
    #screen -S heyuejiankong python3 074_heyuejiankong.py 
    #每2小时存储10个最大和
    # 每小时执行一次（模拟每小时执行一次）
    time.sleep(7200)
        
