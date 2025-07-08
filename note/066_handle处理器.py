import urllib.parse
import urllib.request
import json

# 适用的场景:数据果集的时候 需要绕过登陆 然后进入到某个页面
# #个人信息页面是utf-8 但是还报错了编码错误 因为并没有进入到个人信息页面 而是跳转到了登陆页面#那么登陆页面不是utf-8所以报错
#请求头的信息不够，所以登录不成功,定制更高级的请求头


url = 'http://www.baidu.com'
url = 'http://www.baidu.com/s?wd=ip'

headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

request = urllib.request.Request(url=url,headers=headers)

#handler build_opener open

#1.获取handler对象
handler = urllib.request.HTTPHandler()
#2.获取opener对象
opener = urllib.request.build_opener(handler)
#3.调用open方法
response = opener.open(request)
content = response.read().decode('utf-8')
print(content)
