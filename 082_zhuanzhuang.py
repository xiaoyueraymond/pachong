from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
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
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

beijing_tz = pytz.timezone('Asia/Shanghai')
beijing_time = datetime.now(beijing_tz)

exchange_mexc = ccxt.mexc({
    'apiKey': 'mx0vglwxo4oW0wKiym',
    'secret': '9220372c34924f8c9f90b111ac5a527e',
    'proxies': proxies
})

exchange_bitget = ccxt.bitget({
    'apiKey': 'bg_085ae54090778b54aa3dee9ebb3cc614',
    'secret': '274e8ccd08c01bf502a308993668f59967018e5e3e817d90b44433d6d5ab7eaf',
    'password': 'zhuan3000wan',
    'proxies': proxies
})

exchange_gate = ccxt.gateio({
    'apiKey': '61f0e2f9e4affb50893e87f90a359080',
    'secret': 'd915d19823d825031234b08f54016bc2f6355e454ef6bd8aef26f98defbb3012',
    'proxies': proxies
})


exchange_htx = ccxt.htx({
    'apiKey': 'vftwcr5tnh-07f545cd-be748f53-f078c',
    'secret': '4e49bc29-fb067f15-10dc62e0-36146',
    'proxies': proxies
})

exchange_bingx = ccxt.bingx()
# markets = exchange_mexc.fetch_markets()

exchange_kucoin = ccxt.kucoin()


exchange_okex = ccxt.okx({
    'apiKey': '1153f253-bf96-4789-a2dc-379bffad2474',
    'secret': 'EA724612A773FA010562A596946E6C95',
    'password':'rfvRFV123!@#',
    'proxies': proxies
})

# 初始化浏览器并获取最新的标签页
browser = Chromium(9333)
page = browser.latest_tab



# //input[@autocomplete='off']
# 


from DrissionPage.common import Actions


def gate_mexc_bitget_htx(symbols):

    while True:
        try:
            order_book_bitget = exchange_bitget.fetch_order_book(symbols)
            order_book_htx = exchange_htx.fetch_order_book(symbols)
            order_book_mexc = exchange_mexc.fetch_order_book(symbols)
            order_book_gate = exchange_gate.fetch_order_book(symbols)
            time.sleep(0.1)
            if len(order_book_bitget['asks']) < 1 or len(order_book_gate['asks']) < 1 or len(order_book_mexc['asks']) < 1 :
                logger.debug(f'符号 {symbols} 的订单簿中没有足够的出价记录')
                continue
                time.sleep(0.1)

            price_bitget = order_book_bitget['asks'][0][0]
            price_gate = order_book_gate['asks'][0][0]
            price_mexc = order_book_mexc['asks'][0][0]
            price_htx = order_book_htx['asks'][0][0]
            amount_htx = order_book_htx['asks'][0][1]
            # print( order_book_htx['asks'])

            x, y = calculate_diff(price_bitget, price_gate, price_mexc)
            logger.debug(f'{symbols}(mexc: {price_mexc},bitget: {price_bitget}, gate: {price_gate},htx: {price_htx}) (差值1：{x} , 差值2:{y})')
            chazhi = 1.5
            time.sleep(0.1)

            if (order_book_htx['asks'][4][0]) < price_gate * chazhi and (order_book_htx['asks'][4][0]) < price_bitget * chazhi:
                logger.debug(f'{symbols}(mexc: {price_mexc},bitget: {price_bitget}, gate: {price_gate}),htx 启动买入程序:{price_htx}')
                try: 
                    order_cancel = exchange_htx.cancel_all_orders(symbols)
                    time.sleep(1)
                    fuckhtx(price_htx,amount_htx)
                    pass
                except Exception as e:
                    logger.debug(f"An error occurred during buying: {e}") 
                    time.sleep(1)

        except Exception as e:
            logger.debug(f"An error occurred while fetching ask price: {e}")
            time.sleep(0.1)  # 

