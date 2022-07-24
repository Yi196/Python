#元组
t=("xiaoming",12,134,[123,1234],12.4)
t1=tuple((21,3,43,540))
print(t,"\n",t1)


t[3].append(1431231)  #元组中的可变序列可操作
print(t)



#集合
d={1,2,4,1,1,2,4,3,5,756}
print(d)               #会自动去重复
d1=set({1,2,4,1,12,3,13})
d2=set([12,13,2123,4,243,12,23,12])
d3=set("xiaoming")
print(d1,"\n",d2,"\n",d3)
d2.add(13)  # 无返回值 若集合内已存在不会报错
d.update([12,13,145,1231,32]) # 集合内已有元素不变，未有元素加入集合
d.discard(0)  # 从集合中移除0 不存在不会报错
d.remove(12)  # 从集合中移除0 不存在时报错
ret = d.pop()  # 随机移除一个元素，并返回

#子集 超集 无交集
s1={1,2,3,4,5,6}
s2={1,2,3}
s3={1,2,3,7}
print(s2.issubset(s1))       #s2是s1的子集？ True
print(s1.issuperset(s3))     #s1是s3的超集？ False
print(s1.isdisjoint(s3))     #s1与s3不相交？ False


#交集 并集 差集 对称差集
# 交集{1, 2, 3}
print(s1.intersection(s2))
print(s1&s2)
# 并集{1, 2, 3, 4, 5, 6, 7}
print(s1.union(s3))
print(s1|s3)
# 差集{7}
print(s3.difference(s1))
print(s3-s1)
# 对称差集{4, 5, 6, 7}
print(s1.symmetric_difference(s3))
print(s1^s3)
