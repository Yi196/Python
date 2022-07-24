class A:
    pass
class B:
    pass
class C(A,B):
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def info(self):
        print(self.name,self.age)
class D(A):
    pass
x=C("张三",24)

#特殊属性
print(x.__dict__)           #取对象x的属性字典
print(C.__dict__)           #取类C的方法字典
print(x.__class__)          #取对象x所属的类
print(C.__bases__)          #取类C的 所有父类的 元组
print(C.__base__)           #取类C的 第一个父类
print(C.__mro__)            #取类C的层次结构  父类和祖先类的 元组
print(A.__subclasses__())   #取类A的所有子类的 列表


#特殊方法
print("------通过重写__add__()方法，实现自定义的 + 号 (1+2等效于1.__add__(2)点 前不能为数字 要用变量代替)-----")
class Student:
    def __init__(self,name):
        self.name=name
    def __add__(self, other):         #1、重写__add__方法，重定义+号
        return self.name+other.name
    def __len__(self):                #2、重写__len__()方法
        return len(self.name)
    def __str__(self):                #3、重写__str__()方法
        return "姓名为{}".format(self.name)
a=Student("张三")
b=Student("Jack")
s=a+b                                #类的 + 号被重定义
print(s)
s1=a.__add__(b)                      #等效于a+b
print(s1)

print("\n——————————重写__len__()方法，让其参数可自定义———————————")
c=[1,2,3,4]
print(len(c))  #内置函数len（） 求表长
print(c.__len__()) #a.__len__等效len(a)
print(len(a,),len(b))                 #重写后参数可为 对象
print(a.__len__())

print("\n————————重写__str__()方法，使print（对象名）返回一个描述——————————")
print(a,b)

print("\n------__new__()方法用于创建对象，__init__()方法用于对创建的对象初始化-------")
class E:
    def __new__(cls, *args, **kwargs):
        obj=super().__new__(cls)     #__new__()方法用于创建对象
        return obj                   #__init__()方法用于对创建的对象初始化
    def __init__(self,name,age):
        self.name=name
        self.age=age
p=E("小王",20)
print(p.name,p.age)                #表示创建成功

#浅拷贝和深拷贝
print("\n----浅拷贝和深拷贝----")
import copy
p1=copy.copy(p)       #浅拷贝：只拷贝对象，而其子对象不拷贝
p2=copy.deepcopy(p)   #深拷贝：对象和其子对象都拷贝