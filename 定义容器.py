import os.path


class C:    #定义不可变容器,返回每个元素被访问次数
    def __init__(self,*args):
        self.values=[x for x in args]
        self.count={}.fromkeys(range(len(self.values)),0)  #dict.fromkeys(lst,a) 创建一个以lst为键  a为值的新字典
    def __len__(self):
        return len(self.values)
    def __getitem__(self, item):     #重写后每访问元素时执行字典值加一
        self.count[item]+=1
        return self.values[item]

c1=C(12,43,5623,32)
c2=C(43,76,0,4,34)
c1[1]
c1[1]
c1[3]
c1[1]+c2[2]
print(c1.count,'\n',c2.count)    #返回每个元素被访问次数
