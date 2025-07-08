
class superstar():
    
    def __init__(self,name,age,sex,techang,ktc,zwjs):
        self.name = name 
        self.age = age
        self.sex = sex
        self.techang = techang
        self.ktc = ktc
        self.zwjs = zwjs

    def koutuchan(self):
        print(self.ktc)
    
    def ziwojieshao(self):
        print(self.zwjs)

caixukun = superstar("蔡徐坤",33,'男',['唱歌',"跳舞","泡妞"],"哎呦你干嘛","时长2年半")
caixukun.ziwojieshao()
print(caixukun.name)


