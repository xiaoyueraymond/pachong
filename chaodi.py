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
    'apiKey': 'mx0vglwxo4oW0wKiym',
    'secret': '9220372c34924f8c9f90b111ac5a527e'
})

exchange_bitget = ccxt.bitget({
    'apiKey': 'bg_085ae54090778b54aa3dee9ebb3cc614',
    'secret': '274e8ccd08c01bf502a308993668f59967018e5e3e817d90b44433d6d5ab7eaf',
    'password': 'zhuan3000wan'
})

exchange_gate = ccxt.gateio({
    'apiKey': '61f0e2f9e4affb50893e87f90a359080',
    'secret': 'd915d19823d825031234b08f54016bc2f6355e454ef6bd8aef26f98defbb3012'
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


def mexc_gate():
    global sell_running_gate, sell_running_mexc, x , price_mexc, price_gate
    while True:
        try:
            order_book_mexc = exchange_mexc.fetch_order_book(symbols)
            order_book_gate = exchange_gate.fetch_order_book(symbols)

            # 检查 order_book['bids'] 是否有足够的元素
            if len(order_book_mexc['asks']) < 4 or len(order_book_gate['asks']) < 4 :
                logger.debug('符号 {} 的订单簿中没有足够的出价记录'.format(symbols))
                time.sleep(0.3)
                continue
            
            price_mexc = order_book_mexc['asks'][0][0]
            price_gate = order_book_gate['asks'][0][0]
            chazhi = 0.9
            x = calculate_diff(price_mexc,price_gate)
            # logger.debug(f'{symbols}:(MEXC: {price_mexc}, GATE: {price_gate})') 
            time.sleep(0.3)

            if  (order_book_gate['asks'][3][0])  < price_mexc * chazhi :
                sell_running_gate = True
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, GATE: {price_gate}),gate启动买入程序')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_gate.cancel_all_orders(symbols)
                    order = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][0][1]),(order_book_gate['asks'][0][0]))
                    order1 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][1][1]),(order_book_gate['asks'][1][0]))
                    order2 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][2][1]),(order_book_gate['asks'][2][0]))
                    order3 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][3][1]),(order_book_gate['asks'][3][0]))                
                    logger.debug(f"Buy Order: {order}{order1}{order2}{order3}")
                    # logger.debug("Buy Order:", order)  
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  
                    
            elif  (order_book_gate['asks'][2][0])  < price_mexc * chazhi :
                sell_running_gate = True
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, GATE: {price_gate}),gate启动买入程序')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_gate.cancel_all_orders(symbols)
                    order = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][0][1]),(order_book_gate['asks'][0][0]))
                    order1 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][1][1]),(order_book_gate['asks'][1][0]))
                    order2 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][2][1]),(order_book_gate['asks'][2][0]))               
                    logger.debug(f"Buy Order: {order}{order1}{order2}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  

            elif  (order_book_gate['asks'][1][0])  < price_mexc * chazhi :
                sell_running_gate = True
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, GATE: {price_gate}),gate启动买入程序')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_gate.cancel_all_orders(symbols)
                    order = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][0][1]),(order_book_gate['asks'][0][0]))
                    order1 = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][1][1]),(order_book_gate['asks'][1][0]))             
                    logger.debug(f"Buy Order: {order}{order1}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  

            elif  (order_book_gate['asks'][0][0])  < price_mexc * chazhi :
                sell_running_gate = True
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, GATE: {price_gate}),gate启动买入程序')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_gate.cancel_all_orders(symbols)
                    order = exchange_gate.create_limit_buy_order(symbols,(order_book_gate['asks'][0][1]),(order_book_gate['asks'][0][0]))               
                    logger.debug("Buy Order:", order)  
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  
        except Exception as e:
            # logger.debug(f"An error occurred while fetching ask price: {e}")
            pass
            time.sleep(0.1)  # 等待然后重试

 

