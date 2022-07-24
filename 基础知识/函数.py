def calc (a,b=15):     #输入时若b缺省，则默认b为15
    c=a+b
    return c
print(calc(10))
print(calc(10,20))       #参数对应位置赋值
print(calc(b=20,a=10))   #指定形参赋值
print()

def s1(a,b):
    a=100
    b.append(100)
    return a,b
num1=10
num2=[12,13,23,56,78]
print(num1)
print(num2)
s1(num1,num2)
print(num1)            #函数体中改变不可变量（如 int float str 元组）值，实参不变
print(num2)            #函数体内改变可变量（如列表 字典 集合），实参跟着改变

print(s1(num1,num2))   #返回值为多个时，返回一个元组
print()

def s2(*a):            #个数可变的位置参数 不确定输入几个形参  只能定义一个*a 返回值为元组
    print(a)
s2(12)
s2(12,123,123)
def s3(**a):            #个数可变的关键字参数  输入为数个键值对  只能定义一个**a 返回值为字典
    print(a)
s3(name="小明")
s3(a=12,b=13,c=134)
#def s (*a1,**a2): 合法     def s（**a,*a）: 非法

def s4(a,b,c,d):
    print(a,b,c,d)
lst=[10,20,30,40]
s4(*lst)                 #在函数调用时，将列表中的每个元素都转换成位置实参进行传递
dic={"a":10,"b":20,"c":30,"d":40}
s4(**dic)                #调用时，将每个元素都转换成关键字实参进行传递

def s5(a,b,*,c,d):       #定义时用*隔开形参，表示*后的形参都必须使用 关键值形式传递
    print(a, b, c, d)
s5(1,2,c=3,d=4)

global age          #将age 声明为全局变量


#递归函数
def jie (n):        #算阶乘
    if n==1:
        return 1
    else:
        return n*jie(n-1)
print(jie(6))

def fib (n):       #算斐波那契数列
    if n==1:
        return 1
    elif n==2:
        return 1
    else:
        return fib(n-1)+fib(n-2)
print(fib(30))
for i in range(1,15):
    print(fib(i),end="\t")