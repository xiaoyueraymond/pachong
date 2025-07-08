import ccxt
import time
import os
import logging
import smtplib
import ssl
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ================================================ 配置 ================================================

# 邮箱配置
SENDER_EMAIL = "13042063262@163.com"
SENDER_PASSWORD = "FGc8jrbvcNtGVW5J"  # 使用授权码
RECEIVER_EMAIL = "musk130@qq.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465

# 文件路径
file_path = "/www/wwwroot/musk/test/bn/bnjiaoyidui.txt"
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp.log')

# 日志时间格式化
timeFormat = "%Y/%m/%d %H:%M:%S"

# ================================================ 日志设置 ================================================

class BeijingTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        beijing_tz = timezone(timedelta(hours=8), name="Asia/Shanghai")
        return dt.astimezone(beijing_tz)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        return dt.strftime(timeFormat if datefmt is None else datefmt)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s'))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(BeijingTimeFormatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ================================================ 函数定义 ================================================

# 初始化币安USD-M期货交易所对象
exchange_bn = ccxt.binanceusdm({
    'enableRateLimit': True,
})

def timestamp_to_beijing_time(timestamp_ms):
    """将Unix时间戳（毫秒）转换为北京时间"""
    try:
        utc_time = datetime.utcfromtimestamp(int(timestamp_ms) / 1000)
        beijing_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        return beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "无法转换（时间戳无效）"

def send_email(subject, body):
    """发送电子邮件"""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        logger.info(f"[{subject}] 邮件发送成功")
    except Exception as e:
        logger.error(f"邮件发送失败: {e}")

def fetch_and_save_markets():
    """获取所有交易对并保存到文件"""
    try:
        markets = exchange_bn.fetch_markets()
        with open(file_path, "w") as file:
            for market in markets:
                file.write(market["symbol"] + "\n")
        logger.info(f"Markets saved to {file_path} at {time.ctime()}")
        return markets
    except Exception as e:
        logger.error(f"获取或保存交易对失败: {e}")
        return []

def load_previous_markets():
    """读取上一次保存的交易对"""
    if not os.path.exists(file_path):
        logger.warning(f"文件 {file_path} 不存在，可能是首次运行")
        return set()
    try:
        with open(file_path, "r") as file:
            return {line.strip() for line in file if line.strip()}
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        return set()

def check_new_markets():
    """比对新旧交易对，打印并发送邮件通知"""
    previous_markets = load_previous_markets()
    current_markets = fetch_and_save_markets()
    
    current_symbols = {market["symbol"] for market in current_markets}
    new_symbols = current_symbols - previous_markets
    
    if new_symbols:
        logger.info("发现新的交易对：")
        email_body = "发现新的交易对：\n\n"
        
        for market in current_markets:
            symbol = market["symbol"]
            if symbol in new_symbols:
                onboard_date = market["info"].get("onboardDate", "未知")
                created = market.get("created", "未知")
                
                onboard_beijing_time = timestamp_to_beijing_time(onboard_date) if onboard_date != "未知" else "无法转换"
                created_beijing_time = timestamp_to_beijing_time(created) if created != "未知" else "无法转换"
                
                # 控制台输出
                print(f"交易对: {symbol}")
                print(f"上线时间 (onboardDate): {onboard_date}")
                print(f"上线北京时间: {onboard_beijing_time}")
                print(f"创建时间 (created): {created}")
                print(f"创建北京时间: {created_beijing_time}")
                print("---")
                
                # 构造邮件内容
                email_body += f"交易对: {symbol}\n"
                email_body += f"上线时间 (onboardDate): {onboard_date}\n"
                email_body += f"上线北京时间: {onboard_beijing_time}\n"
                email_body += f"创建时间 (created): {created}\n"
                email_body += f"创建北京时间: {created_beijing_time}\n"
                email_body += "---\n"
        
        # 发送邮件
        send_email("币安新交易对通知", email_body)
    else:
        logger.info("没有发现新的交易对")

def main():
    """主循环，每60s检查一次"""
    while True:
        check_new_markets()
        logger.info("等待下一次检查（60s后）...")
        time.sleep(60)

#检查币安交易对，如果有新的交易对就发邮件通知。
#cd /www/wwwroot/musk/test/bn
#screen -S bnxinbishangxian python3 073bnjianyiduijiankong.py 

if __name__ == "__main__":
    main()