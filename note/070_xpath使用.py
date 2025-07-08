import urllib.request
import urllib.response
from lxml import etree

# 使用原始字符串（避免反斜杠转义）
tree = etree.parse(r'D:\python\note\070_xpath使用.html')

# 打印整个树的内容（可以用 .xpath() 方法查询，或将树转换为字符串）
print(etree.tostring(tree, pretty_print=True).decode())

#查找ul下面的li# 
li_list = tree.xpath('//body/ul/li')
print(li_list)

# 查找所有有id的属性的li标签
li_list = tree.xpath('//ul/li[@id]/text()')
print(li_list)

#找到id为l1的li标签 注意引号的问题
li_list = tree.xpath('//ul/li[@id="l1"]/text()')
print(li_list)

#查找到id为l1的li标签的class的属性值
# 
li = tree.xpath('//ul/li[@id="l1"]/@class')
print(li)

url = 'http://www.baidu.com/'
headers = {
'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
}

import urllib.request
request = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
# print(content)

from lxml import etree

tree = etree.HTML(content)
# result = tree.xpath('//input[@id=\'su\' and @value=\'百度一下\']')
result = tree.xpath('//input[@id="su"]/@Value')

print(result)

#//div[@class="tupian-list com-img-txt-list masonry"]//div/img/@src
#//div[@class="tupian-list com-img-txt-list masonry"]//div/img/@alt