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
        if line and (len(line) == 12):
            filtered_lines.append(line)

print(filtered_lines)

 
def changdu():
    for i in range(3, 12):  # 从tr[3]开始
        try:
            # 假设这是检查元素是否存在，timeout=0.1表示0.1秒超时
            if page.ele(f'x:/html/body/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[1]', timeout=0.1):
                continue  # 如果元素存在，则继续下一次循环
            else:
                return i
        except Exception:  # 如果超时或找不到元素，会抛出异常
            return i  # 如果元素不存在，则返回当前的i值
        
        
# 获取标签属性值
def getdata(so_number):
    url = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do?TYPE=BL&BL=149408793422'
    page.get(url)
    page.ele('x://*[@id="NO"]').input(so_number)
    page.ele('x://*[@id="nav-quick"]/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div[2]/input').click()
    time.sleep(1)
    non_empty_texts = []
    non_empty_texts = []
    Date2 = []
    Container_Moves = []
    Location = []
    Vessel_Voyage = []
    try:
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[2]/tbody/tr[6]/td[2]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[1]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[2]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[3]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[4]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[5]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[6]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[7]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[8]').text)
        non_empty_texts.append(page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[9]').text)
    except Exception as e:
        print(f"Error fetching data for SO: {so_number}. Error: {e}")
        return None  # In case of error, return None or handle differently

    try:
        page.ele('x:/html/body/div[7]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[1]/a').click()
        time.sleep(1)
        changdu_value = changdu()  # 调用函数并将返回值保存
        print(changdu_value)  # 打印结果

        for i in range(3,changdu_value):
            Date2.append(page.ele(f'x:/html/body/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[1]').text)
            Container_Moves.append(page.ele(f'x:/html/body/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[2]').text)
            Location.append(page.ele(f'x:/html/body/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[3]').text)
            Vessel_Voyage.append(page.ele(f'x:/html/body/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[4]').text)
    except Exception as e:
        print(f"Error fetching data for SO: {so_number}. Error: {e}")

    Date2 = [so_number] + Date2 
    Container_Moves = ['-'] + Container_Moves
    Location = ['-'] + Location
    Vessel_Voyage = ['-'] + Vessel_Voyage


    a = {
                'SO号': [so_number] + ['-'] *(changdu_value -3),
                'Container No.': [non_empty_texts[1]]+ ['-'] *(changdu_value -3),
                'Size/Type': [non_empty_texts[2]]+ ['-'] *(changdu_value -3),
                'Seal No.': [non_empty_texts[3]]+ ['-'] *(changdu_value -3),
                'Service Type': [non_empty_texts[4]]+ ['-'] *(changdu_value -3),
                'Quantity': [non_empty_texts[5]]+ ['-'] *(changdu_value -3),
                'Method': [non_empty_texts[6]]+ ['-'] *(changdu_value -3),
                'VGM': [non_empty_texts[7]]+ ['-'] *(changdu_value -3),
                'Current Status': [non_empty_texts[8]]+ ['-'] *(changdu_value -3),
                'Date': [non_empty_texts[9]]+ ['-'] *(changdu_value -3),
                'Date2': Date2,
                'Container Moves': Container_Moves,
                'Location': Location,
                'Vessel Voyage': Vessel_Voyage,       
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
    data_list.append(data)  # 将 data 添加到 data_list 中

# 将列表中的所有 DataFrame 合并为一个 DataFrame
result = pd.concat(data_list, ignore_index=True)

# 将合并后的 DataFrame 保存到 Excel 文件
result.to_excel(r"D:\\python\\note\\075_driss_emc.xlsx", index=False)

print("Data saved to Excel successfully.")


