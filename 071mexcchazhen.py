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

#这是用来统计抹茶插针的幅度，进行捡漏操作

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


exchange_mexc = ccxt.mexc({  
})


#这是用来统计抹茶插针的幅度，进行捡漏操作
#cd /www/wwwroot/musk/test
symbols_example = 'MUBARAK_USDT'
timeframe = '1h'
limit = 37
bars = exchange_mexc.fetch_ohlcv(symbols_example, timeframe=timeframe, limit=limit)
df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])
print(df)
# 将时间列转换为日期时间对象
df['时间'] = pd.to_datetime(df['时间'], unit='ms')
# 设置时区为北京时间（中国标准时间，CST）
df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
# 计算插针幅度并新增一列，并转换为百分比
df['插针幅度'] = ((df['高'] - df['收']) / df['收']) * 100
# 保留两位小数
# 保留两位小数并添加百分号符号
df['插针幅度'] = df['插针幅度'].apply(lambda x: f"{x:.2f}%")
# 提取插针幅度列的数值部分进行最大值计算（去掉百分号后比较）
df['插针幅度数值'] = df['插针幅度'].str.rstrip('%').astype(float)
# 打印插针幅度最大值
max_value = df['插针幅度数值'].max()
# 找到最大插针幅度对应的时间
max_value_row = df[df['插针幅度数值'] == max_value]
list = [symbols_example,max_value_row['时间'].values[0],max_value,]
print(f"插针幅度的最大值为:{symbols_example}:{max_value_row['时间'].values[0]}:{max_value}%")

def max_value(symbols):
    bars = exchange_mexc.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])
    # 将时间列转换为日期时间对象
    df['时间'] = pd.to_datetime(df['时间'], unit='ms')
    # 设置时区为北京时间（中国标准时间，CST）
    df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    # 计算插针幅度并新增一列，并转换为百分比
    df['插针幅度'] = ((df['高'] - df['收']) / df['收']) * 100
    # 保留两位小数
    # 保留两位小数并添加百分号符号
    df['插针幅度'] = df['插针幅度'].apply(lambda x: f"{x:.2f}%")
    # 提取插针幅度列的数值部分进行最大值计算（去掉百分号后比较）
    df['插针幅度数值'] = df['插针幅度'].str.rstrip('%').astype(float)
    # 打印插针幅度最大值
    max_value = df['插针幅度数值'].max()
    # 找到最大插针幅度对应的时间
    max_value_row = df[df['插针幅度数值'] == max_value]
    list = [symbols,max_value_row['时间'].values[0],max_value,]
    # print(f"插针幅度的最大值为:{symbols}:{max_value_row['时间'].values[0]}:{max_value}%")
    return list


symbols_list = ['KET_USDT', 'VIVI_USDT', 'XOXO_USDT', 'ONON_USDT', 'LIBRA_USDT', 'WINK_USDT', 'ARCSOL_USDT', 
'BROCCOLI_USDT', 'BROWNIE_USDT', 'SHELL_USDT', 'FULLSEND_USDT', 'CAPTAINBNB_USDT', 'HEI_USDT', 
 'DIN_USDT', 'IP_USDT', 'AVL_USDT', 'G7_USDT', 'LAYER_USDT', 'TJRM_USDT', 'OKM_USDT', 
'CAR_USDT', 'JAILSTOOL_USDT', 'B3_USDT', 'ANLOG_USDT', 'TST_USDT', 'CHEX_USDT', 'MBX_USDT', 
'BERA_USDT', 'ELON4AFD_USDT', 'STONKS_USDT', 'HOOD_USDT', 'FLAY_USDT', 'GANG_USDT', 'AIC_USDT', 
'GFM_USDT', 'VVV_USDT', 'TICO_USDT', 'SPA_USDT', 'SHX_USDT', 'SLC_USDT', 'GST_USDT', 
 'SAFEMOONSOL_USDT', 'VINE_USDT', 'SOSO_USDT', 'MELANIA_USDT', 'YULI_USDT', 
  'PLUME_USDT', '1DOLLAR_USDT', 'TRUMP_USDT', 'BGSC_USDT', 'VR_USDT', 
'SQD_USDT', 'TRISIG_USDT', 'VADER_USDT', 'GPS_USDT', 'BSX_USDT']




# fudu_list = []  # 用来存储每个交易对和对应的fudu
big_list = []
for symbols in symbols_list:
    list_a = max_value(symbols)
    time.sleep(1)
    big_list.append(list_a)

print(big_list)

