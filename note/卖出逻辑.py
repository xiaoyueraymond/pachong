import ccxt
from datetime import datetime
import pytz
import time
import sys  # Import sys to enable exiting the program
from pytz import timezone
import logging
import os
import sys
import threading

current_directory = os.getcwd()

# 生成带有时间前缀的日志文件名
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f"{current_time}_log.txt"
log_file_path = os.path.join(current_directory, log_file_name)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the log recording level to DEBUG

# Create a file handler, specify a log file path and encoding
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)  # Set the file handler level to WARNING

# 假设 BeijingTimeFormatter 是自定义的格式化类
# 如果没有自定义，可使用 logging.Formatter 代替
# file_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create a stream handler to output logs to the terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # Set the stream handler level to DEBUG

# 假设 BeijingTimeFormatter 是自定义的格式化类
# 如果没有自定义，可使用 logging.Formatter 代替
# stream_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
stream_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)




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


exchange_htx = ccxt.htx({
    'apiKey': 'vftwcr5tnh-07f545cd-be748f53-f078c',
    'secret': '4e49bc29-fb067f15-10dc62e0-36146'
})

exchange_bingx = ccxt.bingx()
# markets = exchange_mexc.fetch_markets()

exchange_kucoin = ccxt.kucoin()


a = 1
sell_running_gate = False  # 标志变量，指示 sell() 是否正在运行
sell_running_mexc = False

def update_a():
    global a
    while True:
        # 从 1 增加到 10，然后重置为 1
        if a < 10:
            a += 1
        else:
            a = 1
        logger.debug(f"Updated value of a: {a}")
        time.sleep(1)  # 每秒更新一次

def sell():
    global sell_running_gate, sell_running_mexc  # 声明为全局变量
    while True:
        if sell_running_gate:
            logger.debug("gate执行卖出操作")
            time.sleep(1)  # 模拟卖出操作的延迟
            # sell_running_gate = False  # 重置标志

        if sell_running_mexc:
            logger.debug("mexc执行卖出操作")
            time.sleep(1)  # 模拟卖出操作的延迟
            # sell_running_mexc = False  # 重置标志

sell_running = False  # 标志变量，指示 sell() 是否正在运行
def test():
    while True:
        global sell_running_gate,sell_running_mexc
        try: 
            # 当 a 大于 0 时触发 sell
            if a > 5:
                sell_running_gate = True
            
            # 当 a 大于 1 时触发 sell
            if a > 8:
                # 启动 sell 函数的线程
                sell_running_mexc = True
            
            time.sleep(1)  # 每秒检查一次
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            time.sleep(1)

#这是买入之后，达到x = 0.9的差值，自动卖出。

if __name__ == "__main__":
    # 启动更新 a 的线程
    update_thread = threading.Thread(target=update_a)
    update_thread.start()
    sell_thread = threading.Thread(target=sell)
    sell_thread.start()    
    # 启动测试函数
    test()

