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
        if line and len(line) == 10 and line.startswith('2'):
            filtered_lines.append(line)

print(filtered_lines)
filtered_lines = list(set(filtered_lines))


def changdu():
    for i in range(2, 30):  # 从tr[3]开始
        try:
            # 假设这是检查元素是否存在，timeout=0.1表示0.1秒超时
            if page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[1]', timeout=0.1):
                continue  # 如果元素存在，则继续下一次循环
            else:
                return i
        except Exception:  # 如果超时或找不到元素，会抛出异常
            return i  # 如果元素不存在，则返回当前的i值
        
def getdata(so_number):     
    url = 'https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx'
    page.get(url)
    page.ele('x://*[@id="SEARCH_NUMBER"]').input(so_number)
    page.ele('x://*[@id="container_btn"]').click()
    time.sleep(3)
    page.ele('x://tbody/tr/td[@id="tab12"]').click()
    a = page.ele('x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[2]//td[1]').text
    print(a)
    Event= []
    Facility = []
    Location = []
    Mode = []
    Time = []
    Remarks = []
    so_number_list = [so_number]

    changdu_value = changdu()
    for i in range(2,changdu_value):
        Event.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[1]', timeout=0.1).text)
        Facility.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[2]', timeout=0.1).text)
        Location.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[3]', timeout=0.1).text)
        Mode.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[4]', timeout=0.1).text)
        Time.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[5]', timeout=0.1).text)
        Remarks.append(page.ele(f'x:(//td[@class="subTabOtherBorder"]//table[@id="eventListTable"]//tbody)[2]//tr[{i}]//td[6]', timeout=0.1).text)
    # print(changdu_value)
    # print(len(Remarks))
    a = {
                'so': so_number_list + ['-'] *(changdu_value - 3),
                'Event': Event,
                'Facility':Facility,
                'Location': Location,
                'Mode.': Mode,
                'Time': Time,
                'Remarks': Remarks,
                    
            }

    data = pd.DataFrame(a)
    print(data)
    return data

# 使用列表来积累数据
data_list = []

# 遍历所有 SO 并将数据存入 data_list
for so_number in filtered_lines:
    time.sleep(random.uniform(0, 3))  # 随机休眠模拟人工操作
    data = getdata(so_number)
    # 假设 getdata 返回的是一个 DataFrame 或者是能够转换为 DataFrame 的数据
    empty_row = pd.DataFrame([[None] * len(data.columns)], columns=data.columns)
    data_list.append(data)
    data_list.append(empty_row)  # 插入一个空行

# 将列表中的所有 DataFrame 合并为一个 DataFrame
result = pd.concat(data_list, ignore_index=True)

# 将合并后的 DataFrame 保存到 Excel 文件
result.to_excel(r"D:\\python\\note\\076_driss_oocl.xlsx", index=False)

print("Data saved to Excel successfully.")
