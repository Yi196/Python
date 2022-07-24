print("---以.py格式结尾的文件就是一个模块-----")
#调用
import math
print(math.pi)
print(dir(math))        #dir()返回可用api
print(math.__doc__)     #__doc__ 返回函数说明（'''三引号内内容'''）
print(math.__name__)    #__name__ 返回函数名
print(__file__)         #__file__ 返回当前文件绝对路径
print(math.pow(2,3),type(math.pow(2,3)))
print(math.sqrt(9))
print(math.ceil(9.01))    #math.ceil()函数，向上取整
print(math.floor(9.99))    #math.floor()函数，向下取整

from math import ceil     #该方式可以导入函数 类 变量 无括号
print(ceil(1.1))
from math import pi
print(pi)


#导入自定义模块 add_1
# from package import add_1 as ad    #package为 包 名

# print(ad.add_1(1,6))

# from package.add_1 import add_1
# print(add_1(5,4))
# print()

#常用模块
import sys
print(sys.getsizeof(24))
print(sys.getsizeof(False))

import time
print(time.time())
print(time.localtime())

import urllib.request
# print(urllib.request.urlopen("http://www.baidu.com").read())