def mexc_bitget(symbols):
    while True:
        try:
            order_book_mexc = exchange_mexc.fetch_order_book(symbols)
            order_book_bitget = exchange_bitget.fetch_order_book(symbols)

            
            # 检查 order_book['bids'] 是否有足够的元素
            if len(order_book_mexc['asks']) < 4 or len(order_book_bitget['asks']) < 4 :
                logger.debug('符号 {} 的订单簿中没有足够的出价记录'.format(symbols))
                continue
            
            price_mexc = order_book_mexc['asks'][0][0]
            price_bitget = order_book_bitget['asks'][0][0]
            x = calculate_diff(price_mexc,price_bitget)
            chazhi = 3
            time.sleep(0.1)

            if  (order_book_bitget['asks'][3][0]) * chazhi < price_mexc :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),bitget启动买入程序{price_bitget}')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_bitget.cancel_all_orders(symbols)
                    order = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][0][1]),(order_book_bitget['asks'][0][0]))
                    order1 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][1][1]),(order_book_bitget['asks'][1][0]))
                    order2 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][2][1]),(order_book_bitget['asks'][2][0]))
                    order3 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][3][1]),(order_book_bitget['asks'][3][0]))                
                    logger.debug(f"Buy Order: {order}{order1}{order2}{order3}")  

                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  
                                       
            elif  (order_book_bitget['asks'][2][0]) * chazhi < price_mexc :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),bitget启动买入程序{price_bitget}')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_bitget.cancel_all_orders(symbols)
                    order = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][0][1]),(order_book_bitget['asks'][0][0]))
                    order1 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][1][1]),(order_book_bitget['asks'][1][0]))
                    order2 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][2][1]),(order_book_bitget['asks'][2][0]))               
                    logger.debug(f"Buy Order: {order}{order1}{order2}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  

            elif  (order_book_bitget['asks'][1][0]) * chazhi < price_mexc :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),bitget启动买入程序{price_bitget}')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_bitget.cancel_all_orders(symbols)
                    order = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][0][1]),(order_book_bitget['asks'][0][0]))
                    order1 = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][1][1]),(order_book_bitget['asks'][1][0]))             
                    logger.debug(f"Buy Order: {order}{order1}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  

            elif  (order_book_bitget['asks'][0][0]) * chazhi < price_mexc :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),bitget启动买入程序{price_bitget}')
                # logger.debug('{} 价格相差10%'.format(symbols)) 
                try: 
                    order_cancel = exchange_bitget.cancel_all_orders(symbols)
                    order = exchange_bitget.create_limit_buy_order(symbols,(order_book_bitget['asks'][0][1]),(order_book_bitget['asks'][0][0]))               
                    logger.debug("Buy Order:", order)  
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")   
                    time.sleep(1)  


            elif  order_book_mexc['asks'][3][0] * chazhi < price_bitget :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),mexc启动买入程序')  
                try:
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    order = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][0][1]),(order_book_mexc['asks'][0][0]))
                    order1 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][1][1]),(order_book_mexc['asks'][1][0]))
                    order2 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][2][1]),(order_book_mexc['asks'][2][0]))
                    order3 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][3][1]),(order_book_mexc['asks'][3][0]))
                    logger.debug(f"Buy Order: {order}{order1}{order2}{order3}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")
                    time.sleep(1) 

            elif  order_book_mexc['asks'][2][0] * chazhi < price_bitget :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),mexc启动买入程序')  
                try:
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    order = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][0][1]),(order_book_mexc['asks'][0][0]))
                    order1 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][1][1]),(order_book_mexc['asks'][1][0]))
                    order2 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][2][1]),(order_book_mexc['asks'][2][0]))
                    logger.debug(f"Buy Order: {order}{order1}{order2}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")
                    time.sleep(1) 

            elif  order_book_mexc['asks'][1][0] * chazhi < price_bitget :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),mexc启动买入程序')  
                try:
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    order = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][0][1]),(order_book_mexc['asks'][0][0]))
                    order1 = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][1][1]),(order_book_mexc['asks'][1][0]))
                    logger.debug(f"Buy Order: {order}{order1}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")
                    time.sleep(1) 

            elif  order_book_mexc['asks'][0][0] * chazhi < price_bitget :
                price_difference = abs((price_mexc - price_bitget) / price_bitget) * 100
                logger.debug(f'{symbols} 价格相差 {x}倍 (MEXC: {price_mexc}, bitget: {price_bitget}),mexc启动买入程序')  
                try:
                    order_cancel = exchange_mexc.cancel_all_orders(symbols)
                    order = exchange_mexc.create_limit_buy_order(symbols,(order_book_mexc['asks'][0][1]),(order_book_mexc['asks'][0][0]))
                    logger.debug(f"Buy Order: {order}") 
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}")
                    time.sleep(1) 

            else:
                logger.debug(f'{symbols} 价格未达到 {chazhi * 100:.2f}% (MEXC: {price_mexc}, bitget: {price_bitget})，差值：{x}')                  
        except Exception as e:
            pass
            time.sleep(0.1)  # 等待然后重试

