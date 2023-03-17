from multiprocessing.managers import BaseManager
from multiprocessing import Process, Lock, Value


# 用Manger()共享类的实例对象
'''
由manager建立的类对象，只能访问其成员函数，而不能直接访问其成员变量;
当我们使用同一个manager, 并在其中注册不同的类对象之后，在不同的地方定义manager对象，可能会产生未知的错误，
因此最好的方式应该为，在什么地方定义一个manager对象，就在什么地方定义一个新的继承自BaseManager类的对象，并注册新类对象.
'''


class MyManager(BaseManager):  # 避免多处都使用BaseManager时发生错误
    pass

class Employee(object):        # 需要共享的实例
    def __init__(self, name, salary):
        self.name = name
        self.salary = Value('i', salary)
    def increase(self):
        self.salary.value += 100
    def getpay(self):
        return self.name + ':' + str(self.salary.value)


# 将需要共享的类对象注册在管理器类中
MyManager.register('Employee', Employee)


def func1(em, lock):
    with lock:
        em.increase()


if __name__ == '__main__':
    # 先实例化BaseManager服务器代理对象并开启服务
    manager = MyManager()
    manager.start()
    # 再实例化需共享的类
    em = manager.Employee('zhangsan', 1000)
    # 定义进程锁
    lock = Lock()

    process = [Process(target=func1, args=(em, lock)) for _ in range(10)]
    # 每个进程都调用一次Employee.increase方法 共十个进程 故最后输出2000
    for p in process:
        p.start()
    for p in process:
        p.join()
    print(em.getpay())
