lst=[1,2,3,4,5,6,7,8,9,0,10]

lst.append("q")

print(lst)

lst.extend("qww")

print(lst)
lst1=["a","b","c","d"]
lst.extend(lst1)
print(lst)

#lst[1:8:1]=lst1

lst[1:8:2]=lst1
print(lst)

q_1=lst.index("q")
print(q_1)
print(lst[::4])
lst.insert(q_1,"qwer")
print(lst)

#删除元素
lst.remove("q")
print(lst)
lst.pop(1)
print(lst)
lst[0:2]=[]
print(lst)
lst.clear()
print(lst)
del lst


#修改
lst=[1,2,3,4,5,6]
print(lst)
lst[-2]=100
print(lst)
lst[1::2]=["a","b","c"]
print(lst)
del lst

#排序
lst=[12,34,5,78,24,56,1223,75,6,12]
lst.sort()
print(lst)
lst.sort(reverse=True)
print(lst,id(lst))
new_lst=sorted(lst,reverse=True)
print(new_lst,id(new_lst))
del lst

#列表生成式
lst=[i*2 for i in range(0,11,2)]
print(lst)

#输出降序排序的索引
a = [8,2,4]
b = [idx for idx,i in sorted(enumerate(a), key=lambda x:x[1],reverse=True)]
print(b)      #[0, 2, 1]

#对列表元素加入判断
a  = [i for i in [0,10,1010,0,1,11,0]
      if i ]
print(a)       #[10, 1010, 1, 11]


#非零参降序排序的索引
c = [idx for idx,i in sorted(enumerate([3,0,5,2]), key=lambda x:x[1], reverse=True)  if i]
print(c)      #[2, 0, 3]