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




#cd /www/wwwroot/musk/test/bn
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



# print(df)

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




     



# 预先获取所有符号的数据
symbol_data = {}
for symbols in symbols_list:
    bars = exchange_bn.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
    symbol_data[symbols] = bars
    time.sleep(0.1)  # 如果需要间隔请求，可以保留

print(symbol_data)

# 然后遍历 symbols_list 和 i 来计算 fudu


for i in range(0, 47):  # 内层循环遍历 i
    total_fudu_for_i = 0 
    for symbols in symbols_list:
        bars = symbol_data[symbols]  # 获取已缓存的 bars 数据
        # 计算 fudu
        fudu = round((bars[i + 1][-2] - bars[0][-2]) / bars[0][-2] * 100, 2)
        # 将 fudu 累加到 total_fudu_for_i
        total_fudu_for_i = round(total_fudu_for_i + fudu, 2)
    print(f'第{i+1}个小时的幅度是:{total_fudu_for_i}')










        
