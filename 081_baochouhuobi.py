from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import ccxt
from datetime import datetime
import pytz
import time
import sys  # Import sys to enable exiting the program
from pytz import timezone
import logging
import os
import sys

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
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)

exchange_mexc = ccxt.mexc({
    'apiKey': 'mx0vgl1QiZ36NFO0Mx',
    'secret': '27983933291d44a5a64186022fb45d12'
})

exchange_bitget = ccxt.bitget({
    'apiKey': 'bg_085ae54090778b54aa3dee9ebb3cc614',
    'secret': '274e8ccd08c01bf502a308993668f59967018e5e3e817d90b44433d6d5ab7eaf',
    'password': 'zhuan3000wan',
    'proxies': proxies
})

exchange_gate = ccxt.gateio({
    'apiKey': '61f0e2f9e4affb50893e87f90a359080',
    'secret': 'd915d19823d825031234b08f54016bc2f6355e454ef6bd8aef26f98defbb3012',
    'proxies': proxies
})


exchange_htx = ccxt.htx({
    'apiKey': 'vftwcr5tnh-07f545cd-be748f53-f078c',
    'secret': '4e49bc29-fb067f15-10dc62e0-36146',
    'proxies': proxies
})

exchange_bingx = ccxt.bingx()
# markets = exchange_mexc.fetch_markets()

exchange_kucoin = ccxt.kucoin()


exchange_okex = ccxt.okx({
    'apiKey': '1153f253-bf96-4789-a2dc-379bffad2474',
    'secret': 'EA724612A773FA010562A596946E6C95',
    'password':'rfvRFV123!@#',
    'proxies': proxies
})

exchange_lbank = ccxt.lbank({'proxies': proxies})

# 初始化浏览器并获取最新的标签页
browser = Chromium()
page = browser.latest_tab



# //input[@autocomplete='off']
# 


from DrissionPage.common import Actions


def gate_mexc_bitget_htx():

    while True:
        try:
            order_book_bitget = exchange_bitget.fetch_order_book(symbols)
            order_book_htx = exchange_htx.fetch_order_book(symbols)
            order_book_mexc = exchange_mexc.fetch_order_book(symbols)
            order_book_gate = exchange_gate.fetch_order_book(symbols)
            order_book_lbank = exchange_lbank.fetch_order_book(symbols)
            time.sleep(xunjia_time)
            if len(order_book_bitget['asks']) < 1 or len(order_book_gate['asks']) < 1 or len(order_book_mexc['asks']) < 1 :
                logger.debug(f'符号 {symbols} 的订单簿中没有足够的出价记录')
                continue
                time.sleep(xunjia_time)

            price_bitget = order_book_bitget['asks'][0][0]
            price_gate = order_book_gate['asks'][0][0]
            price_mexc = order_book_mexc['asks'][0][0]
            price_htx = order_book_htx['asks'][0][0]
            amount_htx = order_book_htx['asks'][0][1]
            # print( order_book_htx['asks'])

            x, y = calculate_diff(price_bitget, price_gate, price_mexc)
            logger.debug(f'{symbols}(mexc: {price_mexc},bitget: {price_bitget}, gate: {price_gate},htx: {price_htx}) (差值1：{x} , 差值2:{y})')
            
            time.sleep(xunjia_time)

            if (order_book_htx['asks'][4][0]) < price_gate * chazhi and (order_book_htx['asks'][4][0]) < price_bitget * chazhi:
                logger.debug(f'{symbols}(mexc: {price_mexc},bitget: {price_bitget}, gate: {price_gate}),htx 启动买入程序:{price_htx}')
                try: 
                    order_cancel = exchange_htx.cancel_all_orders(symbols)
                    time.sleep(guadan_time)
                    fuckhtx(price_htx,amount_htx)
                    pass
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}") 
                    time.sleep(guadan_time)

        except Exception as e:
            logger.debug(f"An error occurred while fetching ask price: {e}")
            time.sleep(xunjia_time)  # 


def lbank_htx():

    while True:
        try:

            order_book_htx = exchange_htx.fetch_order_book(symbols)
            order_book_lbank = exchange_lbank.fetch_order_book(symbols)
            time.sleep(xunjia_time)
            if len(order_book_lbank['asks'])  < 1 or len(order_book_htx['asks']) < 1 :
                logger.debug(f'符号 {symbols} 的订单簿中没有足够的出价记录')
                continue
                time.sleep(xunjia_time)

            price_lbank = order_book_lbank['asks'][0][0]
            price_htx = order_book_htx['asks'][0][0]
            amount_htx = order_book_htx['asks'][0][1]
            # print( order_book_htx['asks'])

            x= calculate_diff2(price_lbank, price_htx)

            logger.debug(f'{symbols}(htx: {price_htx}, lbank: {price_lbank}) (差值1：{x}')
            
            time.sleep(xunjia_time)

            if (order_book_htx['asks'][4][0]) < price_lbank * chazhi :
                logger.debug(f'{symbols}(htx: {price_htx}, lbank: {price_lbank}),htx 启动买入程序:{price_htx}')
                try: 
                    order_cancel = exchange_htx.cancel_all_orders(symbols)
                    time.sleep(guadan_time)
                    fuckhtx(price_htx,amount_htx)
                    pass
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}") 
                    time.sleep(guadan_time)

        except Exception as e:
            logger.debug(f"An error occurred while fetching ask price: {e}")
            time.sleep(xunjia_time)  # 

def fuckhtx(price_htx,amount_htx):

    # page.ele("x://button[@class='type-item']").click()
    # time.sleep(2)
    # page.ele("x://button[@class='type-item cur']").click()
    # time.sleep(2)
    page.ele("x://input[@data-v-26c898f1]").clear()
    page.ele("x://input[@data-v-26c898f1]").input(price_htx)
    # time.sleep(4)
    # page.actions.key_down('Tab')
    # page.actions.key_up('Tab')
    # page.actions.key_down('Tab')
    # page.actions.key_up('Tab')
    page.ele("x:(//input[@data-v-26c898f1])[2]").clear()
    page.ele("x:(//input[@data-v-26c898f1])[2]").input(amount_htx)
    # page.ele("x:(//input[@data-v-26c898f1])[3]").input(5.4)
    page.ele("x://button[@class='submit-btn buy']").click()
    # //button[@class='submit-btn buy']

def calculate_diff2(a, b):
    # 将三个参数放入列表中并排序
    sorted_lst = sorted([a, b])
    max_value = sorted_lst[1]
    
    # 计算差值
    diff1 = round(max_value / sorted_lst[0], 2)
    return diff1  
  
def calculate_diff(a, b, c):
    # 将三个参数放入列表中并排序
    sorted_lst = sorted([a, b, c])
    min_value = sorted_lst[0]
    
    # 计算差值
    diff1 = round(min_value / sorted_lst[1], 2)
    diff2 = round(min_value / sorted_lst[2], 2)

    return diff1, diff2
 

#定义询价间隔
xunjia_time = 0.1
#定义挂单间隔
guadan_time = 1

chazhi = 0.6
symbol = 'szn'
# chazhi = 1.2
# symbol = 'btc'
url = f'https://www.htx.com/zh-cn/trade/{symbol}_usdt?type=spot'
page.get(url)
symbols = f'{symbol.upper()}/USDT'
# lbank_htx()
while True:
    