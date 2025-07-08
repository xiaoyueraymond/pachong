import ccxt
from datetime import datetime
import pytz
import time

# 当前本地时间
current_time = datetime.now()
print("当前时间:", current_time.strftime('%Y-%m-%d %H:%M:%S'))

# 打印北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)
print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))

# 创建 Bitget 交易所实例
exchange = ccxt.bitget({
    'apiKey': 'bg_a42c11b91c4efb8e506b26eb5ddbf36f',
    'secret': '9ca1ddbc7bb7133926e5575ea6a6031084957274b90dbae4bb5f4899642f8776',
    'password': 'zhuan3000wan'
})


# # 获取订单簿信息并打印
# bitget_book = exchange.fetch_order_book(symbols)
# print(bitget_book)

# # 计算 fetch_balance 执行时间
# start_time = time.time()  # 记录开始请求时间
# balance = exchange.fetch_balance()
# end_time = time.time()    # 记录返回请求时间

# # 打印余额和请求时间信息
# print(balance)
# print("开始请求时间:", datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'))
# print("返回请求时间:", datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'))
# print(f"fetch_balance 请求耗时: {end_time - start_time:.6f} 秒")


beijing_tz = pytz.timezone('Asia/Shanghai')
symbolsm = 'BGB'
symbols = f'{symbolsm}/USDT'
buy_usdt = 1.1

def measure_latency(api_call_function, *args, **kwargs):
    start_time = time.time()
    response = api_call_function(*args, **kwargs)
    end_time = time.time()
    
    latency = end_time - start_time
    print(f"请求耗时（延迟）: {latency:.6f} 秒")
    return response

def buy():
    try:
        current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print("购买时间:", current_time)
        
        order = measure_latency(exchange.create_market_buy_order_with_cost, symbols, buy_usdt)
        print("Buy Order:", order)
    except Exception as e:
        print(f"An error occurred during buying: {e}")

def get_size():
    try:
        balance = measure_latency(exchange.fetch_balance)
        size = float(balance[symbolsm]['total'])
        print("Current size:", size)
        return size
    except Exception as e:
        print(f"An error occurred while fetching balance: {e}")
        return 0

def sell(size):
    try:
        if size > 0:
            current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print("出售时间:", current_time)
            
            order = measure_latency(exchange.create_market_sell_order, symbols, size)
            print("Sell Order:", order)
        else:
            print("Insufficient balance to sell.")
    except Exception as e:
        print(f"An error occurred during selling: {e}")



# while True:
#     beijing_time = datetime.now(beijing_tz)
#     print("当前北京时间（精确到毫秒）:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    
#     if (beijing_time.hour == 20 and 
#         beijing_time.minute == 13 and 
#         beijing_time.second == 00):
#         print("触发交易:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
#         buy()
#         time.sleep(0.3)
#         size = get_size()
#         sell(size)
#         break
    
#     time.sleep(0.1)  # 检查间隔

beijing_time = datetime.now(beijing_tz)
print("请求账户余额时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
balance2 = measure_latency(exchange.fetch_balance)
print(balance2)

# for i in range(0,10000):
#     current_time = datetime.now()
#     print("当前时间:", current_time.strftime('%Y-%m-%d %H:%M:%S'))
#     time.sleep(1)


# start_time = time.time()
# balance = exchange.fetch_balance()
# print(balance)
# end_time = time.time()
# hana_total = float(balance['HANA']['total']) - 1
# print(hana_total)
# elapsed_time = end_time - start_time
# print("请求耗时: {:.6f} 秒".format(elapsed_time))


# order = exchange.create_market_buy_order_with_cost(symbols,2)
# order2 = exchange.create_market_sell_order_with_cost(symbols,)
#print(order)
#获取所有交易对信息,查询是否存在ETH
# markets = exchange.load_markets()

# for market in markets:
#    if 'ETH' in market:
#     print(market)

# 定义交易对符号
# symbol = "COMAI/USDT"  # 对于 Binance，通常使用 USDT

# # # 获取 BTC/USDT 的市场价格信息,获取报价
# # btcticker = exchange.fetch_ticker(symbol)
# # print(btcticker)

# # #查看订单本
# order_book = exchange.fetch_order_book(symbols)
# print(order_book)
#print
# 打印结果1
# # #print(btcticker)



# symblo = 'uBTCUSD'
# size = 1
# bid = 33333
# ask = 33333

# order = exchange.create_limit_buy_order(symbol,size,bid)
# order = exchange.create_limit_sell_order(symbol,size,ask)

#查看订单本，获得最优的出价单 bid 是买入价 ask是卖出价
# def get_bid_ask():
#     start_time2 = time.time()
#     gateio_book = exchange.fetch_order_book(symbols)  
#     print(gateio_book) 
#     end_time2 = time.time()
#     #symbols_bid = gateio_book['bids'][0][0]
#     symbols_ask = gateio_book['asks'][0][0]
#     elapsed_time2 = end_time2 - start_time2
#     print("请求耗时: {:.6f} 秒".format(elapsed_time2))

# get_bid_ask()