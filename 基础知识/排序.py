lst=[1,2,3,4,234,6,78]
d={"id":"1001","name":"小明","成绩":"230"}
lst.sort()           #sort（）函数只能对列表排序 对原列表排序
print(lst)
d1=sorted(d)         #sorted()函数可对所有可迭代对象排序，产生一个新的列表
d2=sorted(d.keys())    #获取键
d3=sorted(d.values())  #获取值
d4=sorted(d.items())   #获取键值对
print(d1,"\n",d2,"\n",d3,"\n",d4)

lst.sort(reverse=True)    #reverse=True  表示降序排序
print(lst)

print("a=lambda x,y:x+y     lambda用于定义一个匿名函数")
f=[(20,123),(123,23),(12,54)]
e=[{"id":"1001","name":"小hong","成绩":"223"},{"id":"1002","name":"小明","成绩":"130"},{"id":"1000","name":"小li","成绩":"560"}]
f.sort(key=lambda x:x[1])     #排序时，每次取一个元组，lambda先将该元组的第二个元素索引为【1】的值返回给  key   再用key的值进行排序
print(f)
e.sort(key=lambda x:int(x["成绩"]))   #每次取一个字典，赋给x  x["A"]表示取键为A的值，返回给key 进行排序
print(e)

#非零参降序排序的索引
c = [idx for idx,i in sorted(enumerate([3,0,5,2]), key=lambda x:x[1], reverse=True)  if i]
print(c)      #[2, 0, 3]