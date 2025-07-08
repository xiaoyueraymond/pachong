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
logger.debug("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))


API_KEY = 'mx0vgl5G1KVhIHgumR'
SECRET = '36243c260d484cf0aba85cd464fbec20'

exchange_mexc = ccxt.mexc({
    'apiKey': API_KEY,
    'secret': SECRET
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

def buy():
    # global ask_prices, buy_prices, max_price,order
    while True:
        try:
            order = exchange_gate.create_limit_buy_order(symbols, buy_amount, buy_prices)
            logger.debug(f'Buy Order:{order}')
            # order_id = order['id']
            # logger.debug(f"Order ID: {order_id}")
            
            # # 检查订单
            # # order_info = exchange.fetch_order(order_id, symbols)
            # # order_status = order_info['info']['status']
            # logger.debug(f"Order Status: {order_status}")
            # logger.debug(order_info)
            #暂时不知道订单完成的状态,太快了，系统反应不过来
            # if order_status == 'open':
            #     exchange.cancel_order(order_id, symbols)
            #     sys.exit("未完成最低价买入操作，程序终止。")    
            # if order_status == 'live':
            #     buy_prices = float(order_info['info']['price'])  # 确保获取到 avg_deal_price
            #     max_price = buy_prices
            # break
        except Exception as e:
            logger.debug(f"An error occurred during buying: {e}")
            time.sleep(0.1)

symbolsm = 'GAMEVIRTUAL'
symbols = f'{symbolsm}/USDT'
my_monney = 8
now_prices = 0.25
buy_prices = now_prices * 0.8
buy_amount = int(my_monney/buy_prices)

# zhangfu =  5 / 100
# sell_price = buy_prices * (1 + zhangfu)
logger.debug("现价是{}:".format(now_prices))
logger.debug("抄底价是{}:".format(buy_prices))


beijing_tz = timezone('Asia/Shanghai')

def wait_until_target_time(target_time, target_time2):
    while True:
        now = datetime.now(beijing_tz)
        # 检查当前时间是否小于目标时间
        if now < target_time:
            pass
        # 检查当前时间是否等于或超过目标时间，同时检查毫秒部分
        elif target_time <= now < target_time2:
            buy()
            break
        time.sleep(0.1)  # 减少CPU使用，微调等待精度

def buy():
    print("执行买入操作")

if __name__ == "__main__":
    target_time = datetime.now(beijing_tz).replace(hour=19, minute=59, second=58, microsecond=0)
    target_time2 = datetime.now(beijing_tz).replace(hour=20, minute=1, second=0, microsecond=0)
    
 
    wait_until_target_time(target_time, target_time2)