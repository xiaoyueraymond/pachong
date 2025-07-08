import pymysql
from prettytable import PrettyTable

# 连接到 MySQL 数据库
db = pymysql.connect(host='192.168.0.202', port=3306, user='Administrator', passwd='Admin@9000', db='after_sale', charset='utf8')

# 创建游标
cursor = db.cursor()

# 获取所有表的列名
database_name = 'after_sale'
search_value = '81100278T241031364'

cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = %s
""", (database_name,))

columns = cursor.fetchall()

# 查找指定的值
results = []

for table, column in columns:
    # 使用反引号来包裹表名和列名
    query = f"SELECT `{column}` FROM `{table}` WHERE `{column}` LIKE %s"
    cursor.execute(query, ('%' + search_value + '%',))
    rows = cursor.fetchall()

    if rows:
        # 如果该列包含值，收集该表及其列的信息
        results.append((table, column, rows))

# 打印包含该值的表、列及所有列的值
for table, column, rows in results:
    print(f"Table: {table}, Column: {column} contains value: {search_value}")
    
    # 获取该表的所有列
    cursor.execute(f"DESCRIBE `{table}`")
    table_columns = cursor.fetchall()

    # 创建 PrettyTable 对象
    pt = PrettyTable()

    # 设置表格列标题
    pt.field_names = [col[0] for col in table_columns]

    # 打印每一行的完整数据
    for row in rows:
        print("Row Values:")
        cursor.execute(f"SELECT * FROM `{table}` WHERE `{column}` = %s", (row[0],))  # 根据找到的值进一步查询该行的所有数据
        full_row = cursor.fetchall()

        # 添加每行数据到表格
        for full_row_data in full_row:
            pt.add_row(full_row_data)

    # 输出表格
    print(pt)

# 关闭游标和数据库连接
cursor.close()
db.close()
