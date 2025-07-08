from DrissionPage import Chromium, ChromiumPage
import time
import random
import pandas as pd
import os

# 初始化浏览器并获取最新的标签页
browser = Chromium()
page = browser.latest_tab





import os

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
        if os.path.exists(base_url_path):
            print(f"文件 {base_url_path} 已存在，检查重复 URL")
            with open(base_url_path, 'r') as file:
                existing_urls = file.readlines()
                # If the URL is not already in the file, write it
                if new_url + '\n' not in existing_urls:
                    print(f"新 URL 未存在，写入文件: {new_url}")
                    with open(base_url_path, 'a') as file_append:
                        file_append.write(new_url + '\n')
                else:
                    print(f"URL 已存在: {new_url}")
        else:
            # If the file doesn't exist, create it and write the URL
            print(f"文件 {base_url_path} 不存在，创建文件并写入 URL: {new_url}")
            with open(base_url_path, 'w') as file:
                file.write(new_url + '\n')


def get_mianpage_url():
   
    # Path to the base URL file
    base_url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_base_urls.txt")
    
    # Load URLs from the file
    base_urls = []
    if os.path.exists(base_url_path):
        with open(base_url_path, "r", encoding="utf-8") as file:
            base_urls = [line.strip() for line in file if line.strip()]
        print(f"已加载 {len(base_urls)} 个基础 URL")
    else:
        print(f"文件 {base_url_path} 不存在")
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

        # Load existing URLs from the text file, if it exists
        text_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_page_two_urls.txt")
        existing_urls = set()
        if os.path.exists(text_file_path):
            with open(text_file_path, "r", encoding="utf-8") as file:
                existing_urls = {line.strip() for line in file if line.strip()}
            print(f"已加载 {len(existing_urls)} 个现有 URL")
        
        # Write new URLs to the file
        with open(text_file_path, "a", encoding="utf-8") as file:  # Append mode
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
        
        # Read the URLs from page_two_file_path
        with open(page_two_file_path, 'r') as file:
            page_two_urls = file.readlines()
        
        # Open the seller profile file in append mode to write new href if not already present
        with open(seller_profile_file_path, 'a+') as seller_file:
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
        if not os.path.exists(df_to_excel_profile_file_path):
            with open(df_to_excel_profile_file_path, 'w', encoding='utf-8'):
                pass  # Just to create the file

        # Read existing data from the file to avoid duplicates
        #df_to_excel_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.txt")
        with open(df_to_excel_profile_file_path, 'r', encoding='utf-8') as file:
            existing_data = file.readlines()

        # Read URLs from sellerProfileTriggerId.txt
        #seller_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_sellerProfileTriggerId.txt")
        with open(seller_profile_file_path, 'r') as file:
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
                with open(df_to_excel_profile_file_path, 'a', encoding='utf-8') as file:
                    file.write(data_str)
                existing_data.append(data_str)  # Add to the in-memory list to avoid future duplicates
                # print(existing_data)

    except Exception as e:
        print(f"发生错误: {e}")

def data_to_excel():

    
    # 读取 txt 文件并将其转换为 DataFrame
    with open(df_to_excel_profile_file_path, 'r', encoding='utf-8') as file:
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

# sku = "Hook"
sku = input("请输入你要搜索的类目：")
base_url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_base_urls.txt")
page_two_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_page_two_urls.txt")
seller_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_sellerProfileTriggerId.txt")
df_to_excel_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.txt")
txt_to_excel_profile_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"amazon_{sku}_data.xlsx")


for i in range(0,1):
    #搜集SKU，用来获取搜索1-10页的链接，保存到amazon_{sku}_base_urls.txt
    page_url(sku)

    #从1-10页的链接，获取商品链接，1页48个商品，保存到amazon_{sku}_page_two_urls.txt
    get_mianpage_url()

#从amazon_{sku}_page_two_urls.txt获取公司地址链接，保存到amazon_{sku}_sellerProfileTriggerId.txt，
# 这里应该加上进度，防止断掉，重头开始，还没写好。
find_sellerProfileTriggerId()

# 从公司地址链接获取公司信息，保存到"amazon_{sku}_data.txt，如果字段data_str2 = f"{data['公司名']}|{data['营业执照号']}|{data['地址']}|{data['QQ']}|{data['电话']}\n"，重复则不保存，否则保存。
process_seller_data()
# data_to_excel()

