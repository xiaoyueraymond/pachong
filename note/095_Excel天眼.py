from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import os
browser = Chromium(9333)
page = browser.latest_tab

def company_data():
    count = 0
    # Check if the progress file exists and read the count from it
    if os.path.exists(tianyan_jindu_file_path_6):
        with open(tianyan_jindu_file_path_6, 'r', encoding='utf-8') as jindu_file:
            try:
                count = int(jindu_file.read().strip())
            except ValueError:
                count = 0  # If file is empty or corrupted, start from the beginning

    # 确保文件路径存在
    if not os.path.exists(company_tianyan_path_5):
        with open(company_tianyan_path_5, 'w', encoding='utf-8') as file:
            file.write("")  # Create an empty file if it doesn't exist

    page.get(f"https://www.tianyancha.com/")
    time.sleep(3)

    # Read the Excel file using pandas
    df = pd.read_excel(get_company_span_path_4)  # Assuming the file has only one sheet and relevant data in it

    # Extract company license numbers from the first column
    company_license_numbers = df.iloc[:, 0].dropna().astype(str).tolist()  # Assuming the license numbers are in the first column

    # Check if data already exists in the output file
    existing_data = set()
    if os.path.exists(company_tianyan_path_5):
        with open(company_tianyan_path_5, 'r', encoding='utf-8') as file:
            existing_data = set(file.readlines())

    # Start writing data to the profile file
    with open(company_tianyan_path_5, 'a', encoding='utf-8') as file:
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
            if any(data_line2 in item for item in existing_data):
                print(f"这是第{count}次搜索数据,数据重复不写入{company_tianyan_path_5}")
            else:
                file.write(data_line)
                existing_data.add(data_line)

            count += 1
            print(f"这是第{count}次搜索数据：")
            print(data)
            time.sleep(1)

            # Save the current progress
            with open(tianyan_jindu_file_path_6, 'w', encoding='utf-8') as jindu_file:
                #把count = 0，暂时关闭这个功能，关闭下一次接着上一次爬虫功能
                # count = 0
                jindu_file.write(str(count))



def txt_to_execl():
    # 读取company_tianyan_path_5文件


    # 定义列名
    columns = ['公司名', '营业执照号', '地址', '邮箱', '电话', '链接']

    # 读取文件并处理数据
    data = []
    if os.path.exists(company_tianyan_path_5):
        with open(company_tianyan_path_5, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除每行的空白字符
                if line:
                    # 按'|'分割每行，并确保列数正确
                    row_data = line.split('|')
                    if len(row_data) == len(columns):  # 确保数据列数匹配
                        data.append(row_data)

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    # 打印DataFrame查看
    print(df)

    # 保存为Excel文件
    
    df.to_excel(tianyan_execl_7, index=False)


today_date = time.strftime("%Y%m%d")  # Get today's date in YYYYMMDD format
sku = "execl天眼查"

base_dir = os.path.dirname(os.path.abspath(__file__))
#从execl获取序列号
get_company_span_path_4 = os.path.join(base_dir, f"营业执照号.xlsx")
#从天眼查到的公司信息

company_tianyan_path_5 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_company_tianyan_path_5.txt")

#天眼查的进度
tianyan_jindu_file_path_6 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_tianyan_jindu_file_path_6.txt")

tianyan_execl_7 = os.path.join(base_dir, f"amazon_{today_date}_{sku}_tianyan_execl_7.xlsx")

company_data()

txt_to_execl()





