import sys

print('**********',sys.argv[0])   #获取命令行参数0为该文件路径
#sys.exit() #结束程序

print("---以.py格式结尾的文件就是一个模块-----")
#调用
import math
print(math.pi)
print(dir(math))
print(math.pow(2,3),type(math.pow(2,3)))
print(math.ceil(9.01))    #math.ceil()函数，向上取整
print(math.floor(9.99))    #math.floor()函数，向下取整

from math import ceil     #该方式可以导入函数 类 变量 无括号
print(ceil(1.1))
from math import pi
print(pi)


#导入自定义模块 add_1
# from package import add_1 as ad    #package为 包 名
#
# print(ad.add_1(1,6))
#
# from package.add_1 import add_1
# print(add_1(5,4))
print()

#常用模块
import sys
print(sys.getsizeof(24))
print(sys.getsizeof(False))

import time
print(time.time())
print(time.localtime())

import urllib.request
# print(urllib.request.urlopen("http://www.baidu.com").read())

#添加分隔符
print('192','168','1','1',sep='.')   #192.168.1.1

class Student(object):
    pass
print(type(Student), Student.__class__, type(int))  # <class 'type'> <class 'type'> <class 'type'>


#不换行，刷新显示
for i in range(101):
    print('\r','█' * int(i),'>','-' * int(100-i),f'{i}%' ,end='')     #'\r'表示回到当前的开头，end=''表示结束符为空
    time.sleep(0.02)


a = 0.223
b = math.pi
print('\n','{:<10},{:.5f}'.format(a,b))     #{:<10} 表示a变量至少占用10个字符 不足时补空格 {:.5f} 表示小数点后保留5位

def _test_1(a:int, b:str)->str:
    return str(a)+b

print(_test_1(3,'2'))

a = 0b1001101
b = 0xA2F4C
print(a)
print(b)
print(bin(a))

# 算术运算符
print(-2**31)  # **幂运算

#位运算符
a = 1
b = 2
print(a&b)  # 位与
print(a|b)  # 位或
print(a^b)  # 位异或
print(~a)   # 按位取反  ~x 类似于 -x-1
print(a<<2) # 二进位左移两位
print(a>>3) # 二进位右移3位