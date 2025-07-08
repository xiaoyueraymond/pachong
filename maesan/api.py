import ccxt
from datetime import datetime, timedelta
import pytz
import time
import sys  # Import sys to enable exiting the program

# 初始化API密钥和交易所实例
API_KEY = '9e54ae9b8ffd3f9a5565fa46b3aa2a60'
SECRET = 'a1398cf030451710aa463077b0022ba4c648239319fb2e9c3be0ac88edfd8500'

exchange = ccxt.gateio({
    'apiKey': API_KEY,
    'secret': SECRET
})

def measure_latency(api_call_function, *args, **kwargs):
    start_time = time.time()
    response = api_call_function(*args, **kwargs)
    end_time = time.time()

    latency = end_time - start_time
    print(f"请求耗时（延迟）: {latency:.6f} 秒")
    return response

def buy():
    global ask_prices, buy_prices, max_price
    while True:
        try:
            balance = measure_latency(exchange.fetch_balance)
            usdt_available = next((float(info['available']) for info in balance['info'] if info['currency'] == 'USDT'), 0)
            print("USDT 可用余额:", usdt_available)
            if usdt_available < 5:
                break
            
            current_time = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print("购买时间:", current_time)
            
            # 创建限价买单
            order = exchange.create_limit_buy_order(symbols, buy_amount, oder_price)
            order_id = order['id']
            print(f"Order ID: {order_id}")
            
            # 检查订单
            order_info = exchange.fetch_order(order_id, symbols)
            order_status = order_info['status']
            print(f"Order Status: {order_status}")

            if order_status == 'open':
                exchange.cancel_order(order_id, symbols)
                sys.exit("未完成最低价买入操作，程序终止。")
            
            if order_status == 'closed':
                buy_prices = float(order_info.get('average', 0))  # 确保获取到 avg_deal_price
                max_price = buy_prices
            
            print("Buy Order:", order)
            break
        except Exception as e:
            print(f"An error occurred during buying: {e}")
            time.sleep(0.1)

# 获取最新的卖出价格
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

def get_size():
    try:
        balance = measure_latency(exchange.fetch_balance)
        size = float(balance[symbolsm]['total'])
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

                order = measure_latency(exchange.create_market_sell_order, symbols, size)
                print("Sell Order:", order)

                sys.exit("卖出操作已完成，程序终止。")  # Exit the program after selling

            time.sleep(0.1)  # 避免过于频繁请求
    except Exception as e:
        print(f"An error occurred during selling: {e}")

def wait_until_target_time(target_time):
    while True:
        now = datetime.now(beijing_tz)
        current_time_str = now.strftime('%H:%M:%S')
        target_time_str = target_time.strftime('%H:%M:%S') 
        # 检查当前时间是否等于或超过目标时间，同时检查毫秒部分
        if current_time_str == target_time_str and now.microsecond // 1000 >= target_time.microsecond // 1000:
            break
        time.sleep(0.1)  # 减少CPU使用，微调等待精度

def execute_trading_strategy(p, q):
    global max_price, ask_prices, oder_price, buy_amount
    print("Executing trading strategy...")

    # 在等待时间前先获取一次报价
    ask_prices = ask_price()
    oder_price = ask_prices * 1
    buy_amount = int(usdt_available2 / oder_price)

    while True:
        try:
            balance = measure_latency(exchange.fetch_balance)
            usdt_available = next((float(info['available']) for info in balance['info'] if info['currency'] == 'USDT'), 0)
            print("USDT 可用余额:", usdt_available)
            if usdt_available > 5:
                buy()
            else:
                time.sleep(0.3)
                size = get_size()
                sell(size, p, q)
        except Exception as e:
            print(f"An unexpected error occurred in trading strategy: {e}")
        time.sleep(0.1)


# 设置时区和符号
beijing_tz = pytz.timezone('Asia/Shanghai')
symbolsm = 'BABYNEIRO'
symbols = f'{symbolsm}/USDT'

# 获取初始资金可用余额
balance = exchange.fetch_balance()
usdt_available2 = next((float(info['available']) for info in balance['info'] if info['currency'] == 'USDT'), 0)
print("USDT 可用余额:", usdt_available2)

# 输出程序启动信息
print("程序启动时间:", datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])