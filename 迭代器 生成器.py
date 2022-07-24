#迭代器 iter（）  next（）
c=iter("asdfg")  #产生一个迭代器
print(next(c))   #从迭代器中输出一个元素，全部输出后报错
print(next(c))

class Fibs:                    #计算n以内的斐波那契数列
    def __init__(self,n):
        self.a=0
        self.b=1
        self.n=n
    def __iter__(self):
        return self
    def __next__(self):
        self.a,self.b=self.b,self.a+self.b
        if self.a>self.n:
            raise Exception   #手动抛出异常
        return self.a

f=Fibs(1000)
try:
    for i in f:
        print(i,'\t',end='')
except:
    print()


#生成器
def a():           #有yield的函数就称为一个生成器，（也是一种迭代器），每当执行到yield语句时会暂停并返回后值
    print("dsad")
    yield 1
    yield 2
    yield 3
a1=a()
print(next(a1))
print(next(a1))
print(next(a1))

def fibs():     #用生成器算斐波那契数列
    a,b=0,1
    while True:
        a,b=b,a+b
        yield a
for i in fibs():
    if i>1000:
        break
    print(i,'\t',end='')