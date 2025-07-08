import threading
import time

# 全局变量a
a = 0

# 定义卖出函数
def sell():
    global a
    while a > 8:
        print("卖出")
        time.sleep(1)  # 控制卖出函数的执行频率

# 定义买入函数
def buy():
    global a
    if a > 2:
        # 启动卖出线程
        sell_thread = threading.Thread(target=sell)
        sell_thread.daemon = True  # 设置为守护线程，主程序退出时，子线程也会退出
        sell_thread.start()
        print('买入函数还在运行')

# 定义股票价格更新函数
def update_price():
    global a
    while True:
        # 模拟股票价格的变化
        a = (a + 1) % 11  # 保证a的值在0到10之间循环变化
        print(f"当前股票价格: {a}")
        time.sleep(1)  # 每秒更新一次股票价格

# 启动股票价格更新线程
price_thread = threading.Thread(target=update_price)
price_thread.daemon = True
price_thread.start()

# 主循环，执行买入逻辑
while True:
    buy()
    time.sleep(1)  # 每秒检查一次买入条件

#这是用来0.6买入0.9卖出的程序，
