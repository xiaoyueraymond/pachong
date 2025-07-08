import requests

url ='https://fanyi.baidu.com/sug'
response = requests.get(url=url)
print(type(response))
#设置响应的编码格式
response.encoding ='utf-8'
# 以字符串的形式来返回了网页的源码张
print(response.text)
#返回-个url地址
print(response.url)
# 返回的是二进制的数据# 
print(response.content)
# 返回响应的状态码# 
print(response.status_code)
# 返回的是响应头
print(response.headers)



data = {
    'kw':'eye'
}

headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}

#url 请求资源路径
#data参数
#kwargs 字典

response =requests.post(url=url,data=data,headers=headers)
content = response.text
print(content)

import json
obj = json.loads(content)
print(obj)