import time
from ascript.android.action import click, slide
from ascript.android.node import Selector
from ascript.android.screen import FindColors, FindImages
from math import sqrt
from airscript.action import slide
from ascript.android.system import R
import random
from airscript.action import touch

def xunlu():
    # 获取所有的坐标点
    jiaoyin = FindColors.find_all("789,1051,#A1FFFF-222222|791,1051,#A1FFFF-222222", rect=[315, 737, 869, 1616])
    print(f"jiaoyin: {jiaoyin}")
    points = []

    # 如果找到了坐标点
    if jiaoyin:
        for point in jiaoyin:
            x = point.x
            y = point.y
            points.append((x, y))

        print(f"打印脚印坐标：{points}")
        # 提取 x 和 y 的值
        x_values = [x for x, y in points]
        y_values = [y for x, y in points]

        # 计算 x 和 y 的最大最小值
        x_max = max(x_values)
        x_min = min(x_values)
        y_max = max(y_values)
        y_min = min(y_values)

        # 计算 x 和 y 的平均值
        average_x = (x_max + x_min) / 2
        average_y = (y_max + y_min) / 2
        print(f"x的平均值是{average_x},y的平均值是{average_y}")

        # 执行滑动操作
        slide(532, 1109, average_x, average_y, 1000)
    else:
        # 如果没有找到足够的点
        print("脚印点数不足，无法计算距离")
        time.sleep(5)  # 等待 5 秒再尝试






def daboss(yishua):
    print("开始点击传送")
    center_x_value = yishua[0].x
    center_y_value = yishua[0].y + 50
    print(f"点击传送：{center_x_value}, {center_y_value}")
    click(center_x_value, center_y_value,500)  
    print(f"寻找传送门")    
    time.sleep(0.6)  
    chuansongmen = FindImages.find_all_template([R.img("传送门.png"),],confidence= 0.95)
    if not isinstance(chuansongmen, list):
        # 如果不是数组，则将其转换为数组
        chuansongmen = [chuansongmen]
    print(f"传送门: {chuansongmen}")
    click(chuansongmen[0]['center_x'], chuansongmen[0]['center_y'],500) 
    print(f"传送门坐标: {chuansongmen[0]['center_x']},{chuansongmen[0]['center_y']}")
    time.sleep(1)
    click(739, 1375, 300)
    time.sleep(2)
    print(f"开始寻找boss残血:")
    bosstouxiangchuxian = FindColors.find("619,513,#9C1E0E|619,524,#9C1E0E|619,526,#9C1E0E|617,537,#95150A",rect=[363,487,802,557])
    print(f"boss血条：{bosstouxiangchuxian}:")
    if not isinstance(bosstouxiangchuxian, list):
        # 如果不是数组，则将其转换为数组
        bosstouxiangchuxian = [bosstouxiangchuxian]
    if bosstouxiangchuxian[0] is None:   
        for i in range(5):
            print(f"bosstouxiangchuxian没有残血，执行第 {i + 1} 次寻路操作")
            xunlu()
            time.sleep(2)  # 每次调用间隔 2 秒
    else:
        print("正在打boss,等待50秒")
        time.sleep(50)

def bossing():  
    bosstouxiangchuxian = FindColors.find("619,513,#9C1E0E|619,524,#9C1E0E|619,526,#9C1E0E|617,537,#95150A",rect=[363,487,802,557])
    print(f"boss血条：{bosstouxiangchuxian}:")
    if not isinstance(bosstouxiangchuxian, list):
        # 如果不是数组，则将其转换为数组
        bosstouxiangchuxian = [bosstouxiangchuxian]
    if bosstouxiangchuxian[0] is None:   
        print("没在打boss,程序继续执行")
    else:
        print("正在打boss,等待50秒")
        time.sleep(50)

#下滑找刷新
def xiahua():
    slide(165,744,165,644,450)
    time.sleep(5)
    # 查找白色的boss名字
    yishua = FindColors.find("99,582,#F4F1E9-222222",rect=[35,331,201,758])
    print(f"yishua: {yishua}")
    if not isinstance(yishua, list):
        # 如果不是数组，则将其转换为数组
        yishua = [yishua]
    print(f"yishua的类型{type(yishua)},{yishua}")
    if  yishua[0] == None: 
        print("没有找到刷新的图片,再次调用下滑")
        xiahua()
    else:
        daboss(yishua)

            
while True:
    try:
        bossing()
        # 查找白色的boss名字
        yishua = FindColors.find("99,582,#F4F1E9-222222",rect=[35,331,201,758])
        print(f"yishua: {yishua}")
        if not isinstance(yishua, list):
            # 如果返回结果不是数组，转换为数组
            yishua = [yishua]
        print(f"yishua的类型{type(yishua)}, {yishua}")

        if yishua[0] is None:
            print("没有找到刷新的图片, 开始向上滑2次")
            # 一次性滑到顶部，再慢慢往下滑，直到找到
            slide(165, 344, 165, 744, 500)
            time.sleep(2)
            slide(165, 344, 165, 744, 500)
            time.sleep(2)
            print("没有找到刷新的图片, 调用下滑")
            yishua = xiahua()
        else:
            # 如果找到图片，调用 daboss 函数
            daboss(yishua)
        
        # 暂停一段时间后继续循环
        time.sleep(1)

    except Exception as e:
        # 捕获任何异常，并打印出来，避免程序崩溃
        print(f"发生异常: {e}")
        time.sleep(5)  # 在出现异常后等待 5 秒钟再重试








