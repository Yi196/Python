import functools

def kuozhan_1(func):    #形参为一个函数对象
    '''2222这是一个函数注释用 函数名.__doc__可显示'''
    @functools.wraps(func)            #用原函数覆盖newfunc()的函数名和函数注释
    def newfunc(*args,**kwargs):      #闭包函数 定义fun()函数前后的功能
        print('你好')
        result=func(*args,**kwargs)   #传参数  返回值
        print('再见')
        return result
    return newfunc     #返回一个函数对象
@kuozhan_1         #装饰器的原理为 func=kuozhan_1(func)
def func():
    '''11111函数注释'''
    print('我是XX')
func()
print(func.__name__) #获取函数名  此处已用func（）覆盖装饰器里的nwefunc（）函数
print(func.__doc__)  #获取函数注释
print(f'返回对象为：{func},是func的函数对象，因为此处已用func（）覆盖装饰器里的nwefunc（）函数')

#装饰器 Decorator
print('=======装饰器Decorator 注意传入参数 和返回值======')
def kuozhan_11(fun):
    def newfun(a,b):       #要将原函数参数带上
        print('你好')
        result=fun(a,b)
        print(f'{a}说得对')
        return result       #当原函数有返回值时，要将原函数返回值带上
    return newfun

@kuozhan_11
def fun2(a,b):
    print(f'{a}说{b}是个好人')
    return True
fun2('小红','小明')     #直接将修饰器写在函数定义上方  省去了步骤1 的赋值调用过程
print(f'装饰器返回对象改为：{fun2}')

#装饰器的嵌套
print('=======装饰器的嵌套======')
def kuozhan_2(fun):
    def newfun():
        print('1')
        fun()
        print('2')
    return newfun
def kuozhan_3(fun):
    def newfun():
        print('3')
        fun()
        print('4')
    return newfun

@kuozhan_2           #从上往下执行  kuozhan_2修饰的是kuozhan_3
@kuozhan_3           #kuozhan_3修饰的是fun3
def fun3():
    print('5')
fun3()                #故执行结果为‘13542’
print(f'装饰器返回对象改为：{fun3}，为第一个装饰器的函数对象')

#类方法
class S1:
    def s1_1(fun):
        def newfun():
            print('1')
            fun()
            print('2')
        return newfun

@S1.s1_1      #直接调用类方法
def fun4():
    print('3')
fun4()
