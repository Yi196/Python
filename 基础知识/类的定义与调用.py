# 类

# 类的创建过程
# 首先,python 调用内置的type类，然后type调用内置的元类mateClass，mateClass再调用__new__方法将类实例化，此时完成了第一步
# 然后，这个实例将会初始化自己的类变量，就是把自己从头到尾扫视一遍，
# 之后，进入构造方法，并初始化自己的实例变量。


# 1、用 type 创造类
def func(self):
    print('do sth')

Klass = type('Klass', (object,), {'func':func})

c = Klass()
c.func()


# 创建
class Student:                                 # 类名默认大写首字母
    shenfen="学生"                              # 类属性    所有对象共享（不用实例化也可以访问）
    def __init__(self,name,age):               # 初始化方法  用于创建对象时对对象进行赋初值，其中self.name称为实例属性
        self.name=name
        self.age=age                           # 实例变量（是动态创建的。必须实例化之后才可以访问，因为之前是不存在的）

    def info(self):                             # 实例方法  用于绑定调用此方法的实例对象 默认参数为self 自身 用于处理对象中数据  （“类”中的函数定义都称作”方法“）
        print("我叫:"+self.name+"，今年%d岁" % (self.age))

    @classmethod
    def cm(cls):                              # 类方法 用“@classmethod”声明 Python 会自动将类本身绑定给 cls 参数（注意，绑定的不是类对象）类方法推荐使用类名直接调用
        print("正在调用类方法",cls)

    @staticmethod
    def sm():                                 # 静态方法 用“@staticmethod”声明  无默认值(不用实例化也可访问)
        print("静态方法")
# 静态方法，其实就是我们学过的函数，和函数唯一的区别是，静态方法定义在类这个空间（类命名空间）中，而函数则定义在程序所在的空间（全局命名空间）
# 因此 Python 解释器不会对它包含的参数做任何类或对象的绑定。也正因为如此，类的静态方法中无法调用任何类属性和类方法
# 调用
print(Student.shenfen)
print(Student.sm())
st1=Student("Yi",24)
st1.info()                   # 等效于Student.info(st1)
Student.info(st1)
print(st1.name,st1.age)
st2=Student("XiaoMing",26)
st2.info()
print(st1.shenfen,st2.shenfen)    # 类属性 所有对象共享
Student.shenfen="研究生"
print(st1.shenfen,st2.shenfen,"\n")
print(type(st1))      # <class '__main__.Student'>

# 类方法 静态方法的调用  类名直接调用
Student.cm()
Student.sm()

# 为类对象动态绑定属性、方法
print("-----为类对象动态绑定属性、方法-------")
st1.gender="男"                    # 为对象st1动态绑定属性 gender =”男“
print(st1.name,st1.age,st1.gender)

def show (name):
    print(name+"是个学生")
st2.show=show                     # 为对象st2动态绑定方法（函数）
st2.show(st2.name)


import math
class Circle :
    def __init__(self,r):
        self.r=r
    def arear(self):
        return math.pi*math.pow(self.r,2)
    def perimeter(self):
        return math.pi*2*self.r


class Test:
    def __new__(cls, *args, **kwargs):
        return super(Test, cls).__new__(cls)
        # return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        self.age = args[0]

    def get_age(self):
        return  self.age

    @classmethod
    def make(cls, num, *args, **kwargs):
        lst = []
        for i in range(num):
            lst.append(cls.__new__(cls))

        # 需要手动调用__init__()才能实例化对象
        [i.__init__(*args, **kwargs) for i in lst]
        return lst


if __name__ == '__main__':
    num=float(input("请输入圆的半径"))
    c=Circle(num)
    print("圆的面积为:{:.3f}".format(c.arear()))
    print("圆的周长为:{:.3f}".format(c.perimeter()))

    test_lst = Test.make(3, 18)
    print(test_lst)
    print(test_lst[1].get_age())