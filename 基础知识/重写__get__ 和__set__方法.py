#重写__get__ 和__set__方法
class C:
    def __init__(self,value=26.0):
        self.value=float(value)
    def __get__(self, instance, owner):   #重写__get__或__set__后才能把类赋给属性:num_c
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)

class F:
    def __get__(self, instance, owner):           #读num_f时，直接读取到num_c并*1.8+32
        return instance.num_c * 1.8+32
    def __set__(self, instance, value):           #对num_f赋值时，直接转换后对num_c赋值
        instance.num_c=(float(value)-32)/1.8

class CF:
    num_c=C()
    num_f=F()

cf=CF()
print(cf.num_c)
print(cf.num_f)
cf.num_c=50
print(cf.num_c)
print(cf.num_f)
cf.num_f=200
print(cf.num_c)
print(cf.num_f)