#!/usr/bin/env python
# -*- coding:utf-8 -*-

#https://www.bilibili.com/video/BV1Yh411o7Sz?spm_id_from=333.788.player.switch&vd_source=2e750606d6f336aa5b5186e2fecafc53&p=5
import requests

# step 1: 指定url
url = 'https://www.sogou.com/'

# step 2: 发起请求
response = requests.get(url=url)

# step 3: 获取响应数据
page_text = response.text
print(page_text)

# step 4: 持久化存储

with open(r'D:\python\note\yuanlai\001_第一血.html', 'w', encoding='utf-8') as fp:
    fp.write(page_text)