import numpy as np
df = pd.DataFrame(big_list, columns=['交易对', '时间', '最大插针幅度'])
print(df)

# #cd /www/wwwroot/musk/test
# #python3 1bijia.py
# # 按fudu值从小到大排序
# # fudu_list.sort(key=lambda x: x[1])

#                  交易对                  时间   最大插针幅度
# 0           KET_USDT 2025-02-19 08:00:00    17.87
# 1          VIVI_USDT 2025-02-19 04:00:00    31.73
# 2          XOXO_USDT 2025-02-18 16:00:00    31.23
# 3          ONON_USDT 2025-02-19 20:00:00    47.55
# 4         LIBRA_USDT 2025-02-15 03:00:00   202.20
# 5          WINK_USDT 2025-02-15 12:00:00    30.65
# 6        ARCSOL_USDT 2025-02-13 14:00:00    34.14
# 7      BROCCOLI_USDT 2025-02-13 20:00:00    71.36
# 8       BROWNIE_USDT 2025-02-13 16:00:00  3369.81
# 9         SHELL_USDT 2025-02-13 14:00:00   137.39
# 10     FULLSEND_USDT 2025-02-13 12:00:00   864.30
# 11   CAPTAINBNB_USDT 2025-02-13 13:00:00   137.64
# 12          HEI_USDT 2025-02-13 08:00:00    24.11
# 13          DIN_USDT 2025-02-14 12:00:00   274.54
# 14           IP_USDT 2025-02-20 20:00:00    52.65
# 15          AVL_USDT 2025-02-12 10:00:00   403.82
# 16           G7_USDT 2025-02-12 12:00:00   139.41
# 17        LAYER_USDT 2025-02-11 15:00:00    28.29
# 18         TJRM_USDT 2025-02-21 23:00:00    19.82
# 19          OKM_USDT 2025-02-19 20:00:00    24.63
# 20          CAR_USDT 2025-02-11 02:00:00    99.78
# 21    JAILSTOOL_USDT 2025-02-10 14:00:00   121.65
# 22           B3_USDT 2025-02-10 13:00:00   298.24
# 23        ANLOG_USDT 2025-02-10 11:00:00   133.73
# 24          TST_USDT 2025-02-08 21:00:00    50.47
# 25         CHEX_USDT 2025-02-07 20:00:00     9.79
# 26          MBX_USDT 2025-02-07 18:00:00     8.12
# 27         BERA_USDT 2025-02-06 12:00:00    58.88
# 28     ELON4AFD_USDT 2025-02-05 05:00:00    63.64
# 29       STONKS_USDT 2025-02-03 04:00:00    30.89
# 30         HOOD_USDT 2025-02-17 16:00:00    58.54
# 31         FLAY_USDT 2025-02-01 09:00:00    69.79
# 32         GANG_USDT 2025-01-31 19:00:00    50.68
# 33          AIC_USDT 2025-01-30 04:00:00    39.28
# 34          GFM_USDT 2025-01-30 22:00:00    60.75
# 35          VVV_USDT 2025-01-28 07:00:00    24.77
# 36         TICO_USDT 2025-02-06 18:00:00    57.72
# 37          SPA_USDT 2025-02-03 01:00:00    31.71
# 38          SHX_USDT 2025-01-27 14:00:00     9.74
# 39          SLC_USDT 2025-02-02 20:00:00    44.29
# 40          GST_USDT 2025-01-27 07:00:00    12.83
# 41  SAFEMOONSOL_USDT 2025-01-24 13:00:00    61.74
# 42         VINE_USDT 2025-01-25 05:00:00    43.93
# 43         SOSO_USDT 2025-01-24 10:00:00   120.80
# 44      MELANIA_USDT 2025-01-20 01:00:00    48.90
# 45         YULI_USDT 2025-01-23 12:00:00    83.90
# 46        PLUME_USDT 2025-01-21 09:00:00    41.78
# 47      1DOLLAR_USDT 2025-01-20 23:00:00    51.83
# 48        TRUMP_USDT 2025-01-18 03:00:00    44.91
# 49         BGSC_USDT 2025-02-03 01:00:00    17.66
# 50           VR_USDT 2025-02-02 21:00:00    27.25
# 51          SQD_USDT 2025-01-20 14:00:00    13.40
# 52       TRISIG_USDT 2025-01-25 16:00:00    31.46
# 53        VADER_USDT 2025-02-01 19:00:00    25.41
# 54          GPS_USDT 2025-02-05 09:00:00    27.15
# 55          BSX_USDT 2025-01-16 10:00:00    58.75
