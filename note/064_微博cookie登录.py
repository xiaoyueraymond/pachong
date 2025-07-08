




import urllib.parse
import urllib.request
import json

# 适用的场景:数据果集的时候 需要绕过登陆 然后进入到某个页面
# #个人信息页面是utf-8 但是还报错了编码错误 因为并没有进入到个人信息页面 而是跳转到了登陆页面#那么登陆页面不是utf-8所以报错
#请求头的信息不够，所以登录不成功

def creat_request(pageIndex):
    url = 'https://weibo.cn/7921414294/info'
    

    headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    'cookie' : '_T_WM=62050067419; SCF=An2iNCnZmUqZmU0XAYOy0_2zQECcY0VhklvRUjPmWXvCt3TCbOzQc6-8UEE-GikYTN7xNsGTEkbzXm6qyAGW_BM.; SUB=_2A25KoQzoDeRhGeFH6VMV8SrOwjiIHXVp3wAgrDV6PUJbktAbLWXtkW1Ne6g2_xlwmZtfkOECw1gIrL0Nl2YlIifY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFq0maGsPH5SZ3ZJ3ah.5X75NHD95QN1KzpSh2Xeo.XWs4Dqcj_i--fiKn4i-8si--Xi-zRiKLWi--fi-zNi-zXi--RiKysi-zEi--NiKn4i-z4; SSOLoginState=1738898616; ALF=1741490616; MLOGIN=1; _TTT_USER_CONFIG_H5=%7B%22ShowMblogPic%22%3A1%2C%22ShowUserInfo%22%3A1%2C%22MBlogPageSize%22%3A10%2C%22ShowPortrait%22%3A1%2C%22CssType%22%3A0%2C%22Lang%22%3A1%7D; _T_H5TOWAP=1; M_WEIBOCN_PARAMS=lfid%3D2304137921414294_-_WEIBO_SECOND_PROFILE_WEIBO%26luicode%3D20000174',

    }


    #请求定制
    request = urllib.request.Request(url=url,headers=headers)
    return request

import urllib.error

def  get_content(request):
    try:
        response = urllib.request.urlopen(request)
        print('123')
        print(response)
        content =response.read().decode('utf-8')
        return content
    except urllib.error.HTTPError as e:
        print(f'{e}')
    except urllib.error.URLError as e:
        print(f'{e}')

def down_load(pageIndex,content):
    file_name = f'weibo{pageIndex}.json'
    with open (file_name,'w',encoding='utf-8') as fp:
        print(content)
        fp.write(content)
 

if  __name__ == '__main__':
    pageIndex = 1
    #定制请求，并返回
    request = creat_request(pageIndex)
    #获取数据
    content = get_content(request)
    #下载
    down_load(pageIndex,content)