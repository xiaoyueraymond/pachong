import threading
import time

class Person:
    # 类属性，不需要实例化就能访问的
    coutury = "中国"

    @classmethod
    # cls 代表类本身
    def print_county(cls):
        print(cls.coutury)

    # self: 实例化对象本身
    def __init__(self, name):
        self.name = name
        print(f"人类创建了: {name}")

    def eat_thing(self, name, age):
        while True:
            print(f"我是线程1，名字是{name}，年龄是{age}")
            time.sleep(1)
    
    def drink_thing(self, name, age):
        while True:
            print(f"我是线程2，名字是{name}，年龄是{age}")
            time.sleep(1)

# 打印类属性
print(Person.coutury)

# 创建实例
Sala = Person("sala")
Minggo = Person("Minggo")

# 打印实例的名字
print(Sala.name, Minggo.name)

# 创建线程
thread1 = threading.Thread(target=Sala.eat_thing, args=("sala", 14))
thread2 = threading.Thread(target=Minggo.drink_thing, args=("Minggo", 17))

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()
