#封装
class Student:
    def __init__(self,name,age):
        self.name=name
        self.__age=age                        #在类内部的实例属性前加两个下划线如self.__age=age  表示该属性不想被外部访问，但可通过如下方式访问
    def info (self):                               #实际在内部以‘_类名称__age’命名 如'_Student__age'
        print("我叫"+self.name+",今年",self.__age)


st1=Student("xiaoming",20)
st1.info()
print(dir(st1))                                     #通过dir（）函数，获取st1所有可操作参数，找到'_Student__age'
print(st1.name,st1._Student__age)
print()


#继承 和 方法重写
class Person(object):                              #objiect为默认父类，可缺省 Python支持多父类继承
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def info(self):
        print(self.name,self.age)
    def __str__(self):                          #重写__str__方法，实现用print（对象名）返回一个描述 是一种类的特殊方法
        return "我是{0}，今年{1}岁。".format(self.name,self.age)

class Students(Person):                             #Person 为Students的父类
    def __init__(self,name,age,student_id):
        super().__init__(name,age)                  #用super（）调用父类定义子类的实例属性
        self.student_id=student_id
    def info(self):                                  #方法重写 （方法名与父类相同）
        super().info()                               #先调用父类方法
        print("id is ",self.student_id)

class Teacher(Person):
    def __init__(self,name,age,teacher_id):
        super().__init__(name,age)
        self.teacher_id=teacher_id
    def info(self):
        super().info()
        print("id is ",self.teacher_id)

st3=Students("xiaohong",23,10086)
te1=Teacher("li",48,101)
st3.info()
te1.info()
print(st3)                          #此处因为重写了 父类object的__str__方法，使得print（对象名）变为输出一个描述
print()

#多态                                #Python中多态只需要，类中含有被调用方法 无需类间有继承关系 （此处只需类中都有info办法即可）
def a1 (aa):
    aa.info()
a1(st3)
a1(st1)
