from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import os

# 初始化浏览器并获取最新的标签页
browser = Chromium(9333)
page = browser.latest_tab



def company_data():
    count = 0
    # Progress tracking file path
    jindu_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_jindu.txt")

    # Check if the progress file exists and read the count from it
    if os.path.exists(jindu_file_path):
        with open(jindu_file_path, 'r', encoding='utf-8') as jindu_file:
            try:
                count = int(jindu_file.read().strip())
            except ValueError:
                count = 0  # If file is empty or corrupted, start from the beginning

    # 确保文件路径存在
    if not os.path.exists(company_profile_file_path):
        with open(company_profile_file_path, 'w', encoding='utf-8') as file:
            file.write("")  # Create an empty file if it doesn't exist

    page.get(f"https://www.tianyancha.com/")
    time.sleep(3)

    # Read lines from the input file and process data
    with open(txt_to_txt_profile_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract company license numbers
    company_license_numbers = [line.split('|')[1].strip() for line in lines if line.strip()]

    # Check if data already exists in the output file
    existing_data = set()
    if os.path.exists(company_profile_file_path):
        with open(company_profile_file_path, 'r', encoding='utf-8') as file:
            existing_data = set(file.readlines())

    # Start writing data to the profile file
    with open(company_profile_file_path, 'a', encoding='utf-8') as file:
        for yingyehzhizhao_num in company_license_numbers[count:]:  # Start from the 'count' line
            url = f"https://www.tianyancha.com/nsearch?key={yingyehzhizhao_num}"
            page.get(url)
            time.sleep(1)

            try:
                # Find company name
                element_company_name = page.ele("x://a[@class='index_alink__zcia5 link-click']", timeout=1)
                company_name = element_company_name.child().text
            except:
                company_name = "未找到company_name"

            try:
                # Get phone number
                element_phone_number = page.ele("x://span[@class='index_value__Pl0Nh']//span", timeout=1)
                phone_number = element_phone_number.text
            except:
                phone_number = "未找到phone_number"

            try:
                # Get email
                element_mail = page.ele("x://a[@class='index_common-link__LzdEO']", timeout=1)
                mail = element_mail.text
            except:
                mail = "未找到mail"

            try:
                # Get address
                element_adress = page.eles("x://span[@class='index_value__Pl0Nh']", timeout=1)
                address = element_adress[4].text if len(element_adress) > 4 else "未找到"
            except:
                address = "未找到address"

            data = {
                '公司名': company_name,
                '营业执照号': yingyehzhizhao_num,
                '地址': address,
                '邮箱': mail,
                '电话': phone_number,
                '链接': url
            }

            # Check if the data already exists
            data_line = f"{data['公司名']}|{data['营业执照号']}|{data['地址']}|{data['邮箱']}|{data['电话']}|{data['链接']}\n"
            data_line2 = f"{data['营业执照号']}"
            if data_line2 not in existing_data:
                file.write(data_line)
                existing_data.add(data_line)
            else:
                print(f"这是第{count}次搜索数据,数据重复不写入{company_profile_file_path}")

            count += 1
            print(f"这是第{count}次搜索数据：")
            print(data)
            time.sleep(1)

                
            # Save the current progress
            with open(jindu_file_path, 'w', encoding='utf-8') as jindu_file:
                jindu_file.write(str(count))





# 读取txt文件并处理
def read_and_merge():
    # 读取两个txt文件
    with open(txt_to_txt_profile_file_path, 'r', encoding='utf-8') as file1:
        lines1 = file1.readlines()
    
    with open(company_profile_file_path, 'r', encoding='utf-8') as file2:
        lines2 = file2.readlines()

    # 用于存储拼接结果
    merged_data = []

    # 比较并拼接
    for line1 in lines1:
        second_element_1 = line1.split('|')[1].strip()  # 假设第二个元素是需要比较的部分
        for line2 in lines2:
            second_element_2 = line2.split('|')[1].strip()  # 假设第二个元素是需要比较的部分
            if second_element_1 == second_element_2:
                # 拼接两行数据
                merged_line = line1.strip() + '|' + line2.strip()
                merged_data.append(merged_line)

    # 切分拼接后的数据并按照列格式组织
    final_data = []
    for line in merged_data:
        # 假设每行数据是用'|'分隔的
        split_line = line.split('|')
        # 确保数据有足够的列数
        if len(split_line) == 12:
            final_data.append(split_line)

    # 定义列名，确保在任何条件之前定义
    columns = ['公司名', '营业执照号', '地址', 'QQ', '电话', '链接', '公司名', '营业执照号', '地址', '邮箱', '电话', '链接']

    # 如果目标文件不存在，则创建一个新的DataFrame并保存为Excel
    if not os.path.exists(finnly_profile_file_path):
        # 创建DataFrame
        df = pd.DataFrame(final_data, columns=columns)
        df.to_excel(finnly_profile_file_path, index=False)
        print(f"新文件已创建并写入：{finnly_profile_file_path}")
    else:
        # 如果文件已经存在，检查文件中是否有相同的数据
        existing_data = pd.read_excel(finnly_profile_file_path)

        # 检查是否已经存在拼接的内容
        new_data = pd.DataFrame(final_data, columns=columns)
        existing_data_set = set(tuple(x) for x in existing_data.values)

        # 过滤掉已存在的数据
        new_data = new_data[~new_data.apply(tuple, 1).isin(existing_data_set)]

        if not new_data.empty:
            # 如果有新数据，追加写入Excel文件
            with pd.ExcelWriter(finnly_profile_file_path, mode='a', engine='openpyxl') as writer:
                new_data.to_excel(writer, index=False, header=False)
            print(f"新数据已追加到文件：{finnly_profile_file_path}")
        else:
            print("没有新数据需要写入。")



# 设置文件路径
sku = "Hook"
txt_to_txt_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.txt")
company_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_company_data.txt")
finnly_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_finnly_data.xlsx")
jindu_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.txt")

#读取文件从亚马逊抓到的公司数据amazon_{sku}_data.txt，从amazon_{sku}_data.txt读取营业执照号，再从天眼查寻找，无法过验证码，手动过验证码，这就要从哪里断掉寻找，从哪里接起来，查找
#查找amazon_{sku}_data.txt进度，从这个进度开始找公司，避免了重复查找，有新的公司就写入。

company_data()
# 执行合并和保存操作
read_and_merge()
