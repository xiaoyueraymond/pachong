import urllib.parse
import urllib.request
import json

# 适用的场景:数据果集的时候 需要绕过登陆 然后进入到某个页面
# #个人信息页面是utf-8 但是还报错了编码错误 因为并没有进入到个人信息页面 而是跳转到了登陆页面#那么登陆页面不是utf-8所以报错
#请求头的信息不够，所以登录不成功

def creat_request(page):
    
    headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    }
    if page == 1:
        url = 'https://sc.chinaz.com/tupian/qinglvtupian.html'
        #请求定制
        request = urllib.request.Request(url=url,headers=headers)
    else: 
        url = f'https://sc.chinaz.com/tupian/qinglvtupian_{page}.html'
        request = urllib.request.Request(url=url,headers=headers)
    
    return request

#https://sc.chinaz.com/tupian/qinglvtupian_3.html

import urllib.error

def  get_content(request):
    try:
        response = urllib.request.urlopen(request)
        content =response.read().decode('utf-8')
        return content
    except urllib.error.HTTPError as e:
        print(f'{e}')
    except urllib.error.URLError as e:
        print(f'{e}')

# def down_load(page,content):
#     file_name = f'weibo{page}.json'
#     with open (file_name,'w',encoding='utf-8') as fp:
#         print(content)
#         fp.write(content)



def down_load(content):
    tree = etree.HTML(content)
    # result = tree.xpath('//input[@id=\'su\' and @value=\'百度一下\']')
    div_list = tree.xpath('//div')
    img_list = tree.xpath('//img')
    print(f"Found {len(div_list)} div tags")
    print(f"Found {len(img_list)} img tags")
    src_list = tree.xpath('//img/@src')
    name_list = tree.xpath('//img/@alt')
    print(len(name_list),len(src_list))
    for i in name_list:
        print(i)
    for j in src_list:
        print(j)

#//div[@class="tupian-list com-img-txt-list masonry"]//div/img/@src
#//div[@class="tupian-list com-img-txt-list masonry"]//div/img/@alt

if  __name__ == '__main__':
    for page in range(1,3):
        #定制请求，并返回
        request = creat_request(page)
        #获取数据
        content = get_content(request)
        #下载
        down_load(content)
