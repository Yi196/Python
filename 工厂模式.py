# 工厂模式包涵一个超类。这个超类提供一个抽象化的接口来创建一个特定类型的对象，而不是决定哪个对象可以被创建

# 根据输入产生相应类
class Person:
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

class Male(Person):
    def __init__(self, name):
        print("Hello Mr." + name)

class Female(Person):
    def __init__(self, name):
        print("Hello Miss." + name)

class Factory:
    def getPerson(self, name, gender):
        if gender == 'M':
            return Male(name)
        if gender == 'F':
            return Female(name)


factory = Factory()
person = factory.getPerson("Chetan", "M")


# 简单的工厂模式
# ABCMeta是python的一个元类，用于在Python程序中创建抽象基类，抽象基类中声明的抽象方法，使用abstractmethod装饰器装饰

from abc import ABCMeta,abstractmethod

class Coke(metaclass=ABCMeta):
    @abstractmethod
    def drink(self):
        pass

class Coca(Coke):
    def drink(self):
        print('drink Coca-Cola')

class Pepsi(Coke):
    def drink(self):
        print('drink Pepsi-Cola')

class Fast_food_restaurant():
    def make_coke(self ,name):
        return eval(name)()

KCD=Fast_food_restaurant()
coke=KCD.make_coke('Coca')
coke.drink()#drink Coca-Cola