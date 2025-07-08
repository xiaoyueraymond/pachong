import ccxt
from datetime import datetime
import pytz
import time
import sys  # Import sys to enable exiting the program

# 当前本地时间

#程序每次都在第一秒内买入，买入都是在顶峰最高价
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


def measure_latency(api_call_function, *args, **kwargs):
    start_time = time.time()
    response = api_call_function(*args, **kwargs)
    end_time = time.time()

    latency = end_time - start_time
    print(f"请求耗时（延迟）: {latency:.6f} 秒")
    return response

def buy():
    global ask_prices, buy_prices, max_price,order
    while True:
        try:
            balance = measure_latency(exchange.fetch_balance)
            usdt_available = next((float(info['available']) for info in balance['info'] if info['coin'] == 'USDT'), 0)
            print("USDT 可用余额:", usdt_available)
            if usdt_available < 3.2:
                break
            
            current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print("购买时间:", current_time)
            
            # 创建限价买单
            order = exchange.create_limit_buy_order(symbols, buy_amount, oder_price)
            print("Buy Order:", order)
            order_id = order['id']
            print(f"Order ID: {order_id}")
            
            # 检查订单
            order_info = exchange.fetch_order(order_id, symbols)
            order_status = order_info['info']['status']
            print(f"Order Status: {order_status}")
            print(order_info)
            #暂时不知道订单完成的状态,太快了，系统反应不过来
            if order_status == 'open':
                exchange.cancel_order(order_id, symbols)
                sys.exit("未完成最低价买入操作，程序终止。")    
            if order_status == 'live':
                buy_prices = float(order_info['info']['price'])  # 确保获取到 avg_deal_price
                max_price = buy_prices
            break
        except Exception as e:
            print(f"An error occurred during buying: {e}")
            time.sleep(0.1)

# 其余代码保持不变

# 其他函数保持不变

def get_size():
    try:
        # balance = measure_latency(exchange.fetch_balance)
        # size = float(balance[symbolsm]['total'])
        order_id = order['info']['orderId']
        orderer = exchange.fetch_order(order_id,symbols)
        size = float(orderer['amount'])
        print("Current size:", size)
        return size
    except Exception as e:
        print(f"An error occurred while fetching balance: {e}")
        return 0

def sell(size, p, q):
    global max_price
    try:
        while True:
            current_price = ask_price()
            #'priceAvg': '0.0001769000000000 买入价格是这个但是无法瞬间获取到
            print("当前买入价格是:",buy_prices)

            # 更新最大价格
            if current_price > max_price:
                max_price = current_price
                print(f"更新最大价格: {max_price}")

            # 检查卖出条件
            max_drop_condition = current_price <= max_price * 0.95
            price_drop_condition = current_price <= buy_prices * (1 - p / 100)
            max_price_increase_condition = max_price >= buy_prices * (1 + q / 100)

            if max_drop_condition or price_drop_condition or max_price_increase_condition:
                trigger_reason = ""
                if max_drop_condition:
                    trigger_reason = "当前价格下降超过最大价格的5%"
                elif price_drop_condition:
                    trigger_reason = f"当前价格低于最初买入价格的 {p}%"
                elif max_price_increase_condition:
                    trigger_reason = f"最大价格曾经高于买入价的 {q}%"
                
                print(f"当前价格 {current_price} 满足卖出条件，准备卖出。触发条件：{trigger_reason}")
                current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print("出售时间:", current_time)
                sell_order = exchange.create_limit_sell_order(symbols,size,current_price)
                # sell_order = measure_latency(exchange.create_market_sell_order, symbols, size)
                print("Sell Order:", sell_order)

                sys.exit("卖出操作已完成，程序终止。")  # Exit the program after selling

            time.sleep(0.1)  # 避免过于频繁请求
    except Exception as e:
        print(f"An error occurred during selling: {e}")

def ask_price():
    while True:
        try:
            order_book = exchange.fetch_order_book(symbols)
            ask_prices = order_book['asks']
            if len(ask_prices) > 0:
                ask_price = ask_prices[0][0]  # 获取最优买入价
                print(f'{symbols}', '最新报价', ask_price)
                return ask_price
            else:
                raise ValueError("No ask prices available")
        except Exception as e:
            print(f"An error occurred while fetching ask price: {e}")
            time.sleep(0.1)  # 等待然后重试



# wait_until_target_time(target_time)

def execute_trading_strategy(p, q):
    global max_price
    print("Executing trading strategy...")
    while True:
        try:
            balance = measure_latency(exchange.fetch_balance)
            usdt_available = next((float(info['available']) for info in balance['info'] if info['coin'] == 'USDT'), 0)
            print("USDT 可用余额:", usdt_available)
            if usdt_available > 3.2:
                buy()
            else:
                time.sleep(0.3)
                size = get_size()
                sell(size, p, q)
        except Exception as e:
            print(f"An unexpected error occurred in trading strategy: {e}")
        time.sleep(0.1)


def wait_until_target_time(target_time):
    while True:
        now = datetime.now(beijing_tz)
        current_time_str = now.strftime('%H:%M:%S')
        target_time_str = target_time.strftime('%H:%M:%S') 
        # 检查当前时间是否等于或超过目标时间，同时检查毫秒部分
        if current_time_str == target_time_str and now.microsecond // 1000 >= target_time.microsecond // 1000:
            break
        time.sleep(0.1)  # 减少CPU使用，微调等待精度

# 设置目标时间为今天的 18:01:01.01


beijing_tz = pytz.timezone('Asia/Shanghai')
symbolsm = 'X'
symbols = f'{symbolsm}/USDT'
balance = exchange.fetch_balance()
usdt_available2 = next((float(info['available']) for info in balance['info'] if info['coin'] == 'USDT'), 0)
print("USDT 可用余额:", usdt_available2)
# order_book2 = exchange.fetch_order_book(symbols)
# print(order_book2)
ask_prices = ask_price()
# 下单的时候多加50%，以防止买不到
oder_price = ask_prices * 1
# oder_price = 1
print(f'{symbols}', "准备买入价格:", oder_price)
buy_amount = int(usdt_available2 / oder_price)
print(f'{symbols}', "准备买入数量:", buy_amount)
print("程序启动时间:", datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


# target_time = datetime.now(beijing_tz).replace(hour=21, minute=59, second=56, microsecond=10000)
# 设置目标时间为今天的某个时间，不等待直接开始策略
# wait_until_target_time(target_time)
# 执行交易策略，指定 p 和 q 参数
execute_trading_strategy(p=5, q=6)

