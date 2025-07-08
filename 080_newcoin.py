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



# Define proxies
proxies = {
    # 'http': 'http://127.0.0.1:10809',
    
    # 'https': 'http://127.0.0.1:10809'
}



# Initialize exchanges
exchange_mexc = ccxt.mexc({
  'proxies': proxies
})

# Correct initialization for other exchanges
exchange_xt = ccxt.xt({
    'proxies': proxies
})

exchange_lbank = ccxt.lbank({
    'proxies': proxies
})

exchange_bitmart = ccxt.bitmart({
    'proxies': proxies
})

exchange_kucoin = ccxt.kucoin({
    'proxies': proxies
})

exchange_bingx = ccxt.bingx({
    'proxies': proxies
})

exchange_bybit = ccxt.bybit({
    'proxies': proxies
})

exchange_bitget = ccxt.bitget({
    'proxies': proxies
})

exchange_htx = ccxt.htx({
    'proxies': proxies
})

exchange_gateio = ccxt.gateio({
    'proxies': proxies
})

exchange_binance = ccxt.binance({
    'proxies': proxies
})

exchange_okex = ccxt.okx({
    'proxies': proxies
})

exchange_bitget = ccxt.bitget({
    'proxies': proxies
})










#cd /www/wwwroot/musk/test
#这个脚本是看下新币有没有在这些三级交易所上线，价格是多少


def get_coin(symbols):
    print(f'-------------------------------------------{symbols}---------------------------------------------------------')
    time.sleep(0.1)
    try:
        order_book_mexc = exchange_mexc.fetch_order_book(symbols)
        price_mexc = order_book_mexc['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_mexc:{price_mexc}')
    except Exception as e:
        logger.debug(f" Mexc: {e}")
        price_mexc = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing
        
    try:
        order_book_xt = exchange_xt.fetch_order_book(symbols)
        price_xt = order_book_xt['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_xt:{price_xt}')
    except Exception as e:
        logger.debug(f" xt: {e}")
        price_xt = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_lbank = exchange_lbank.fetch_order_book(symbols)
        price_lbank = order_book_lbank['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_lbank:{price_lbank}')
    except Exception as e:
        logger.debug(f" lbank: {e}")
        price_lbank = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_bitmart = exchange_bitmart.fetch_order_book(symbols)
        price_bitmart = order_book_bitmart['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_bitmart:{price_bitmart}')
    except Exception as e:
        logger.debug(f" bitmart: {e}")
        price_bitmart = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_kucoin = exchange_kucoin.fetch_order_book(symbols)
        price_kucoin = order_book_kucoin['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_kucoin:{price_kucoin}')
    except Exception as e:
        logger.debug(f" kucoin: {e}")
        price_kucoin = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_bingx = exchange_bingx.fetch_order_book(symbols)
        price_bingx = order_book_bingx['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_bingx:{price_bingx}')
    except Exception as e:
        logger.debug(f" bingx: {e}")
        price_bingx = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing
    
    try:
        order_book_bybit = exchange_bybit.fetch_order_book(symbols)
        price_bybit = order_book_bybit['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_bybit:{price_bybit}')
    except Exception as e:
        logger.debug(f" bybit: {e}")
        price_bybit = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_bitget = exchange_bitget.fetch_order_book(symbols)
        price_bitget = order_book_bitget['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_bitget:{price_bitget}')
    except Exception as e:
        logger.debug(f" bitget: {e}")
        price_bitget = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_gateio = exchange_gateio.fetch_order_book(symbols)
        price_gateio = order_book_gateio['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_gateio:{price_gateio}')
    except Exception as e:
        logger.debug(f" gateio: {e}")
        price_gateio = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing

    try:
        order_book_htx = exchange_htx.fetch_order_book(symbols)
        price_htx = order_book_htx['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_htx:{price_htx}')
    except Exception as e:
        logger.debug(f" htx: {e}")
        price_htx = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing      

    try:
        order_book_binance = exchange_binance.fetch_order_book(symbols)
        price_binance = order_book_binance['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_binance:{price_binance}')
    except Exception as e:
        logger.debug(f" binance: {e}")
        price_binance = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing 

    try:
        order_book_okex = exchange_okex.fetch_order_book(symbols)
        price_okex = order_book_okex['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_okex:{price_okex}')
    except Exception as e:
        logger.debug(f" okex: {e}")
        price_okex = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing 

    try:
        order_book_bitget = exchange_bitget.fetch_order_book(symbols)
        price_bitget = order_book_bitget['asks'][0][0]  # Fetch ask price only if order book fetch is successful
        print(f'price_bitget:{price_bitget}')
    except Exception as e:
        logger.debug(f" bitget: {e}")
        price_bitget = None  # Default value if there's an error
        time.sleep(0.1)  # Sleep for a short period before retrying or continuing 

#这是一个用来查看交易所上币情况的信息，如果有上架，就有交易对，没有就没有改交易对



symbols_list=  ['PBT/USDT', 'SGC/USDT', 'BCHEM/USDT', 'NRWA/USDT']
#cd /www/wwwroot/musk/test
#python3 080_newcoin.py 


for symbols in symbols_list:
    get_coin(symbols)

