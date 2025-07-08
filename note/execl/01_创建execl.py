import pandas as pd

filename = 'D:\\python\\note\\execl\\01.xlsx'
data = pd.read_excel(filename)

# 查看读取的数据

# 新数据
new_data = {
    '平台': ['mexc'],
    '上币时间': ['2025年12月2日 18:00'],
    '开1价格': [None],  # 使用 None 填充
    '开5价格': [None],
    'MAX': [None],
    '1涨幅': [None],
    '5涨幅': [None],
    '币种': ['cab'],
    '合约地址': [None],
    '总结': [None]
}

# 加载现有的工作簿并追加新数据的函数
def xieru():
    global data  # 确保操作的是全局变量 'data'
    
    # 将新数据转为 DataFrame
    new_row = pd.DataFrame(new_data)

    # 检查平台和币种是否已经存在
    if not ((data['平台'] == new_row['平台'].iloc[0]) & (data['币种'] == new_row['币种'].iloc[0])).any():
        # 如果没有重复，追加新数据
        data = pd.concat([data, new_row], ignore_index=True)
        print(f"数据已追加: {new_row}")
        
        # 保存并覆盖原 Excel 文件
        data.to_excel(filename, index=False)  
        print("数据已保存并覆盖原 Excel 文件")
    else:
        print("该平台和币种已经存在，未追加新数据")

    # 查看最终 DataFrame
    print("最终数据：")
    print(data)

if __name__ == '__main__':
    xieru()
