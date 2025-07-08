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
print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))

exchange_mexc =ccxt.bitmart

exchange_mexc = ccxt.mexc({
    'apiKey': 'mx0vgl5G1KVhIHgumR',
    'secret': '36243c260d484cf0aba85cd464fbec20'
})

exchange_bitget = ccxt.bitget({
    'apiKey': 'bg_085ae54090778b54aa3dee9ebb3cc614',
    'secret': '274e8ccd08c01bf502a308993668f59967018e5e3e817d90b44433d6d5ab7eaf',
    'password': 'zhuan3000wan'
})

exchange_gate = ccxt.gateio({
    'apiKey': 'd9ebc00738f9942017b6ee37f7ad1861',
    'secret': '3dae582af173e36614edfb43a2b23275649ffea66c2e37a43fd7ffdcf567ff45'
})

exchange_htx = ccxt.htx({
    'apiKey': 'vftwcr5tnh-07f545cd-be748f53-f078c',
    'secret': '4e49bc29-fb067f15-10dc62e0-36146'
})


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
symbols = 'KMNO/USDT'
timeframe = '1d'
limit = 190
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

# symbols_list = ['FIS/USDT','MEMEFI/USDT','INIT/USDT','DEEP/USDT','HYPER/USDT',
#                 'BANK/USDT','EPT/USDT','AERGO/USDT',
#                 'WCT/USDT','KERNEL/USDT','XCN/USDT','ONDO/USDT','BIGTIME/USDT',
#                 'VIRTUAL/USDT','PROMPT/USDT','FORTH/USDT','BABY/USDT',
#               'ATH/USDT','GUN/USDT','MLN/USDT']

#Z这是种子标签，记录从币安出现到现在的涨跌幅，按第一天来计算和第五天
symbols_list = [
     "STO/USDT", "SIGN/USDT", "INIT/USDT", "HYPER/USDT", 
    "WCT/USDT", "KERNEL/USDT", "ONDO/USDT", "BIGTIME/USDT", "BABY/USDT", "GUN/USDT", 
    "MUBARAK/USDT", "BROCCOLI714/USDT", "PARTI/USDT", "NIL/USDT", "FORM/USDT", 
    "BMT/USDT", "EPIC/USDT", "RED/USDT", "GPS/USDT", "SHELL/USDT", "KAITO/USDT", "HEI/USDT", 
    "LAYER/USDT", "1000CHEEMS/USDT", "TST/USDT", "BERA/USDT", "ANIME/USDT", "TRUMP/USDT", 
    "SOLV/USDT", "S/USDT", "AIXBT/USDT", "CGPT/USDT", "COOKIE/USDT", "D/USDT", "BIO/USDT", 
    "USUAL/USDT", "1000CAT/USDT", "PENGU/USDT", "VANA/USDT", "VELODROME/USDT", "ME/USDT", 
    "MOVE/USDT", "ACX/USDT", "ORCA/USDT"
]


fudu_list = []  

for i in symbols_list:
    bars = exchange_bn.fetch_ohlcv(i, timeframe=timeframe, limit=limit)
    time.sleep(0.1)
    fudu = (bars[-1][-2] - bars[4][-2]) / bars[4][-2] * 100  # 转换为百分比
    fudu = round(fudu, 2)  # 保留两位小数
    fudu_list.append((i, fudu))  # 将交易对和fudu值添加到列表中

#cd /www/wwwroot/musk/test
#python3 1bijia.py
# 按fudu值从小到大排序
# fudu_list.sort(key=lambda x: x[1])

# 打印排序后的结果
for i, fudu in fudu_list:
    print(f'{i}  {fudu}%')

for i, fudu in fudu_list:
    print(f'{i}')

for i, fudu in fudu_list:
    print(f'{fudu}%')   
    
# print('-----------------------------------------------------------------------')
# fudu_list.sort(key=lambda x: x[1], reverse=True)
# # 打印最大 10 个元素及其和
# max_10 = fudu_list[:10]  # 取前 10 个元素
# max_10_sum = sum([fudu for i, fudu in max_10])  # 计算最大 10 个元素的和
# print("最大 10 个元素及其和：")
# for i, fudu in max_10:
#     print(f'{i}  {fudu}%')
# print(f"最大 10 个元素的和: {max_10_sum}%")

# # 打印最小 10 个元素及其和
# min_10 = fudu_list[-10:]  # 取后 10 个元素
# min_10_sum = sum([fudu for i, fudu in min_10])  # 计算最小 10 个元素的和
# print("\n最小 10 个元素及其和：")
# for i, fudu in min_10:
#     print(f'{i}  {fudu}%')
# print(f"最小 10 个元素的和: {min_10_sum}%")