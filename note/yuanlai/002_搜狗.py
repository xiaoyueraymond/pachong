import urllib.parse
import urllib.request
import json

# 适用的场景:数据果集的时候 需要绕过登陆 然后进入到某个页面
# #个人信息页面是utf-8 但是还报错了编码错误 因为并没有进入到个人信息页面 而是跳转到了登陆页面#那么登陆页面不是utf-8所以报错
#请求头的信息不够，所以登录不成功

# def creat_request(pageIndex):


#     # #请求定制
#     # request = urllib.request.Request(url=url,headers=headers)
#     # return request

import requests

def get_content():
    url = 'http://www.sogou.com/web'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    }
    param = {
        'query': 'deepseek'
    }
    try:
        response = requests.get(url=url, params=param, headers=headers, verify=False)
        content = response.text  # 获取页面内容
        return content

    except requests.exceptions.HTTPError as e:
        print(f'HTTP 错误: {e}')
    except requests.exceptions.RequestException as e:
        print(f'请求错误: {e}')

def down_load(content):
    file_name = r'D:\\python\\note\\yuanlai\\002_搜狗.html'
    with open(file_name, 'w', encoding='utf-8') as fp:
        fp.write(content)

if __name__ == '__main__':
    content = get_content()
    if content:  # 确保获取到内容再下载
        down_load(content)


