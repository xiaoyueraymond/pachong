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
print("北京timestamp:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))


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
symbols = 'HIPPO/USDT'
timeframe = '1h'
limit = 1500
bars = exchange_bn.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# 将timestamp列转换为日期timestamp对象
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 设置时区为北京timestamp（中国标准timestamp，CST）
df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')

# 将DataFrame存储为txt文件
filename = f'/www/wwwroot/musk/test/gps.txt'
df.to_csv(filename, sep='\t', index=False, encoding='utf-8')

# 打印数据
print(df)
symbols_list = [
    
    "SHELL/USDT",
    "GPS/USDT",
    "IP/USDT",
    "B3/USDT",
    "HEI/USDT",
    "LAYER/USDT",
    "1000CHEEMS/USDT",
    "TST/USDT",
    "BERA/USDT",
    "VVV/USDT",
    "PIPPIN/USDT",
    "VINE/USDT",
    "ANIME/USDT",
    "VTHO/USDT",
    "MELANIA/USDT",
    "TRUMP/USDT",
    "ARC/USDT",
    "AVAAI/USDT",
    "SOLV/USDT",
    "PROM/USDT",
    "AIXBT/USDT",
    "CGPT/USDT",
    "COOKIE/USDT",
    "ALCH/USDT",
    "SWARMS/USDT",
    "BIO/USDT",
    "GRIFFAIN/USDT",
    "AI16Z/USDT",
    "ZEREBRO/USDT",
    "PHA/USDT",
    "DF/USDT",
    "HIVE/USDT",
    "LUMIA/USDT",
    "USUAL/USDT",
    "1000CAT/USDT",
    "PENGU/USDT",
    "VANA/USDT",
    "MOCA/USDT",
    "VELODROME/USDT",
    "AVA/USDT",
    "DEGO/USDT",
    "ME/USDT",
    "RAYSOL/USDT",
    "KOMA/USDT",
    "VIRTUAL/USDT",
    "SPX/USDT",
    "MOVE/USDT",
    "ACX/USDT",
    "ORCA/USDT",
    "KAIA/USDT",
    "AERO/USDT",
    "MORPHO/USDT",
    "CHILLGUY/USDT",
    "1000WHY/USDT",
    "SLERF/USDT",
    "SCRT/USDT",
    "BAN/USDT",
    "AKT/USDT",
    "DEGEN/USDT",
    "HIPPO/USDT",
    "1000X/USDT",
    "ACT/USDT",
    "PNUT/USDT",
    "GRASS/USDT",
    "DRIFT/USDT",
    "SWELL/USDT",
    "CETUS/USDT",
    "1000000MOG/USDT",
    "COW/USDT",
    "PONKE/USDT",
    "TROY/USDT"
]

import pandas as pd

def get_fudu(symbols):
    # 假设 symbols 和 bars 已经定义
    fudu_list = []
    fudu_list_symbols = [symbols]  # 第一列是符号
    bars = exchange_bn.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
    # 计算涨跌幅，并存储在 fudu_list 中
    for i in range(0, len(bars)):
        if i > 46:
            fudu = (bars[i][-2] - bars[i-47][-2]) / bars[0][-2] * 100  # 转换为百分比
            fudu = round(fudu, 4)  # 保留四位小数
            fudu_list.append(fudu)

    # 如果 fudu_list 长度不为 1453，前面填充 0
    if len(fudu_list) < 1453:
        fudu_list = [0] * (1453 - len(fudu_list)) + fudu_list

    # 将符号和涨跌幅组合起来
    fudu_list = fudu_list_symbols + fudu_list

    # 将数据转换为 DataFrame
    df = pd.DataFrame([fudu_list], columns=['Symbol'] + [f'fudu_{i+1}' for i in range(1453)])
    return df

# 初始化一个空的 DataFrame 用来拼接数据


import os

filename = '/www/wwwroot/musk/test/huice/fudu_data.csv'

# 假设 symbols_list 和 bars 已经定义
for symbols in symbols_list: 
    # 获取每个符号的 fudu 数据
    df = get_fudu(symbols)
    time.sleep(0.1)
    print(f'已经写入{symbols}')
    # 如果文件不存在，写入头部（columns），否则追加数据
    df.to_csv(filename, mode='a', index=False, header=not os.path.exists(filename))






    
