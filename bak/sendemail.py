import smtplib
import ssl
import ccxt
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

# 初始化 API 密钥和交易所实例
API_KEY = '9e54ae9b8ffd3f9a5565fa46b3aa2a60'
SECRET = 'a1398cf030451710aa463077b0022ba4c648239319fb2e9c3be0ac88edfd8500'

exchange = ccxt.gateio({
    'apiKey': API_KEY,
    'secret': SECRET
})

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

def save_symbols_to_file(symbols):
    """将交易对列表追加保存到文件。

    参数:
        symbols (set): 当前交易对集合。
    """
    with open("symbols.txt", 'a') as f:  # 打开文件用于追加 ('a' 模式)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n--- {timestamp} ---\n")  # 添加时间戳以标识不同时间点的数据
        for symbol in sorted(symbols):
            f.write(f"{symbol}\n")
    
    print("Symbols appended to symbols.txt")

# 初始化已知的交易对集合
known_symbols = set(exchange.load_markets().keys())
print(known_symbols)

# 标记BTC价格邮件是否已发送
btc_email_sent = False
last_save_time = time.time()





# 主循环
while True:
    try:
        # 检查 BTC 价格
        btcticker = exchange.fetch_ticker('BTC/USDT')
        price_btc = float(btcticker['last'])
        print(f"BTC 最新报价: {price_btc}")
        beijing_tz = pytz.timezone('Asia/Shanghai')
        beijing_time = datetime.now(beijing_tz)
        print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))

        if price_btc > 69000 and not btc_email_sent:
            send_email(body=f"BTC 最新报价: {price_btc}。准备买进合约")
            btc_email_sent = True  # 设置标志为 True，以免再次发送

        # 检查新的交易对
        current_symbols = set(exchange.load_markets().keys())
        new_symbols = current_symbols - known_symbols

        if new_symbols:
            send_email(body=f"新增交易对: {', '.join(new_symbols)}")
            known_symbols.update(new_symbols)

        # 每小时将交易对追加存入文件
        current_time = time.time()
        if current_time - last_save_time >= 3600:  # 3600秒 = 1小时
            save_symbols_to_file(current_symbols)
            last_save_time = current_time

        time.sleep(1)  # 每秒检查一次

    except Exception as e:
        print(f"出现错误: {e}")
        time.sleep(5)  # 出现错误时等待更长时间再重试