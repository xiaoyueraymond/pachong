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

beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)
print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))



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





def gate_mexc_bingx(symbols):
    while True:
        try:
            order_book_bingx = exchange_bingx.fetch_order_book(symbols)
            order_book_mexc = exchange_mexc.fetch_order_book(symbols)
            order_book_gate = exchange_gate.fetch_order_book(symbols)

        

            if len(order_book_bingx['asks']) < 1 or len(order_book_gate['asks']) < 1 or len(order_book_mexc['asks']) < 1 :
                logger.debug('符号 {} 的订单簿中没有足够的出价记录'.format(symbols))
                continue
            price_bingx = order_book_bingx['asks'][0][0]
            price_gate = order_book_gate['asks'][0][0]
            price_mexc = order_book_mexc['asks'][0][0]

            balance = exchange_mexc.fetch_balance()
            mexc_balance = balance['USDT']['free']
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            logger.debug(f'USDT:(mexc: {order_book_mexc['asks']}, GATE: {gate_balance})')

            balance = exchange_gate.fetch_balance()
            gate_balance = next((float(info['available']) for info in balance['info'] if info['currency'] == 'USDT'), 0)

            logger.debug(f'USDT:(mexc: {mexc_balance}, GATE: {gate_balance})')
            # logger.debug(f'{symbols}(mexc: {price_mexc},bingx: {price_bingx}, GATE: {price_gate})')
            chazhi = 0.9
            time.sleep(0.1)

            if price_mexc < price_gate * chazhi and price_mexc < price_bingx * chazhi:
                logger.debug(f'{symbols}(mexc: {price_mexc},bingx: {price_bingx}, GATE: {price_gate}),启动买入程序')
                try: 
                    # order = exchange_mexc.create_limit_buy_order(symbols,int(mexc_balance / price_mexc),price_mexc)
                    time.sleep(0.5)
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    # logger.debug(f"Buy Order: {order}")  
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}") 

            elif price_gate < price_mexc * chazhi and price_gate < price_bingx * chazhi:
                logger.debug(f'{symbols}(mexc: {price_mexc},bingx: {price_bingx}, GATE: {price_gate}),启动买入程序')
                try: 
                    # order = exchange_gate.create_limit_buy_order(symbols,int(gate_balance / price_gate),price_gate)
                    time.sleep(0.5)
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    # logger.debug(f"Buy Order: {order}")  
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")  
            else:
                logger.debug(f'{symbols} 价格未达到预想差价 (bingx: {price_bingx}, GATE: {price_gate}, MEXC:{price_mexc})')                  
        except Exception as e:
            logger.debug(f"An error occurred while fetching ask price: {e}")
            time.sleep(0.1)  # 
#cd /www/wwwroot/musk/test

symbols = 'BTC/USDT'

beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)
print("程序启动时间:", datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


if __name__ == "__main__":
    # h2('XTER/USDT')
    gate_mexc_bingx(symbols)

