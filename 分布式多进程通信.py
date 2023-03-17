from multiprocessing.managers import BaseManager
from multiprocessing import Manager


class MyManager(BaseManager):
    pass


global_dict = Manager().dict()    # 注意此处要先将字典赋值给一个变量，用该变量在MyManager.register中注册才行，不然连接时会生成一个新的字典
''' 可调用的方法有'clear', 'copy', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values' '''


def init_global_value(ip='127.0.0.1', port=9110):
    MyManager.register('CodexGlobalValue', callable=lambda: global_dict)
    manager = MyManager(address=(ip, port), authkey=b'CodeX')
    try:
        manager.start()
    except Exception as e:
        print(e)
        manager.connect()
    return manager.CodexGlobalValue()


def connect_global_value(ip='127.0.0.1', port=9110):
    try :
        MyManager.register('CodexGlobalValue')
        manager = MyManager(address=(ip, port), authkey=b'CodeX')
        manager.connect()
        return manager.CodexGlobalValue()
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    a = init_global_value()
    a.update({'1': 2})

    print(a.items())