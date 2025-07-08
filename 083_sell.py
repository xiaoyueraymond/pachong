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
import asyncio

# Get the current Python script file path
current_script_path = os.path.abspath(sys.argv[0])
current_script_directory = os.path.dirname(current_script_path)
# logger.debug(f"当前脚本文件路径: {current_script_path}")
# logger.debug(f"当前脚本文件所在目录: {current_script_directory}")

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


exchange_bitget = ccxt.bitget({
    'apiKey': 'bg_085ae54090778b54aa3dee9ebb3cc614',
    'secret': '274e8ccd08c01bf502a308993668f59967018e5e3e817d90b44433d6d5ab7eaf',
    'password': 'zhuan3000wan'
})

    
def sell_biget():
    max_price = 0
    sleeptime = 0.1
    while True:

        try:
            order_book = exchange_bitget.fetch_order_book(symbols)
            ask_prices = order_book['asks']
            if len(ask_prices) > 0:
                ask_price = ask_prices[0][0]  # 获取最优买入价 
                
                logger.debug(f"{symbols} 最新报价: 成本价是：{buy_prices}  保本价是: {chengben_prices}  最新价格是：{ask_price} ")
                time.sleep(sleeptime)
            else:
                raise ValueError("No ask prices available")
        except Exception as e:
            logger.debug(f"An error occurred while fetching ask price: {e}")
            time.sleep(sleeptime)  # 等待然后重试
    

        try:
            balance = exchange_bitget.fetch_balance()
            size = float(balance[symbol]['total'])
            logger.debug(f"拥有的数量是: {size}")
            time.sleep(sleeptime) 
        except Exception as e:
            logger.debug(f"An error occurred while fetching balance: {e}")
            time.sleep(sleeptime) 

        
        # 更新最大价格
        try:      
            if ask_price > max_price:
                max_price = ask_price
                logger.debug(f"更新最大价格: {max_price}")

            # 检查卖出条件
            max_drop_condition = (ask_price < max_price * 0.9999) and (ask_price > buy_prices)

            if max_drop_condition :
                current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%')[:-3]
                logger.debug(f"出售时间:{current_time}")
                order_cancel = exchange_bitget.cancel_all_orders(symbols)
                order = exchange_bitget.create_limit_sell_order(symbols,size,200)
                time.sleep(sleeptime) 
                logger.debug(f"Sell Order:{order}")
        except Exception as e:
            logger.debug(f"An error occurred while selling: {e}")
            time.sleep(sleeptime) 

#cd /www/wwwroot/musk/test
#python3 083_sell.py
# 开局直接开始卖，开局要高于成本价，并且一直涨就不卖，如果跌，立马卖。成本价是关键，还有加上手动操作，停掉程序，直接卖掉，所以要反复确认成本。

# 设置交易参数
symbol = 'SKYAI'
symbols = f'{symbol}/USDT'
buy_prices = 0.083
chengben_prices = buy_prices * 1.03

sell_biget()

