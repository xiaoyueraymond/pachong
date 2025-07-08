from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import os

# 初始化浏览器并获取最新的标签页
browser = Chromium(9333)
page = browser.latest_tab


def page_url(sku):
    # Initialize URL
    url = "https://www.amazon.pl/ref=nav_logo"
    print(f"访问主页: {url}")
    page.get(url)
    page.wait.load_start()
    # Input SKU and search
    print(f"输入 SKU: {sku} 进行搜索")
    input_element = page.ele("x://input[@id='twotabsearchtextbox']", timeout=2)
    input_element.clear()
    input_element.click()
    input_element.input(sku)
    
    input_element = page.ele("x://input[@id='nav-search-submit-button']", timeout=2)
    print("点击搜索按钮")
    input_element.click()
    
    # Wait for page to load
    print("等待页面加载...")
    page.wait.load_start()
    print(page.url)
    # Split the URL at the first '&'
    base_url, query_params = page.url.split("&", 1)
    print(f"基础 URL: {base_url}, 查询参数: {query_params}")
    
    # Prepare the URLs for pages 1 to 9
    for page_number in range(1, 10):
        # Create the new URL
        new_url = f"{base_url}&page={page_number}&{query_params}"
        print(f"生成的新 URL: {new_url}")
        
        # Check if the new URL already exists in the file
        if os.path.exists(base_url_path_1):
            print(f"文件 {base_url_path_1} 已存在，检查重复 URL")
            with open(base_url_path_1, 'r') as file:
                existing_urls = file.readlines()
                # If the URL is not already in the file, write it
                if new_url + '\n' not in existing_urls:
                    print(f"新 URL 未存在，写入文件: {new_url}")
                    with open(base_url_path_1, 'a') as file_append:
                        file_append.write(new_url + '\n')
                else:
                    print(f"URL 已存在: {new_url}")
        else:
            # If the file doesn't exist, create it and write the URL
            print(f"文件 {base_url_path_1} 不存在，创建文件并写入 URL: {new_url}")
            with open(base_url_path_1, 'w') as file:
                file.write(new_url + '\n')


def get_mianpage_url():
   
    # Path to the base URL file
    
    # Load URLs from the file
    base_urls = []
    if os.path.exists(base_url_path_1):
        with open(base_url_path_1, "r", encoding="utf-8") as file:
            base_urls = [line.strip() for line in file if line.strip()]
        print(f"已加载 {len(base_urls)} 个基础 URL")
    else:
        print(f"文件 {base_url_path_1} 不存在")
        return
    
    page_number = 0
    # Iterate over each base URL and append page_number for pagination
    for base_url in base_urls:
        page_number = page_number + 1
        # Generate the URL for the current page using base URL and page number
        url = f"{base_url}&page={page_number}"
        print(f"处理 URL: {url}")
        
        # Make the request to the page
        page.get(url)
        
        # Wait for page to load (you can re-enable if necessary)
        # page.wait.load_start()

        # Extract product links
        elements = page.eles('@class^a-link-normal s-line-clamp-4 s-link-style a-text-normal')
        print(f"找到 {len(elements)} 个产品链接")

        existing_urls = set()
        if os.path.exists(product_url_path_2):
            with open(product_url_path_2, "r", encoding="utf-8") as file:
                existing_urls = {line.strip() for line in file if line.strip()}
            print(f"已加载 {len(existing_urls)} 个现有 URL")
        
        # Write new URLs to the file
        with open(product_url_path_2, "a", encoding="utf-8") as file:  # Append mode
            for i, element in enumerate(elements, 1):
                page_two = element.attr("href")
                print(f"处理第 {i} 个链接: {page_two}")
                if page_two not in existing_urls:  # Only add if not already present
                    file.write(page_two + "\n")  # Save page_two to text file
                    existing_urls.add(page_two)  # Update the set to prevent duplicates in this run
                    print(f"已保存新 URL: {page_two}")
                else:
                    print(f"跳过重复 URL: {page_two}")