def fuckhtx(price_htx,amount_htx):

    # page.ele("x://button[@class='type-item']").click()
    # time.sleep(2)
    # page.ele("x://button[@class='type-item cur']").click()
    # time.sleep(2)
    page.ele("x://input[@data-v-26c898f1]").clear()
    page.ele("x://input[@data-v-26c898f1]").input(price_htx)
    # time.sleep(4)
    # page.actions.key_down('Tab')
    # page.actions.key_up('Tab')
    # page.actions.key_down('Tab')
    # page.actions.key_up('Tab')
    page.ele("x:(//input[@data-v-26c898f1])[2]").clear()
    page.ele("x:(//input[@data-v-26c898f1])[2]").input(amount_htx)
    # page.ele("x:(//input[@data-v-26c898f1])[3]").input(5.4)
    page.ele("x://button[@class='submit-btn buy']").click()
    # //button[@class='submit-btn buy']
   
  
def calculate_diff(a, b, c):
    # 将三个参数放入列表中并排序
    sorted_lst = sorted([a, b, c])
    min_value = sorted_lst[0]
    
    # 计算差值
    diff1 = round(min_value / sorted_lst[1], 2)
    diff2 = round(min_value / sorted_lst[2], 2)

    return diff1, diff2
 


symbols = 'ELX/USDT'
mexc_usdt_trc20_address = 'THcXhrVRsJC2u723nqEryxL6f77Xvrf2WW'
mexc_usdt_bsc20_address = '0x3298feff55389a694be14212523efbd6da783843'

def htx_usdt_trc20(address):
    
    url = 'https://www.htx.com/zh-cn/finance/withdraw/usdt'
    page.get(url)
    # gate_mexc_bitget_htx(symbols)
    # //div[normalize-space(text())='TRC20']
    page.ele("x://div[normalize-space(text())='TRC20']").click()
    #//textarea[@class='input' and @placeholder='输入或者长按粘贴地址或ENS用户名']
    page.ele("x://textarea[@class='input' and @placeholder='输入或者长按粘贴地址或ENS用户名']").input(address)
    #//button[@class='all-in' and text()='全部']
    page.ele("x://button[@class='all-in' and text()='全部']").click()
    #//span[@class='ui-button-content']
    time.sleep(3)
    page.ele("x://span[@class='ui-button-content']").click()

def bitget_usdt_bsc20(address):
    url = 'https://www.bitget.cloud/zh-CN/asset/withdraw?coinId=129'
    page.get(url)
    #//div[@class='bit-select bit-select-large bit-select-round w-full Y4JEHnQfdkPgO14QteO2 css-1ig2lkn bit-select-single bit-select-show-arrow bit-select-show-search bit-select-show-search-and-img']
    page.ele("x://div[@class='bit-select bit-select-large bit-select-round w-full Y4JEHnQfdkPgO14QteO2 css-1ig2lkn bit-select-single bit-select-show-arrow bit-select-show-search bit-select-show-search-and-img']",timeout=30).click()
    #//span[text()='USDT']
    time.sleep(0.2)
    page.ele("x://span[text()='USDT']").click()
    time.sleep(0.2)
    #//input[@placeholder='提现地址 ']
    page.ele("x://input[@placeholder='提现地址 ']").input(address)
    time.sleep(0.2)
    #//span[text()='下一步']
    page.ele("x://span[text()='下一步']").click()
    time.sleep(0.2)
    #//span[@data-testid='WithdrawAmountInputAllBtn']
    page.ele("x://span[@data-testid='WithdrawAmountInputAllBtn']").click()
    time.sleep(0.2)
    #//button[@data-testid='WithdrawBtn']
    page.ele("x://button[@data-testid='WithdrawBtn']").click()

def bitget_bnb_bsc20(address):
    url = 'https://www.bitget.cloud/zh-CN/asset/withdraw?coinId=129'
    page.get(url)
    #//div[@class='bit-select bit-select-large bit-select-round w-full Y4JEHnQfdkPgO14QteO2 css-1ig2lkn bit-select-single bit-select-show-arrow bit-select-show-search bit-select-show-search-and-img']
    page.ele("x://div[@class='bit-select bit-select-large bit-select-round w-full Y4JEHnQfdkPgO14QteO2 css-1ig2lkn bit-select-single bit-select-show-arrow bit-select-show-search bit-select-show-search-and-img']").click()
    #//span[text()='USDT']
    time.sleep(0.2)
    page.ele("x://span[text()='BNB']").click()
    time.sleep(0.2)
    #//input[@placeholder='提现地址 ']
    page.ele("x://input[@placeholder='提现地址 ']").input(address)
    time.sleep(0.2)
    #//span[text()='下一步']
    page.ele("x://span[text()='下一步']").click()
    time.sleep(0.2)
    #//span[@data-testid='WithdrawAmountInputAllBtn']
    page.ele("x://span[@data-testid='WithdrawAmountInputAllBtn']").click()
    time.sleep(0.2)
    #//button[@data-testid='WithdrawBtn']
    page.ele("x://button[@data-testid='WithdrawBtn']").click()


