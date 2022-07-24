class A:
    def __init__(self,length=0,width=0):
        self.length=length                        #1
        self.width=width
    def __setattr__(self, key, value):
        if key=='square':
            self.width=value
            self.length=value
        else:
            super().__setattr__(key,value)   #此处不能用key=value，否则会出现死循环，因为在1处要赋值会调用__setattr__()用key=value 又会调用__setattr__()
    def arear(self):
            print(self.length*self.width)
a1=A(4,5)
a1.arear()

a2=A()
a2.square=5     #因为重写了赋值方法，在对a2进行赋值时判断名为square，故直接对长宽赋相同值
a2.arear()