def find_sellerProfileTriggerId():
    # File paths

    
    try:
        print("Entering second page...")
        
        # Read the URLs from product_url_path_2
        with open(product_url_path_2, 'r') as file:
            page_two_urls = file.readlines()
        
        # Open the seller profile file in append mode to write new href if not already present
        with open(seller_url_path_3, 'a+') as seller_file:
            # Read existing hrefs to avoid duplicates
            seller_file.seek(0)
            existing_hrefs = seller_file.readlines()
            existing_hrefs = [href.strip() for href in existing_hrefs]

            count = 0 
            for url in page_two_urls:
                count = count + 1
                page.get(url.strip())
                print(f"第{count}次获取链接")
                # page.wait.load_start()  # Uncomment if needed to wait for page load
                
                # Try to find the sellerProfileTriggerId element
                element = page.ele("x://a[@id='sellerProfileTriggerId']",timeout=1)
                if element:
                    href = element.attr("href")
                    print(f"Found href: {href}")

                    # If href is not already in the seller profile file, write it
                    if href not in existing_hrefs:
                        seller_file.write(href + "\n")
                        print(f"Written href: {href}")
                    else:
                        print(f"Href already exists: {href}")
                else:
                    print("No sellerProfileTriggerId element found on this page.")
    except Exception as e:
        print(f"Error in find_sellerProfileTriggerId: {e}")




# Define a placeholder for page scraping logic
# Ensure you initialize your page object here (e.g., playwright or selenium setup)

def process_seller_data():
    try:
    
        # Check if the output file exists, if not, create it
        if not os.path.exists(get_company_span_path_4):
            with open(get_company_span_path_4, 'w', encoding='utf-8'):
                pass  # Just to create the file

        # Read existing data from the file to avoid duplicates
        #get_company_span_path_4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.txt")
        with open(get_company_span_path_4, 'r', encoding='utf-8') as file:
            existing_data = file.readlines()

        # Read URLs from sellerProfileTriggerId.txt
        #seller_url_path_3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_sellerProfileTriggerId.txt")
        with open(seller_url_path_3, 'r') as file:
            urls = file.readlines()

        count = 0 
        for url in urls:
            count += 1
            url = url.strip()
            page.get(url)
            
            #等待加载完成
            # page.wait.load_start() 
            try:
                # print("开始寻找公司信息span")
                # Find all span elements in the specific section
                elements = page.eles("x://div[@id='page-section-detail-seller-info']//span",timeout=1)
                data_list = [element.text for element in elements]
            except:
                elements = "未找到elements"
            
            # print("开始判断span元素长度")
            if len(data_list) < 12:  # Ensure enough elements exist
                print(f"span 元素数量不足 for {url}")
                continue  # Skip this URL if the span elements are insufficient

            # Extract relevant data
            data = {
                '公司名': data_list[2],
                '营业执照号': data_list[6],
                '地址': ' '.join(data_list[-8:-1]),
                'QQ': data_list[12],
                '电话': data_list[10],
                '链接': url
            }
            print(f"第{count}个链接的数据:")
            print(data)
            
            # Create a string representation of the data to check for duplicates
            data_str = f"{data['公司名']}|{data['营业执照号']}|{data['地址']}|{data['QQ']}|{data['电话']}|{url}\n"
            data_str2 = f"{data['营业执照号']}"
            # Check if data already exists in the file
            # if data_str2 not in existing_data:
            if any(data_str2 in item for item in existing_data):
                print(f"{data_str2}已经存在，不写入amazon_{sku}_data.txt")
            else:
                with open(get_company_span_path_4, 'a', encoding='utf-8') as file:
                    file.write(data_str)
                existing_data.append(data_str)  # Add to the in-memory list to avoid future duplicates
                # print(existing_data)

    except Exception as e:
        print(f"发生错误: {e}")

