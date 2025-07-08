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
log_file_path = os.path.join(current_script_directory, 'makemoney.log')

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
file_handler.setLevel(logging.DEBUG)  # Set the file handler level to WARNING
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


####################################################################


exchange_bn = ccxt.binanceusdm({
    'apiKey': '1J1Kyk7a6gL8nl7wklOHmFhaMkcRJ1RO9QytTLNMi5gRjKm3nkJOyiLp9cW3A4DT',
    'secret': 'qS7AfSQQOQp6o89qDkZGiLs0kSzYfR0PJoxodVBf3MmyUlmTUFVfWsD8BqPkJXWd'
})

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



exchange_bingx = ccxt.bingx()
# markets = exchange_mexc.fetch_markets()

exchange_kucoin = ccxt.kucoin()


    # print(exchange_bn.fetch_ticker('BTC/USDT'))
    # symbols = 'BTC/USDT'
    # timeframe = '1h'
    # limit = 5
    # bars = exchange_bn.fetch_ohlcv(symbols, timeframe=timeframe, limit=limit)
    # df = pd.DataFrame(bars, columns=['时间', '开', '高', '低', '收', '数量'])
    
    # # 将时间列转换为日期时间对象
    # df['时间'] = pd.to_datetime(df['时间'], unit='ms')
    
    # # 设置时区为北京时间（中国标准时间，CST）
    # df['时间'] = df['时间'].dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    
    # print(df)
# 配置日志记录，将日志保存到当前目录下的 test.log 文件中

# cd /www/wwwroot/musk/test
# screen -S demo2 python3 bn_balance.py 

def test():

    while True:
        try:
            balance_bn = exchange_bn.fetch_balance()
            total_unrealized_profit = balance_bn['info']['totalUnrealizedProfit']
            logger.debug(total_unrealized_profit)
            time.sleep(3600)
        except Exception as e:
            logger.debug(f"An error occurred during fetch_balance: {e}")
            time.sleep(1) 
   
    
if __name__ == "__main__":
    # h2('XTER/USDT')
    # mexc_gate('LYP/USDT')
    # mexc_bitget('YULI/USDT')
    test()