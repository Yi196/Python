import time
import ctypes

#https://docs.python.org/zh-cn/3/library/functions.html#round


#dir()如果没有实参，则返回当前本地作用域中的名称列表。如果有实参，它会尝试返回该对象的有效属性列表
print(dir())
print(dir(time))

abs(-9) #返回一个数的绝对值;如果参数是一个复数，则返回它的模。

all([])  #True      #如果 iterable 的所有元素均为真值（或可迭代对象为空）则返回 True
any([])  #False     #如果 iterable 的任一元素为真值则返回 True。 如果可迭代对象为空，返回 False

ord('易')  #返回Unicode码
chr(26131)  #返回 Unicode 码对应的字符串格式。这是 ord() 的逆函数

c1 = complex(3,4)  #返回值为 real + imag*1j 的复数，或将字符串或数字转换为复数。
print(c1,abs(c1))

divmod(10,3)   #(3,1)   #以两个（非复数）数字为参数，在作整数除法时，返回商和余数。

print(globals())      #返回表示当前全局符号表的字典。这总是当前模块的字典（在函数或方法中，不是调用它的模块，而是定义它的模块）。
print(locals())       #更新并返回表示当前本地符号表的字典。 在函数代码块但不是类代码块中调用 locals() 时将返回自由变量。 请注意在模块层级上，locals() 和 globals() 是同一个字典。

#eval(expression[, globals[, locals]])  #eval 返回值为代码执行值
eval('print(abs(c1))')    #实参是一个字符串，以及可选的 globals 和 locals。globals 实参必须是一个字典。locals 可以是任何映射对象。

#exec(object[, globals[, locals]])    这个函数支持动态执行 Python 代码(可创建变量并赋值) #exec 返回值永远为 None。
exec('print("HelloWorld！")')
exec("""
a = []
for i in range(10):
    a.append(i)
print(a)
""")
x = 10
expr = '''
z = 30 
print(sum((x,y,z)))
'''
def fun():
    y = 20
    exec(expr)                               #60
    exec(expr,{'x':1,'y':2})                 #33     变量x,y被替换为1，2
    exec(expr,{'x':1,'y':2},{'y':3,'z':4})   #34     变量y被改为3 变量z先被赋值为4后又被赋值为30
fun()

#compile() 函数将一个字符串编译为字节代码。
str = 'for i in range(2): print(i)'
c = compile(str,'','exec') # 编译为字节代码对象  此处不可编译为eval()
exec(c)
str = '3*4+5'
a = compile(str,'','eval')
print(eval(a))

id(a) #返回对象的“标识值”。


class A():
    pass
aa1= A()
#isinstance(object, classinfo)  如果 object 参数是 classinfo 参数的实例，或其（直接、间接或 virtual ）子类的实例，则返回 True
print(isinstance(aa1, object))

object  #返回一个不带特征的新对象。object 是所有类的基类。它带有所有 Python 类实例均通用的方法。本函数不接受任何参数。


sum((1,2,3))  #求和函数 输入元组

print(round(12.44455667786,4))   #返回 number 舍入到小数点后 ndigits 位精度的值。

#sorted(iterable, *, key=None, reverse=False)    根据 iterable 中的项返回一个新的已排序列表。
print(sorted([2, 4, 51, 5, 131, 521]))    #默认升序 reverse = True为降序

print(vars(A))  #返回模块、类、实例或任何其它具有 __dict__ 属性的对象的 __dict__ 属性。

print(list(zip([1,2,3],[4,5,6],[7,8,9])))   #在多个迭代器上并行迭代，从每个迭代器返回一个数据项组成元组。

print(bin(12))    # 0b 转为二进制
print(oct(12))    # 0o 转为八进制
print(hex(12))    # 0x 转为十六进制
d1 = 0x11a
print(int(d1))    #转为十进制
d2 = '0x11a'
print(int(d2,16)) #字符串转为十进制

a = 'a12'
# id()获取内存地址
address = id(a)
# 1、通过变量ID 得到变量的值
from _ctypes import PyObj_FromPtr
b = PyObj_FromPtr(address)
print(b)
# 2、import ctypes
get_value = ctypes.cast(address, ctypes.py_object).value
print(get_value)