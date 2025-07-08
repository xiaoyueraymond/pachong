from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd

# 初始化浏览器并获取最新的标签页
browser = Chromium()
page = browser.latest_tab

# 过滤文件中的行
filtered_lines = []
filepath_so = r"C:\Users\musk8\Desktop\so.txt"  # 文件路径
with open(filepath_so, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line and (line.startswith('640') or line.startswith('804')):
            filtered_lines.append(line)
print(filtered_lines)

# 提取页面数据的函数
def getdata(url):
    page.get(url)
    non_empty_texts = []
    for t in page.eles('x://span[@data-v-27d3e544]'):
        if t.text.strip():
            non_empty_texts.append(t.text)
    
    non_empty_texts2 = []
    for t in page.eles('x://div[@data-v-27d3e544 and @class="ant-flex css-ffhn8y ant-flex-justify-center"]'):
        if t.text.strip():
            non_empty_texts2.append(t.text)

    # 整理数据
    str0 = non_empty_texts[0] + '\n' + non_empty_texts[4] + '\n' + non_empty_texts2[-4] + '\n' + non_empty_texts[8] + ' ' + non_empty_texts[9] + '\n' + non_empty_texts[10]
    str1 = non_empty_texts[1] + '\n' + non_empty_texts[5] + '\n' + non_empty_texts2[-3] + '\n' + non_empty_texts[11] + ' ' + non_empty_texts[12] + '\n' + non_empty_texts[13]
    str2 = non_empty_texts[2] + '\n' + non_empty_texts[6] + '\n' + non_empty_texts2[-2] + '\n' + non_empty_texts[14] + ' ' + non_empty_texts[15] + '\n' + non_empty_texts[16]
    str3 = non_empty_texts[3] + '\n' + non_empty_texts[7] + '\n' + non_empty_texts2[-1] + '\n' + non_empty_texts[17] + ' ' + non_empty_texts[18] + '\n' + non_empty_texts[19]

    # 返回整理后的数据
    return {
        'SO号': so_number,
        '起始地': [str0],
        '始发港': [str1],
        '目的港': [str2],
        '目的地': [str3]
    }

# 在 df 中追加每一行数据
def data_append(df, data):
    # 将新的一行数据添加到现有的 DataFrame 中
    new_row = pd.DataFrame(data)
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# 初始化一个空的 DataFrame
df = pd.DataFrame(columns=['SO号', '起始地', '始发港', '目的港', '目的地'])

# 遍历所有 URL 并将每一行数据追加到 df 中
for so_number in filtered_lines:
    new_url = "https://elines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number=%20" + so_number
    time.sleep(random.uniform(0, 3))  # 随机休眠模拟人工操作
    data = getdata(new_url)
    df = data_append(df, data)
    print(df)

# 最终将 df 保存到 Excel 文件
df.to_excel(r"D:\\python\\note\\071_driss实战.xlsx", index=False)
