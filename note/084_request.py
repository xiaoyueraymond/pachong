import requests

url ='http://www.baidu.com'
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
    'wd':'北京'
}

headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}

#url 请求资源路径#params 参数
#kwargs 字典
proxy = {
    # 'http':'121.230.210.31:3256'
}

response =requests.get(url=url,params=data,headers=headers,proxies=proxy)
content = response.text
print(content)