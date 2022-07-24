import time
import timeout_decorator



# 此装饰器只用于Linux系统
@timeout_decorator.timeout(2)   # timeout_exception=StopIteration 更改报错类型；use_signals=False用于多线程中
def aa():
    try:
        time.sleep(3)
        print('success')
    except Exception as e:   # TimeOut报错会被捕捉
        print(e)


if __name__ == '__main__':
    aa()