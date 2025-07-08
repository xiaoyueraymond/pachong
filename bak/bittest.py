import ccxt
from datetime import datetime
import pytz
import time

# 当前本地时间


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



beijing_tz = pytz.timezone('Asia/Shanghai')
symbolsm = 'AIX'
symbols = f'{symbolsm}/USDT'
buy_usdt = 1


EOS_LAST  = exchange.fetch_ticker(symbols)['last']
# print(f'{symbols}','最新报价',EOS_LAST)

# take_order = exchange.create_market_buy_order_with_cost(symbols,buy_usdt)
# print(take_order)

# order_id = order_details['info']['orderId']
# print("Order ID:", order_id)

markets = exchange.load_markets()

# 打印所有交易对
for symbol in markets:
    print(symbol)
    
#take_order['id']
# orderId =  '1233315294170488843'
# order_status = exchange.fetch_order_status(orderId,symbols)
# orderer = exchange.fetch_order( orderId,symbols)
# print(orderer)
# base_volume = orderer['info']['baseVolume']
# print(f"Base Volume: {base_volume}")

# print(order_status)