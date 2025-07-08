import  pandas as pd

data ={'Name':['Alice','Bob','Charlie'],
       'Age':[25,30,35]}

df = pd.DataFrame(data)
print(df)

df = pd.DataFrame(data, index=['Person1','Person2', 'Person3'])
print(df)

# 读取文件
# pd.read*()函数，用于从不同数据源读取数据并将其加载到 Pandas 的 DataFrame 中。
# df = pd.read csv('data.csv”)
# df= pd.read excel('data.xlsx',sheet name='sheet1’)
# df= pd.read json('data.json')
# pd.read_sql() 用于从 SQL 数据库中读取数据，需要连接到数据库并指定 SQL 查询。
# pd.read html()用于从 HTML 网页中提取表格数据。它返回的是一个包含所有表格的pd.read_pickle()用于从 Pickle 格式的数据中读取数据。Pickle 是 Python 的序列化格式

# 读取csv文件
# 基本语法 dfpd.read csv(filepath or buffer,delimiter=None.sep='，,二header='infer,names=None,index col=None, usecols=None)
# 'filepath_or_buffer’: 必需，指定要读取的CSV文件的路径或URL，可以是字符串或类文
# 件对象。'sep':可选，指定CSV文件中字段之间的分隔符，默认为逗号(，)。delimiter':可选，与'sep'参数相同，用于指定分隔符。'header': 可选，指定哪一行作为列名，可以是整数、列表或None。默认为infer'，表示自动推断列名。
# names':可选，用于指定列名的列表，如果"header'参数为None时使用。index_co1':可选，用于指定哪一列作为行索引的列号或列名，默认为None，表示没有行索引。
# 可选，用于选择要读取的列的列表，可以是列号或列名，默认为None，表示读usecols :取所有列。

# read csv()常用参数--查官方文档
# chunksize: 每次读多少行，在处理特别大的数据时使用提高效率，无需一次性将文件夹在到内存中。
# header=0代表用第一行作为表头，需要自定header= None 代表文件中没有列名，自定义names=[]
filepath = r"D:\work2\mysql\导入.csv"
df = pd.read_csv(filepath, header=0, names=['a', 'b', 'c','4'], chunksize = 3)
print('3-----------------------------------------------chunk-----------------------------------------------')
for chunk in df:

    print(chunk)

df = pd.read_csv(filepath, header=0, names=['a', 'b', 'c','4'])
print('4-----------------------------------------------chunk-----------------------------------------------')
print(df.head(1))
print(df.tail(1))
print(df.tail(1))

df = pd.read_csv(filepath, header=0,)
print('5-----------------------------------------------chunk-----------------------------------------------')
print(df)

df = pd.read_csv(filepath, names=['1', '2', '3','4'])
print('5-----------------------------------------------chunk-----------------------------------------------')
print(df)
print(df.sample(3))

df = pd.read_csv(filepath, names=['1', '2', '3','4'],index_col='1')
print('5-----------------------------------------------chunk-----------------------------------------------')
print(df)


# 缺失值、重复值
# 检测缺失值:使用isna()或isnul()方法来检测缺失值，返回布尔值的DataFrame，其中True表示缺失值。df.isna()
# 删除缺失值:使用dropna()方法删除包含缺失值的行或列。df.dropna(axis=1)删除包含缺失值的列,df.dropna(axis=0)删除包含缺失值的行
# 填充缺失值:使用filna()方法将缺失值替换为指定的值。fina(0)，ffil，bfi
# 检测重复数据:使用duplicated()方法检测重复的行，返回布尔值的Series，其中True表示重复的行
# 删除重复的行:df.drop duplicates()

# 数据类型转换
# 查看数据类型:df.dtypes
# 转换列的数据类型:astype()方法将一列的数据类型转换为其他类型df['A’] = df'A'].astype(float)
# 日期和时间转换:处理日期和时间数据通常需要将字符串转换为日期时间对象df['Date’]= pd.to datetime(df['Date'])

# 数据切片
# 常用的切片方法
# 根据列名:使用列名来选择DataFrame的列子集df['col1’]根据行索引进行切片df.loc['row labe1’]同时进行行和列切片
# df[['col1', 'col2’]
# df.iloc[1:3]df.iloc[0]
# subset = df.loc'Row Label', ['Column1', 'Column2']]

import pandas as pd

data ={'A':[1,2,3,4,5],
        'B':[10,20,30,40,50]}
print('6-----------------------------------------------打印所有数据-----------------------------------------------')
df= pd.DataFrame(data)
print(df)
print('7-----------------------------------------------select 索引1到3 A列的数据-----------------------------------------------')
select_date = df.loc[1:3,'A']
print(select_date)
print('8-----------------------------------------------select 第三行所有列數據-----------------------------------------------')
select_date = df.loc[2]
print(select_date)
print('9-----------------------------------------------select B列所有數據-----------------------------------------------')
select_date = df.loc[:,'B']
print(select_date)

print('10-----------------------------------------------select 特定的行和列-----------------------------------------------')
select_date = df.iloc[1:3,0]
print(select_date)

print('11-----------------------------------------------select A列大于3的行-----------------------------------------------')
select_date = df[df['A'] > 3]
print(select_date)