import os
import sys
import logging
import re
import time
import random
from datetime import datetime
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from paddleocr import PaddleOCR
import smtplib
import ssl
import ccxt
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

# 获取当前 Python 脚本文件路径
current_script_path = os.path.abspath(sys.argv[0])
current_script_directory = os.path.dirname(current_script_path)

# 指定日志文件的相对路径
log_file_path = os.path.join(current_script_directory, 'temp.log')

# 创建自定义 Formatter 类以将时间转换为北京时间
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

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志记录级别为 DEBUG

# 创建文件处理器，指定日志文件路径和编码
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)  # 设置文件处理器级别为 WARNING
file_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 创建流处理器以将日志输出到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # 设置流处理器级别为 DEBUG
stream_formatter = BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

l = logger

exchange_gate = ccxt.gateio({

})

chrome_driver_path = r'/usr/local/bin/chromedriver'

# 配置 Chrome 无头浏览器选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--no-sandbox")  # 禁用沙盒
chrome_options.add_argument("--disable-dev-shm-usage")  # 解决 /dev/shm 不足的问题
chrome_options.add_argument("--remote-debugging-port=9222")  # 远程调试端口，避免 DevToolsActivePort 问题

# 创建 Chrome 服务对象
service = Service(chrome_driver_path)

def send_email(body):
    """发送电子邮件。
    
    参数:
        body (str): 邮件正文。
    """
    sender_email = "13042063262@163.com"
    sender_password = "FGc8jrbvcNtGVW5J"
    receiver_email = "musk130@qq.com"
    subject = "通知"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully")


# 启动 Chrome 浏览器并打开指定页面
def pachong_start():
    global wd
    # chrome_driver_path = r'D:\python\note\chromedriver-win64\chromedriver.exe'
    # chrome_driver_path = r'/usr/local/bin/chromedriver'
    # wd = webdriver.Chrome(service=Service(chrome_driver_path))
    wd = webdriver.Chrome(service=service, options=chrome_options)
    wd.get('https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN')
    time.sleep(10)
    print("开始下拉")
    wd.execute_script("window.scrollBy(0, 310);")
    while True:
    # 随机等待 0 到 5 秒.
        process_page()
        # 刷新页面
        wd.refresh()




# 定义函数 a 和 b
def a(content):
    beijing_tz = pytz.timezone('Asia/Shanghai')
    time2 = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    send_email(body=f"{time2}准备买进: {text}。准备买进合约")
    logger.debug(f"执行函数 a，内容: {content}")
    symbols = f'{text}/USDT'
    try: 
        # order = exchange_gate.create_market_buy_order_with_cost(symbols,11)
        # logger.debug("Buy Order:", order)  
        print("测试成功")
        sys.exit()
    except Exception as e:
        logger.debug(f"An error occurred during buying: {e}") 

def b(content):
    beijing_tz = pytz.timezone('Asia/Shanghai')
    time2 = datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    logger.debug(f"执行函数 b，内容: {content}")
    send_email(body=f"{time2}准备买进: {text}")
    symbols = f'{text}/USDT'
    try: 
        order = exchange_gate.create_market_buy_order_with_cost(symbols,11)
        logger.debug("Buy Order:", order)  
        sys.exit()
    except Exception as e:
        logger.debug(f"An error occurred during buying: {e}") 


# 定义一个函数来执行页面截图和 OCR 识别
def process_page():
    global text
    # 读取文件内容
    try:
        with open('str.txt', 'r', encoding='utf-8') as file:
            existing_content = file.read().splitlines()
    except FileNotFoundError:
        existing_content = []
    # 等待页面加载完成
    time.sleep(0.1)

    # 截图并保存，如果图片已经存在则覆盖
    screenshot_path = os.path.join(current_script_directory, 'screenshot.png')
    wd.save_screenshot(screenshot_path)

    # 使用 PaddleOCR 进行 OCR 识别
    ocr = PaddleOCR()
    result = ocr.ocr(screenshot_path)

    # 打开文件，以追加模式写入
    with open('str.txt', 'a', encoding='utf-8') as file:
        for line in result:
            for word in line:
                text_line = word[-1]
                text = text_line[0]
                l.debug(text)
                # 检查 text 是否已经存在于文件中
                if text not in existing_content:
                    # 检查 text 中是否包含关键字“添加种子标签”
                    if "添加种子标签" in text:
                        # 使用正则表达式提取括号中的内容
                        match = re.search(r'\((.*?)\)', text)
                        if match:
                            a_content = match.group(1)
                            print('a_content', a_content)
                            a(a_content)  # 执行函数 a

                    # 检查 text 中是否包含关键字“1-75倍 永续合约”
                    if "币安合约将上线" in text:
                        # 使用正则表达式提取“上线”到“USDT”之间的内容
                        match = re.search(r'上线(.*?)USDT', text)
                        if match:
                            b_content = match.group(1).strip()
                            print('b_content', b_content)
                            b(b_content)  # 执行函数 b
                    file.write(text + '\n')  # 将内容写入文件
    
    random_wait_time = random.uniform(0, 10)
    print(f"随机等待时间: {random_wait_time} 秒")
    time.sleep(random_wait_time)

# 初始处理页面


# 循环刷新页面并重复处理
# while True:
#     # 随机等待 0 到 5 秒
#     random_wait_time = random.uniform(0, 5)
#     logger.info(f"随机等待时间: {random_wait_time} 秒")
#     time.sleep(random_wait_time)

#     # 刷新页面
#     wd.refresh()

#     # 处理刷新后的页面
#     process_page()

#     # 保持页面打开
#     if input("按任意键继续刷新页面，按 'q' 退出: ").lower() == 'q':
#         break


# 关闭浏览器


if __name__ == "__main__":
    pachong_start()
