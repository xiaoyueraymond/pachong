import urllib.parse
import urllib.request
import json


url = 'http://www.baidu.com/s?wd=ip'


headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

#117.42.94.94 19714
request = urllib.request.Request(url=url,headers=headers)

# respon = urllib.request.urlopen(requset)
# content = respon.read().decode('utf-8')

#handler build_opener open

# proxies = {
#     '117.42.94.94':'19714'
# }
# #1.获取handler对象
# handler = urllib.request.ProxyHandler(proxies=proxies)
# #2.获取opener对象
# opener = urllib.request.build_opener(handler)
# #3.调用open方法
# response = opener.open(request)
# content = response.read().decode('utf-8')

# file_name = 'daili.html'
# with open (file_name,'w',encoding='utf-8') as fp:
#     print(content)
#     fp.write(content)

#代理池子，多个代理
#https://www.youtube.com/watch?v=VXdmBKfWdpM&list=PLmOn9nNkQxJH39Kc0suTsx7qxMGc_Cp1-&index=68
proxies_pool = [
{'117.42.94.94':'19714'},
{'117.42.94.91':'19711'}
]
import random
proxies = random.choice(proxies_pool)
request = urllib.request.Request( url = url ,headers=headers)
handle = urllib.request.ProxyHandler(proxies=proxies)
opener = urllib.request.build_opener(handle)
response = opener.open(request)
content = response.read().decode('utf-8')

file_name = 'daili.html'
with open (file_name,'w',encoding='utf-8') as fp:
    print(content)
    fp.write(content)