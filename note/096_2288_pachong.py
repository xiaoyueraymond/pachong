import urllib.request
from lxml import etree

# Define the URL and headers
url = 'https://elonmusk35511.lofter.com/post/8ac3b930_2bebb8c9d'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}

# Create request and fetch response
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

# Parse the HTML content using lxml
tree = etree.HTML(content)

# Use XPath to extract the <p> element with the specific id
p_content = tree.xpath('//p[@id="p_u5xmbu93bkx"]/text()')
# print(content)
# Print the extracted content


from bs4 import BeautifulSoup

# The provided HTML content
text = content


import re
# 使用正则表达式提取 <p id="p_u5xmbu93bkx"> 到 </p> 之间的内容
match = re.search(r'(ipmitool\.exe.*?0x01)', text)

if match:
    content = match.group(1)
    # 替换 &nbsp; 为普通空格
    content2 = content.replace('&nbsp;', ' ')
    # print(content2)
else:
    print("没有找到匹配的内容")

import subprocess
def load_default():
   
    # command = f'ipmitool -I lanplus -H {host_ip} -U Administrator -P Admin@9000 raw 0x30 0x93 0xdb 0x07 0x00 0x07 0x00 0xaa'
    #降低内存认证告警的级别
    command1 = content2
    
    # print(command2)
    # print(command3)
    # print(command4)
  # 使用 subprocess.run 执行命令
    result1 = subprocess.run(command1, shell=True, text=True, capture_output=True)
    # result2 = subprocess.run(command2, shell=True, text=True, capture_output=True)
    # result3 = subprocess.run(command3, shell=True, text=True, capture_output=True)
    # result4 = subprocess.run(command4, shell=True, text=True, capture_output=True)

    print("命令输出:", result1.stdout)
    print("命令错误输出:", result1.stderr) 
    # print("命令输出:", result2.stdout)
    # print("命令错误输出:", result2.stderr) 
    # print("命令输出:", result3.stdout)
    # print("命令错误输出:", result3.stderr) 
    # print("命令输出:", result4.stdout)
    # print("命令错误输出:", result4.stderr) 


load_default()






