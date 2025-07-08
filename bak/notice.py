import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import hashlib
import pytz
import time
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# 邮箱配置
SENDER_EMAIL = "13042063262@163.com"
SENDER_PASSWORD = "FGc8jrbvcNtGVW5J"  # 使用授权码
RECEIVER_EMAIL = "musk130@qq.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465

# 网址列表
urls = [
    'https://www.htx.com/-/x/support/public/getDetails?id=44984691526265&x-b3-traceid=28a2ea623182221333e25a0eea395306',
    'https://www.mexc.com/help/announce/api/zh-TW/section/360000254192/articles?page=1&perPage=20',
    'https://www.gate.io/zh/announcements/newlisted',
    'https://www.bitget.cloud/support/_next/data/tAOF3akVypv2qXiQYrYjb/zh-CN/support/articles/12560603817639.json?contentId=12560603817639',
    'https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN'
    'https://www.okx.com/zh-hans/help/section/announcements-new-listings'
]

# 获取网页内容
def fetch_announcements(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # 处理编码问题
    return response.text

# 解析网页内容
def parse_announcements(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 根据网页结构修改选择器
    announcements = soup.find_all('div', class_='announcements-item')  
    announcements_text = []
    for announcement in announcements:
        title = announcement.find('h3').get_text(strip=True)
        date = announcement.find('span', class_='date').get_text(strip=True)
        announcements_text.append(f"{date}: {title}")
    return "\n".join(announcements_text)

# 发送电子邮件
def send_email(body):
    """发送电子邮件，body为邮件内容"""
    subject = "网站公告更新"
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print("Email sent successfully")

# 计算网页内容的哈希值
def get_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

# 监控单个网站
def monitor_site(url):
    previous_hash = None
    while True:
        try:
            # 获取当前北京时间
            beijing_tz = pytz.timezone('Asia/Shanghai')
            beijing_time = datetime.now(beijing_tz)
            
            html = fetch_announcements(url)
            announcements = parse_announcements(html)
            current_hash = get_hash(announcements)

            if previous_hash is None:
                previous_hash = current_hash  # 初始化
            elif current_hash != previous_hash:
                print(f"网站 {url} 有更新，发送邮件...")
                # 将更新的内容作为邮件正文
                email_content = f"网站 {url} 的公告更新:\n{announcements}"
                send_email(email_content)
                previous_hash = current_hash  # 更新哈希值

            # 显示北京时间
            print("北京时间:", beijing_time.strftime('%Y-%m-%d %H:%M:%S'))

        except Exception as e:
            print(f"访问 {url} 时出现错误: {e}")
        
        time.sleep(60)  # 每60秒检查一次

# 主函数，使用多线程监控多个网址
def main():
    threads = []
    send_email("test")
    for url in urls:
        thread = threading.Thread(target=monitor_site, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # 等待所有线程完成

if __name__ == '__main__':
    main()
