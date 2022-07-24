#筛选 filter（）
#1
a=[1,2,"sj",0,"",False,True]
b=list(filter(None,a))    #第一个参数为None时，筛选出可迭代的第二个参数的所有True值
print(b)

a=filter(None,range(10))
print(next(a))

#2
def a1(i):
    return i%2
b1=list(filter(a1,range(5,46,7)))  #当第一个参数为函数时，将第二个参数依次带入函数，筛选出结果为True 的第二个参数值
print(b1)

print(list(filter(lambda x:x%2,range(5,46,7))))   #与上面四行代码作用相同

#映射map（）
print(list(map(lambda x:x*2+1,range(10))))    #将参数二依次带入参数一的函数，返回所有结果的可迭代序列