def gate_usdt_bsc20(address):
    url = 'https://www.gate.io/zh/myaccount/withdraw/USDT'
    page.get(url)
    time.sleep(20)
    url = 'https://www.gate.io/zh/myaccount/withdraw/USDT'
    page.get(url)
    page.ele("x: //input[@placeholder='请输入 ']").input(address)
    page.ele("x://span[text()='选择网络']").click()
    time.sleep(2)
    page.ele("x://span[text()='BNB Smart Chain']").click()
    time.sleep(1)
    page.ele("x://span[@class='withdraw-amount-all']").click()
    time.sleep(1)
    page.ele("x://span[text()='提现']").click()

def mexc_usdt_bsc20(address):
    url = 'https://www.mexc.com/zh-TW/assets/withdraw/USDT'
    page.get(url)
    time.sleep(10)
    page.ele("x://div[@class='select-chain_option__2eHJu']").click()
    page.ele("x://p[text()='BNB Smart Chain(BEP20)']").click()
    time.sleep(0.2)
    page.ele("x: //input[@placeholder='請輸入或選擇提幣地址']").input(address)
    time.sleep(2)
    page.ele("x://a[text()='選擇全部']").click()
    time.sleep(2)
    page.ele("x://span[text()='提 交']").click()

def mexc_usdt_aptos(address):
    url = 'https://www.mexc.com/zh-TW/assets/withdraw/USDT'
    page.get(url)
    time.sleep(20)
    page.ele("x://div[@class='select-chain_option__2eHJu']").click()
    page.ele("x://p[text()='APTOS(APT)']").click()
    time.sleep(0.2)
    page.ele("x: //input[@placeholder='請輸入或選擇提幣地址']").input(address)
    time.sleep(2)
    page.ele("x://a[text()='選擇全部']").click()
    time.sleep(2)
    page.ele("x://span[text()='提 交']").click()


mexc_usdt_trc20_address = 'THcXhrVRsJC2u723nqEryxL6f77Xvrf2WW'
mexc_usdt_bsc20_address = '0x3298feff55389a694be14212523efbd6da783843'
bitget_usdt_bsc20_address = '0x698d301b1bc2f436d93ba30f8185594888d8b51f'
gate_usdt_bsc20_address = '0x0A37F6361BD9f8b38c6D679620f929D57086b62B'
bitget_usdt_aptos_address = '0x89dd10f72b6cd032e815464c6dfdb93db65ac9747a3f8d152ba4215ae4f47ceb'
okex_web3_bnb_bsc20_address = '0x3f02fa224d7848bd7e89f0474f93c89beb714722'
htx_usdt_bsc20_address = '0xb256c9dec34e9d6907b18a6c8f81167f6d905626'
binance_usdt_bsc20_address='0x4e8ea9eb41b97d8179bb052bd512456a088afac2'

if __name__ == "__main__":
    # htx_usdt_trc20(mexc_usdt_trc20_address)
    
    # gate_usdt_bsc20(mexc_usdt_bsc20_address)
    # mexc_usdt_bsc20(gate_usdt_bsc20_address )
    # mexc_usdt_bsc20(bitget_usdt_bsc20_address)
    # mexc_usdt_aptos(bitget_usdt_aptos_address)
    # mexc_usdt_bsc20(htx_usdt_bsc20_address)
    # bitget_bnb_bsc20(okex_web3_bnb_bsc20_address)
    # bitget_usdt_bsc20(mexc_usdt_bsc20_address)
    mexc_usdt_bsc20(binance_usdt_bsc20_address)
  