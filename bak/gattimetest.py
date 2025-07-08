from datetime import datetime, timedelta
import pytz
import time
import socket
import ccxt

# 初始化API密钥和交易所实例
API_KEY = '9e54ae9b8ffd3f9a5565fa46b3aa2a60'
SECRET = 'a1398cf030451710aa463077b0022ba4c648239319fb2e9c3be0ac88edfd8500'

exchange = ccxt.gateio({
    'apiKey': API_KEY,
    'secret': SECRET
})

beijing_tz = pytz.timezone('Asia/Shanghai')
symbolsm = 'CYCON'
symbols = f'{symbolsm}/USDT'
buy_usdt = 4





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
        
        order = measure_latency(exchange.create_market_buy_order_with_cost, symbols,buy_usdt)
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
            
            order = measure_latency(exchange.create_market_sell_order, symbols,size)
            print("Sell Order:", order)
        else:
            print("Insufficient balance to sell.")
    except Exception as e:
        print(f"An error occurred during selling: {e}")



beijing_time = datetime.now(beijing_tz)
print("请求账户余额时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
balance2 = measure_latency(exchange.fetch_balance)




# current_time = datetime.now()
# print("当前时间:", current_time.strftime('%Y-%m-%d %H:%M:%S'))

# # 打印北京时间
# # 确保安装了 pytz 库：pip install pytz
# beijing_tz = pytz.timezone('Asia/Shanghai')
# beijing_time = datetime.now(beijing_tz)


# # while True:
# #     # 获取当前北京时间
# #     beijing_time = datetime.now(beijing_tz)
# #     print("当前北京时间（精确到毫秒）:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
# #     # 检查时间是否是 18:00:00.001 (注意：微秒部分用 1000 来表示)
# #     if (beijing_time.hour == 15 and 
# #         beijing_time.minute == 12 and 
# #         beijing_time.second == 50 ):
# #         #beijing_time.microsecond // 1000 == 1):
# #         print("当前北京时间（精确到毫秒）:", beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
# #         break
# #         # 暂停一段时间以避免重复执行（这里暂停更长的时间是因为条件非常精确）
# #         time.sleep(1)
    
# #     # 每 0.1 秒检查一次时间，以提高捕捉的精度
# #     time.sleep(0.1)

# import time
# import requests

# # Gate.io API URL 示例（请根据需要更改）
# url = 'https://api.gateio.ws/api/v4/spot/currency_pairs'

# # 记录开始时间
# start_time = time.time()

# # 发送请求
# response = requests.get(url)

# # 记录结束时间
# end_time = time.time()

# # 计算请求延迟（秒）
# elapsed_time = end_time - start_time

# print("请求耗时: {:.6f} 秒".format(elapsed_time))



# def get_ip_address(domain):
#     try:
#         # 获取域名对应的IP地址
#         ip_address = socket.gethostbyname(domain)
#         return ip_address
#     except socket.error as e:
#         print(f"Error resolving {domain}: {e}")
#         return None

# # 主函数
# if __name__ == "__main__":
#     domain = "api.gateio.ws"
#     ip_address = get_ip_address(domain)

#     if ip_address:
#         print(f"The IP address of {domain} is: {ip_address}")
#     else:
#         print(f"Could not resolve domain: {domain}")