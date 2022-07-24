import timeit
help(timeit)               #帮助文档
print(dir(timeit))         #所有key
print()
print(timeit.__all__)      #作者提供给外界，使用的方法

import time
a=time.time() #标准时间
b=time.localtime(a)  #本地时间
c=time.asctime(b)   #格式输出
print(c)
d=time.strftime('%Y-%m-%d %a %H:%M:%S',b)  #指定时间格式
print(d)