def calculate_diff(a, b):
    # 将三个参数放入列表中并排序
    sorted_lst = sorted([a, b])
    max_value = sorted_lst[1]
    
    # 计算差值
    diff1 = round(max_value / sorted_lst[0], 2)
    return diff1

def mexc_gate_sell():
    global sell_running_gate, sell_running_mexc,x  # 声明为全局变量
    while True:
        if x < 1.06 and sell_running_gate:
            try: 
                logger.debug("gate执行卖出操作")
                balance = exchange_gate.fetch_balance()
                # logger.debug(f"{balance}") 
                symbols_balance_gate = balance['total'][f'{symbol}'] 
                logger.debug(f"{symbol}: {symbols_balance_gate}") 
                # order_cancel = exchange_gate.cancel_all_orders(symbols)  
                order = exchange_gate.create_limit_sell_order(symbols,symbols_balance_gate,price_gate)  
                logger.debug(order)
                time.sleep(1)  # 模拟卖出操作的延迟
                # sell_running_gate = False  # 重置标志
                order_cancel = exchange_gate.cancel_all_orders(symbols)  
            except Exception as e:
                logger.debug(f"An error occurred during selling: {e}")
                time.sleep(1) 

        elif x < 1.3 and sell_running_mexc:
            try: 
                logger.debug("mexc执行卖出操作")  
                balance = exchange_gate.fetch_balance()
                # logger.debug(f"{balance}") 
                symbols_balance_mexc = balance['total'][f'{symbol}'] 
                logger.debug(f"{symbol}: {symbols_balance_mexc}") 
                # order_cancel = exchange_gate.cancel_all_orders(symbols)       
                order = exchange_gate.create_limit_sell_order(symbols,symbols_balance_mexc,price_mexc)
                logger.debug(order)
                time.sleep(1)
                order_cancel = exchange_mexc.cancel_all_orders(symbols)
                # sell_running_mexc = False  # 重置标志 
            except Exception as e:
                logger.debug(f"An error occurred during selling: {e}")
                time.sleep(1)       
        else:           
            logger.debug("不满足卖出条件")
            time.sleep(0.3)


#cd /www/wwwroot/musk/test
#python3 1bijia.py
#这是2个交易所，一个上线很久了，一个后面上面，如果后面上的在旧的价格90%以下，狠狠抄底。
sell_running_gate = False  # 标志变量，指示 sell() 是否正在运行
sell_running_mexc = False
x = 10
symbol =  'AVERY'
symbols = f'{symbol}/USDT'
test_price = 0.01
beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)
print("程序启动时间:", datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


if __name__ == "__main__":
    sell_thread = threading.Thread(target=mexc_gate)
    sell_thread.start() 
    sell_thread = threading.Thread(target=mexc_gate_sell)
    sell_thread.start()  
