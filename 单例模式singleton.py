# 单例模式保证了在程序的不同位置都可以且仅可以取到同一个对象实例


# 一、使用函数装饰器实现单例
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class Cls_1(object):
    def __init__(self):
       pass

cls1 = Cls_1()
cls2 = Cls_1()
print(id(cls1) == id(cls2))


# 二、使用类装饰器实现单例
class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self,):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

@Singleton
class Cls_2(object):
    def __init__(self):
        pass
# 此处装饰器等效于 Cls_2=Singleton(Cls_2)
cls11 = Cls_2()
cls22 = Cls_2()
print(id(cls11) == id(cls22))



# 元类(metaclass) 可以通过方法 __metaclass__ 创造了类(class)，而类(class)通过方法 __new__ 创造了实例(instance)

# 三、使用new关键字实现单例(使用 __new__ 方法在创造实例时进行干预，达到实现单例模式的目的)
class Singleton_1(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        pass

single1 = Singleton_1()
single2 = Singleton_1()
print(id(single1) == id(single2))


# 使用metaclass实现单例
class Singleton_2(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_2, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Cls4(metaclass=Singleton_2):
    pass

cls1 = Cls4()
cls2 = Cls4()
print(id(cls1) == id(cls2))