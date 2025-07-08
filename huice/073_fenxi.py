import pandas as pd
# 指定文件路径
filename = r'D:\python\test\huice\fudu_data.csv'
# 读取 CSV 文件为 DataFrame
df = pd.read_csv(filename)
# 打印 DataFrame
# 从第二列开始（通过 df.iloc[:, 1:] 获取第二列到最后一列的子集）
df = df.iloc[:, 1:]
print(df)

# def sum_top_10_non_zero(x):
#     # 过滤掉0
#     x_non_zero = x[x != 0]
#     # 获取最大10个数并计算它们的和
#     return x_non_zero.nlargest(10).sum()

# # 对每一列应用该函数
# max_sum_non_zero = df.apply(sum_top_10_non_zero)

# # 将结果转换为 DataFrame 并命名
# result_df = pd.DataFrame(max_sum_non_zero, columns=['max_sum_non_zero'])

# # 显示结果 DataFrame
# print(result_df)
# 假设 df 是你的原始 DataFrame

# 创建一个函数来处理每列非零最大10个数的求和
def sum_top_10_non_zero(x):
    x_non_zero = x[x != 0]  # 过滤掉0
    return x_non_zero.nlargest(10).sum()  # 获取最大10个数并计算它们的和

# 创建一个函数来处理每列非零最小10个数的求和
def sum_bottom_10_non_zero(x):
    x_non_zero = x[x != 0]  # 过滤掉0
    return x_non_zero.nsmallest(10).sum()  # 获取最小10个数并计算它们的和

# 对每一列应用这两个函数
max_sum_non_zero = df.apply(sum_top_10_non_zero)
min_sum_non_zero = df.apply(sum_bottom_10_non_zero)

# 将两个结果组合在一起，生成一个新的 DataFrame
result_df = pd.DataFrame({
    'max_sum_non_zero': max_sum_non_zero,
    'min_sum_non_zero': min_sum_non_zero
})

result_df = result_df.applymap(lambda x: f"{x:.2f}%")

# 显示结果 DataFrame
print(result_df)
# 将 result_df 写入 CSV 文件
filename = r'D:\python\test\huice\result_max_sum_non_zero3.csv'
result_df.to_csv(filename, index=True)


# 长期数据集，每小时统计一次，并且：

# max_sum_non_zero：48小时内（过去48小时）涨幅前10的新币的累计涨幅之和。
# min_sum_non_zero：48小时内（过去48小时）跌幅前10的新币的累计跌幅之和。