"""
def fib (n):       #递归算斐波那契数列
    if n==1:
        return 1
    elif n==2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

for i in range(1,30):
    print(fib(i))    """


import traceback       #打印异常报告
try:                        #用循环数组算斐波那契数列
    x =50
    a = [0,]
    for i in range(1,x):
        if i == 1:
            a.append(1)
            print(1)
        elif i == 2:
            a.append(1)
            print(1)
        else:
            a.append(a[i - 1] + a[i - 2])
            print(a[i])

except SyntaxError:
    pass
except:
    traceback.print_exc()
else:                   #except和else只执行其中一个
    pass
finally:
    pass                #不管是否异常都执行的的代码


#手动抛出异常
a=int(input("请输入学生成绩"))
if 0<=a<=100:
    print(a)
else:
    raise Exception("分数不正确")   #执行时会抛出  ”异常“   此处由Python解释器捕获并显示 并报错

try:
    a = int(input("请输入学生成绩"))
    if 0 <= a <= 100:
        print(a)
    else:
        raise Exception("分数不正确")
except Exception as e:         #在try except 结构中出现异常由程序自生捕获  不会报错
    print(e)


