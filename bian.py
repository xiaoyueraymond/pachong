import asyncio
import json
import os
import smtplib
import ssl
import threading
import time
import pytz
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote, urlencode

import requests
from bs4 import BeautifulSoup


proxies = {}


url = "https://www.binance.com/zh-CN/support/announcement/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81%E5%8F%8A%E4%BA%A4%E6%98%93%E5%AF%B9%E4%B8%8A%E6%96%B0?c=48&navId=48&hl=zh-CN"
res = requests.get(url, proxies=proxies)

if res.status_code != 200:
    print(

        res.status_code
    )

html = BeautifulSoup(res.text, "html.parser")
# data = html.find(id="__APP_DATA").get_text()
print(html)