def data_to_excel():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_to_excel_profile_file_path = os.path.join(base_dir, f"amazon_{today_date}_{sku}_get_company_span_path_4.xlsx")
    
    # 读取 txt 文件并将其转换为 DataFrame
    with open(get_company_span_path_4, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 假设每一行是以 "|" 分隔的字段
    data = []
    for line in lines:
        data.append(line.strip().split('|'))
    
    # 创建 DataFrame
    df = pd.DataFrame(data, columns=['公司名', '营业执照号', '地址', 'QQ', '电话', '链接'])
    
    # 打印 DataFrame
    print(df)
    
    # 将 DataFrame 写入 Excel 文件
    df.to_excel(txt_to_excel_profile_file_path, index=False)




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

    # Read lines from the input file and process data
    with open(get_company_span_path_4, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract company license numbers
    company_license_numbers = [line.split('|')[1].strip() for line in lines if line.strip()]

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
                count = 0
                jindu_file.write(str(count))





# 读取txt文件并处理
# 读取txt文件并处理
def read_and_merge():
    # 读取两个txt文件
    with open(get_company_span_path_4, 'r', encoding='utf-8') as file1:
        lines1 = file1.readlines()
    
    with open(company_tianyan_path_5, 'r', encoding='utf-8') as file2:
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
            with pd.ExcelWriter(finnly_profile_file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                new_data.to_excel(writer, index=False, header=False)
            print(f"新数据已追加到文件：{finnly_profile_file_path}")
        else:
            print("没有新数据需要写入。")


today_date = time.strftime("%Y%m%d")  # Get today's date in YYYYMMDD format
sku = input("请输入你要搜索的类目：")

# 构建文件路径
base_dir = os.path.dirname(os.path.abspath(__file__))
#1-10页链接
base_url_path_1 = os.path.join(base_dir,"log", f"amazon_{today_date}_{sku}_base_url_path_1.txt")

#从1-10页链接获取的商品链接
product_url_path_2 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_product_url_path_2.txt")

#销售商链接
seller_url_path_3 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_seller_url_path_3.txt")

#存储span信息
get_company_span_path_4 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_get_company_span_path_4.txt")

#从天眼查到的公司信息
company_tianyan_path_5 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_company_tianyan_path_5.txt")

#天眼查的进度
tianyan_jindu_file_path_6 = os.path.join(base_dir, "log", f"amazon_{today_date}_{sku}_tianyan_jindu_file_path_6.txt")

#最后合成文件。
finnly_profile_file_path = os.path.join(base_dir, f"amazon__{today_date}_{sku}_finnly_data.xlsx")

#读取文件从亚马逊抓到的公司数据amazon_{sku}_data.txt，从amazon_{sku}_data.txt读取营业执照号，再从天眼查寻找，无法过验证码，手动过验证码，这就要从哪里断掉寻找，从哪里接起来，查找
#查找amazon_{sku}_data.txt进度，从这个进度开始找公司，避免了重复查找，有新的公司就写入。


#1.搜集SKU，用来获取搜索1-10页的链接，保存到amazon_hook_base_url_path_1
page_url(sku)

#2.从1-10页的链接，获取商品链接，1页48个商品，保存到amazon_hook_product_url_path_2
get_mianpage_url()

#3.从amazon_hook_product_url_path_2获取公司地址链接，保存到amazon_hook_seller_url_path_3
# 这里应该加上进度，防止断掉，重头开始，还没写好。
find_sellerProfileTriggerId()

# amazon_hook_seller_url_path_3获取公司信息，保存到"amazon_{sku}_data.txt，如果字段data_str2 = f"{data['公司名']}|{data['营业执照号']}|{data['地址']}|{data['QQ']}|{data['电话']}\n"，重复则不保存，否则保存。
process_seller_data()

#先生成一个execl
data_to_excel()

#从天眼查询公司信息
company_data()

# 执行合并和保存操作
read_and_merge()
