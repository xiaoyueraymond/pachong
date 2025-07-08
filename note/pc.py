import urllib
import urllib.parse
import urllib.request

# url = "http://www.baidu.com"

# #'模拟浏览器发送请求，返回的类型是HTTPRseponse'
# response = urllib.request.urlopen(url)

# #read方法 返回字节形式的二进制数据
# #解码decode
# content =response.read().decode('utf-8')

# #一个类型6个方法

# #读10个字节
# content = response.read()
#读一行
# content = response.readline

# #读10行
# content = response.readlines()

# print(content)
#获取状态码
# print(response.getcode())
# #获取链接
# print(response.geturl())
# #获取状态信息
# print(response.getheaders())

#55 下载东西


# url_img = 'https://img1.baidu.com/it/u=1044474657,3890888056&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=1082'
# # urllib.request.urlretrieve(url = url_img,filename = 'liuyifei.jpg')

# #下载视频

# url_video = 'https://vdept3.bdstatic.com/mda-qj9ha5n41yaxuyif/360p/h264/1728562387257505910/mda-qj9ha5n41yaxuyif.mp4?v_from_s=hkapp-haokan-hbf&auth_key=1738838117-0-0-8ba5c7d3f45a6043442b834cf6e4c184&bcevod_channel=searchbox_feed&pd=1&cr=0&cd=0&pt=3&logid=2116982607&vid=11450434447018315492&klogid=2116982607&abtest='
# # urllib.request.urlretrieve(url = url_video,filename = 'liuyifei.mp4')



# url_zjl = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd='

headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}

#伪装一个请求对象
# request = urllib.request.Request(url=url,headers=headers)
# #'模拟浏览器发送请求，返回的类型是HTTPRseponse'
# response = urllib.request.urlopen(requset)

# #汉字转换为unicode编码



# #read方法 返回字节形式的二进制数据
# #解码decode
# content =response.read().decode('utf-8')
# print(content)

# name = urllib.parse.quote('周杰伦')
# name = url_zjl + name
# print (name)

#多参数拼接

# data = {
#     'wd':'周杰伦',
#         'sex':'',
#             'location':'美国'
# }

# search_data = urllib.parse.urlencode(data)

# base_url = 'https://www.baidu.com/s?'
# url = base_url + search_data
# #伪装一个带有头的请求
# request = urllib.request.Request(url=url,headers=headers)
# response = urllib.request.urlopen(request)
# content = response.read().decode('utf-8')
# print (url)
# print(content)

#059--------------------------------------------------------------------------------------------------------------------
baidufanyi_url ='https://fanyi.baidu.com/sug'

data = {
    'kw':'spider'
}

#post 请求的参数必须进行编码 #post请求要二次编码

data = urllib.parse.urlencode(data)
data = data.encode('utf-8')

request = urllib.request.Request(url=baidufanyi_url,data=data,headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
print(data)
print(response)
print(content)

import json

obj =json.loads(content)
print(obj)

#60--------------------------------------------------------------------------------
# url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'

# heards = {
#     'cookie':
# }
# data = {
#     'from': 'en',
#     'to': 'zh',
#     'query': 'love',  # 你要翻译的单词
#     'transtype': 'realtime',
#     'simple_means_flag': '3',
#     'sign': '198772.518981',  # 需要根据实际情况计算签名
#     'token': '5483bfa652979b41f9c90d91f3de875d',  # token也是需要从API文档或实际请求中获得的
#     'domain': 'common'
# }

# # #post 请求的参数必须进行编码 #post请求要二次编码
# data = urllib.parse.urlencode(data)
# data = data.encode('utf-8')

# #请求定制
# request = urllib.request.Request(url=url,data=data,headers=headers)
# #模拟浏览器请求
# response = urllib.request.urlopen(request)
# content = response.read().decode('utf-8')
#61-------------------------------------------------------------------------------------------------------------
#https://www.youtube.com/watch?v=nZ9CXEnpVl0&list=PLmOn9nNkQxJH39Kc0suTsx7qxMGc_Cp1-&index=61
#get 请求
# url ='https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'


# headers = {
# 'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
# }

# #请求对象的定制
# requsest = urllib.request.Request(url=url,headers=headers)

# #模拟网页请求数据，获取响应数据
# response = urllib.request.urlopen(requsest)
# content =response.read().decode('utf-8')
# print(content)
# #open编码默认是GBK的的编码
# fp = open ('douban.json','w',encoding='utf-8')
# fp.write(content)
# fp.close()
#62-----------------------------------------------------------------------------------------------------------------------------------------
#1.构造请求
#2.获取响应数据
#3.下载

# import urllib.parse
# import urllib.request

# def creat_request(page):
#     base_url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&'
#     data = {
#         'start' : (page-1)*20,
#         'limit' : 20
#     }

#     data = urllib.parse.urlencode(data)
#     url = base_url + data
#     print(url)

#     headers = {
#     'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
#     }

#     #请求对象的定制
#     requsest = urllib.request.Request(url=url,headers=headers)
#     return requsest

# def  get_content(request):
#     response = urllib.request.urlopen(request)
#     content =response.read().decode('utf-8')
#     return content

# def down_load(page,content):
#     fp = open ('douban' + str(page) + '.json','w',encoding='utf-8')
#     print(content)
#     fp.write(content)
#     fp.close()  

# if  __name__ == '__main__':
#     for page in range(1,2):
#         #定制请求，并返回
#         request = creat_request(page)
#         #获取数据
#         content = get_content(request)
#         #下载
#         down_load(page,content)