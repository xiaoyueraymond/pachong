




import urllib.parse
import urllib.request
import json

def creat_request(pageIndex):
    url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname1'
    
    data = {
        'cname': '北京',
        'pid': '',  # pid 是空的，所以用 None 代替
        'pageIndex': str(pageIndex),
        'pageSize': 10
    }

    data_encoded = urllib.parse.urlencode(data)
    # url = base_url + '&' + data_encoded  # 拼接完整 URL
    # print(url)  

    headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }
    # #post 请求的参数必须进行编码 #post请求要二次编码
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')

    #请求定制
    request = urllib.request.Request(url=url,data=data,headers=headers)
    return request

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

def down_load(pageIndex,content):
    file_name = f'kfc{pageIndex}.json'
    with open (file_name,'w',encoding='utf-8') as fp:
        print(content)
        fp.write(content)
 

if  __name__ == '__main__':
    for pageIndex in range(1,2):
        #定制请求，并返回
        request = creat_request(pageIndex)
        #获取数据
        content = get_content(request)
        #下载
        down_load(pageIndex,content)
        